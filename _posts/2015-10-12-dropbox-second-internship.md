---
title: Learned at Dropbox - 2nd internship, Pyston team
date: 2015-10-12 00:00:02
disqus: y
---

This is one of four blog posts on my experiences interning at Dropbox in Fall 2014 and Summer 2015. Read more about [my first internship](/2015/10/12/dropbox-first-internship), [maximizing signal in interviews](/2015/10/12/dropbox-interviews.html) and [the social, cultural and business aspects](/2015/10/12/dropbox-misc.html).

During my second internship, I worked on [Pyston](https://github.com/dropbox/pyston), an open-source Python JIT compiler. Compilers are programs that generate machine code from human-written source code. Just-in-time compilers do some of that work at runtime - it will generate code to execute as the program is being executed. This is a very very different kind of project from my previous internship. I am moving from building a consumer-facing front-end product to building low-level fundamental infrastructure code [^1].

JITs
----

The first thing I learned from the Pyston codebase is what a JIT compiler is or rather, what it can be. I think that when most people first hear about JITs, it is almost always in the context of the JVM or .NET. While learning Java or C#, we learn that code is first compiled to an intermediate portable bytecode, and a final translation step to machine code occurs when the program is run. This is used to explain Java/C#'s startup time. This layer of abstraction increases portability and allows for some machine-specific optimizations. Otherwise, the bytecode looks very machine-like already (even though it is technically interpreted) as Java and C# are static languages.

JITs for dynamic languages don’t have much of a pre-compilation step. They often default to execution by an interpreter and compile parts of the code as needed (often one function at a time). A good illustration of the power of a dynamic language JIT is the inline cache optimization.

Suppose we implement a distance function for vectors:

``` python
def length(v):
    vx = v.x
    vy = v.y
    return sqrt(vx * vx + vy * vy)
```

Since Python is dynamic, `v` could have any type. To get the field `x`, we need to do a hash lookup. The function would compiled to something like

```cpp
PyObject* length(PyObject* v)
{
    vx = hash_lookup(v, "x")
    if (!vx) raise error("attribute x not found")
    vy = hash_lookup(v, "y")
    if (!vy) raise error("attribute y not found")

    // Objects in Python are always boxed
    return new PyFloatObject(sqrt(vx * vx + vy * vy))
}
```

Note that this is slow due to the necessity of doing hash lookups. The idea behind inline caching is to record the type of the arguments to a function. If the function is called often with an argument of the same type, we could recompile the function to take a “fast path” which assumes that type. For example:

```cpp
PyObject* lengthFaster(PyObject *v)
{
    // If guard fails, fall back to slow path
    if (typeof(v) != type(vector))
      return length(v)

    vx = ((vector*)v).x
    vy = ((vector*)v).y
    return new PyFloatObject(sqrt(vx * vx + vy * vy))
}
```

_For simplicity, this example ignores the issue of making sure vx and vy support multiplication and addition._

Feature work
------------

Some of my work on Pyston has been compatibility/feature work. We want Pyston to have the same behavior as CPython, the default Python implementation, whenever possible. For example, when you use the slice operator on an object (e.g. `obj[1:]`), CPython will call `__getslice__` (technically deprecated but still supported) or `__getitem__` depending on a number of different conditions. I also helped build some preliminary support for NumPy, a popular Python library (compile it + run a very simple program).

When it comes to compatibility work like this, there are a lot of things to do. You want to support a library. It crashes. You debug it for a while and fix the crash. It crashes again some number of function calls later. This process can repeat ad infinitum. A good strategy is to be as hacky as possible during this phase. A crash occurs in a internal C function? Comment the whole function out. A line of Python uses a feature we don’t support? Comment out that line too. This is a strange process that took some time to get used to. _Normally_, in software engineering, you aim to write correct code.

Nevertheless, the advantage of doing this is that you end up with a list of TODOs which gives a sense of the scope of the problem. Another advantage is that it isolated a number of little tasks that I subsequently put up as Github issues for other contributors to fix. That may sound very lazy, but Pyston is a complex project and at this stage, it is very valuable to have easy tasks for interested contributors to dive their feet in the codebase with. It makes the project accessible. It’s really hard to get into Pyston and start working on say, implementing a new garbage collector. There’s too much context needed. However, it’s very reasonable to add the `__doc__` attribute to `capifunc` object since it’s a self-contained task but allows the contributor to start touching the codebase.

Finalizers
----------

My main work on Pyston involved the garbage collector. For the first few weeks, I implemented finalizer support. A [finalizer](https://en.wikipedia.org/wiki/Finalizer) is a method that gets called when an unreachable object is about to get deallocated by the garbage collector. In Python, this would be the `__del__` method. This is often used to manage external resources. For example, a file object might have a finalizer that closes a file handle.

Why is this problem hard? Isn’t it just adding a function call?

Finalizers can contain arbitrary code. So what happens in this scenario?

```python
import gc
class C(object):
    def __del__(self):
        gc.collect()
```

Starting a garbage collection pass while the previous one is in progress is almost certainly going to break some invariants (e.g. mark bits that are not cleared).

Or what about this?

```python
x = None

class C(object):
    def __del__(self):
        global x
        x = self

def create_short_lived_object():
    c = C()
    # `c` immediately goes out of scope and becomes unreachable

create_short_lived_object()
gc.collect()
print x
```

The finalizer just assigned the object back into a global variable, so now it is reachable again! Languages like Python and Java really hate to have invalid references. So the only correct behavior is to [resurrect the object](http://morepypy.blogspot.kr/2008/02/python-finalizers-semantics-part-2.html).

On top of this, implementing finalizers for Python has even more edge cases like supporting the `tp_dealloc` slot in C extensions, a second type of finalizers. Care must be taken not to break JIT invariants (e.g. guards). Those are subtle problems that are hard to explain in a blog post, but let’s just say that finalizers are one of the nastiest features in programming language history (for the compiler writer) [^2].

Moving garbage collection
-------------------------

Most modern languages have a moving garbage collector. Those garbage collectors, in addition to freeing objects, move (copy) objects from one address to another. This opens up room for a lot of performance optimizations [^3]. I spent a couple days reading papers and writing an implementation proposal, which was nice - I finally get to read papers at work! Then, with the time I had remaining in the internship, I started some preliminary work into implementing it [^4].

This was a lot of fun because I went into garbage collection in a lot of depth. Garbage collection techniques are easy to explain conceptually but practical considerations involve a lot more than textbook presentations let on. For example, the name ‘garbage collection’ has the connotation ‘algorithm that frees garbage’. However, a garbage collector is never designed independently. The implementation of the heap is strongly tied to the implementation of the garbage collector (e.g. semispaces in copying and generational GCs). The rest of the runtime might need to do bookkeeping to support the garbage collector (e.g. reference counts, write barriers). Choosing a garbage collector requires evaluating the combined performance impact on allocation costs, deallocation costs and runtime costs.

I also learned that textbook garbage collection algorithms almost never work in practice [^5].

C/C++
-----

I also learned a lot about low-level coding with Pyston, which operates at a lower level than anything I’ve done before. For example, we use C-style function pointers. These are rarely used nowadays because there are better engineering techniques available (e.g. lambda functions, virtual dispatches). However, in Pyston, we may need to call generated code, which you can only do with function pointers.

Pyston is designed for performance and it is surprising how much performance gains code inlining can achieve. This helped me gain a whole new level of understanding into the saying “indirection [abstraction] solves every problem except that of too many layers of indirection”, as every layer of abstraction introduces a performance hit.

During my second internship, there were also some C++ meetups organized by Alex Allain which were also very nice. Notably, Chandler Carruth came to give a talk about Clang, and how they improved over GCC, and the nice static analysis tools it features.

----------------------------------------

[^1]: Being a return intern has the perk of knowing all the teams and being able to have meetings with them. This is why it was worth going to Dropbox twice (otherwise, in general, I think it's preferrable to try a few different companies to maximize exposure to different industries).

[^2]: http://ericlippert.com/2015/05/18/when-everything-you-know-is-wrong-part-one/ http://ericlippert.com/2015/05/21/when-everything-you-know-is-wrong-part-two/

[^3]: Hand-wavy explanation as to why. Reference counting requires bookkeeping whenever references are changed, objects passed as arguments to methods, etc. Roughly speaking, the cost of the overhead is `O(# operations in the program)`. Even in a program where almost no object ever gets allocated (e.g. numerical programs), this still adds a lot of overhead.

    Mark-and-sweep collectors mark the reachable objects and sweep over the entire heap to free the unreachable objects. The cost per garbage collection is `O(size of heap)`. A garbage collection will typically occur every `n` allocation, given a reasonable allocation pattern. Then the cost of mark-and-sweep can be roughly amortized to be `O(# of allocations)` <= `O(# operations in the program)`.

    Some moving collectors, such as copying collectors, copy all reachable objects to a new area in the heap and discard the old area entirely. The cost per garbage collection is then `O(size of the live heap)` < `O(size of the heap)`.

    These are very approximate figures and constant factors matter a lot in garbage collector. Nevertheless, they help give a sense of the usefulness of moving garbage collectors.

[^4]: Most of it involved uncovering additional work we would need to do elsewhere in the codebase. For example, in mark-and-sweep, you can sometimes forget to scan a pointer in an object and get away with it. The same pointer might always be present in another object that we do scan. However, in moving collectors, the garbage collector needs to be aware of every single pointer, because it might need to update them as the object being pointed to moves around the heap. This is non-trivial — generated code might contain embedded pointers for instance.

[^5]: Conservative garbage collection. Lots and lots to discuss there, and Pyston has a lot more conservative pointers than most other language implementations due to support for C extensions.
