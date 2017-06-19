---
title: Compiler optimization contest (Part II) - Racket functional programming
disqus: y
---

In the [previous post](/2014/08/08/compiler-optimization-i.html), I talked about my participation in a compiler optimization contest, where the goal was to compile a program into the smallest possible executable. Three languages were allowed for the contest : C, C++ and Racket, a dialect of Lisp/Scheme. No one would reasonably choose to use C for a high-level program like a compiler, especially for a contest, so it was really a choice between C++ and Racket, two vastly different languages.

Whereas the previous post focused on the compiler, this post will focus on the usage of the Racket language to write the compiler.

As I intend for this post to be more of a discussion on programming languages than an enumeration of Racket features, the focus will lean more towards parts which I did not like than those which I did. However, despite some dissatisfactions, I quite like Racket.

*This is not meant to provide any definite answer on whether Racket is a good or bad language. In fact, much of the analysis will be written mostly with respect to my own personal programming preferences and in comparison to languages I am familiar with, mainly C++, Python, F#, C# and Java.*


Context
-------

Prior to this, I had only written small (100-400 lines) Racket programs as well as a few F# programs of similar size (100-800 lines). This compiler was 10x larger, ~3300 lines not including tests, so I suppose this qualifies as a "medium" size program.


Pattern Matching
----------------

Pattern matching is a distinctive feature of functional languages.

In particular, pattern matching is an extremely powerful way of dealing with case analysis. Rather than analyzing a data structure with a myriad of branches, one can simply write down the form of the data structure and bind all its internals to symbols.

It is much easier to read and less error-prone. The code below handles the grammar rules for addition and subtraction exactly, where the input is a nested list.

```racket
(struct expr-binop (type op expr1 expr2))

; parse-tree -> expr
(define (get-expr expr)
  (match expr
    [`("expr term" ,term) (get-term term)]
    [`("expr expr PLUS term" ,expr  _ ,term)
     (expr-binop 'NONE '+ (get-expr expr) (get-term term))]
    [`("expr expr MINUS term" ,expr _ ,term)
     (expr-binop 'NONE '- (get-expr expr) (get-term term))]))
```

In contrast, the equivalent C++ code (including error checking, which needs to be explicit) would need:

```cpp
AstNode *getExpr(ParseTree tree)
{
    if (tree.rule == "expr term" &&
        tree.children.size() == 1) {
        return getTerm(tree.children[0]);
    } else if (tree.rule == "expr expr PLUS term" &&
               tree.children.size() == 3) {
        return new BinaryNode('+', tree.children[0], tree.children[2]);
    } else if (tree.rule == "expr expr MINUS term" &&
               tree.children.size() == 3)
        return new BinaryNode('-', tree.children[0], tree.children[2]);
    } else {
        // Pattern matching throws an exception if none of the clauses
        // match, so we need this here too for completeness.
        throw ...
    }
}
```

In the C++ version, many things need to be written explicitly (e.g. indexing into the children) which can be more error prone. Note how in the C++ example, `tree.children[0]` is not automatically bound to a name, a form of self-documentation. There's no way for the compiler to optimize sequential else-ifs into a finite state machine as commonly done for pattern matching, so the C++ version would run slower as we add more clauses. On top of it, this is a simple example, where we only examine the root node during traversal. Typically, we would also need to get into nested conditionals and the structure of the code becomes harder to read in one glance.

So pattern matching works quite well for constructing a data structure from the input in this case. I also use pattern matching later in the program, when I want to iterate or traverse my data structures.

```racket
; Note structs in Racket are closer to C-style structs
; than C++ style structs which are the same as classes.
(struct ssa-binop (op target var1 var2))

(match ssa

  ; ... cases ... (by the way, semicolon is a comment in Racket)

  ; Prints MIPS assembly for binary arithmetics.
  ; printi is a local function that prints with indentation
  [(ssa-binop '+ target var1 var2)
   (printi "add $~a, $~a, $~a" target var1 var2)]
  [(ssa-binop '- target var1 var2)
   (printi "sub $~a, $~a, $~a" target var1 var2)]
  [(ssa-binop '* target var1 var2)
   (printi "mult $~a, $~a" var1 var2)
   (printi "mflo $~a" target)]
  [(ssa-binop (or '/ '%) target var1 var2)
   (printi "div $~a, $~a" var1 var2)
   (if (eq? (ssa-binop-op ssa) '/)
     (printi "mflo $~a" target)
     (printi "mfhi $~a" target))]

  ; ... more cases ...
```

This looks like a reasonable way of printing different strings depending on the "object". However, having done a lot of OOP, I ended up asking myself, how does it compare with polymorphism? Alternatively, we could have:

```csharp
class SsaInstruction
{
    public virtual void PrintMips() {}
}

class SsaBinary : SsaInstruction
{
    private String op;
    private SsaVariable var1, var2;

    public override void PrintMips()
    {
        Console.WriteLine(...)
    }
}

class SaaMemLoad : SsaInstruction
{
    private SsaVariable var1, var2;

    public override void PrintMips()
    {
        Console.WriteLine(...)
    }
}
```

This is interesting, because these two approaches to case analysis come at orthogonal angles. This becomes clear if we consider hypothetical scenarios:

1) I want to implement constant folding, so I need to traverse my parse tree. With pattern matching, I add *one* file with a large pattern match over my dozen data structures or, with polymorphism, I add one function to *each* file containing a data structure/class.

2) I want to implement a new grammar rule/instruction that casts floats into integers. I add a new structure/class for this instruction to *each* file that traverses my parse tree or, with polymorphism, I add *one* file for this new instruction.

Observe and contrast these two scenarios. If we represented our problem space as pairs (x, y) = (action, object), pattern matching is like sorting by x first, and polymorphism is like sorting by y first. I call these *sorting by action* and *sorting by object*, respectively.

Which is better? Neither. If data points are more spread out along the x axis, we usually want to sort by x. If the data points are more spread out along the y axis, we usually want to sort by y.

Functional languages, as long as they support classes, allow both, with perhaps a slight bias towards sorting by action.

Imperative languages typically* strongly favors sorting by object. There are ways of sorting by action, such as the [Visitor Pattern](http://en.wikipedia.org/wiki/Visitor_pattern). However, notice that to implement the pattern, you need at least multiple classes, inheritance (& polymorphism) - often overloaded functions. All wrapped in a terminology (accept, visit) that is not necessarily aligned with the actions being performed. Given that we are really only doing case analysis, pattern matching is a more elegant approach.

> \* [C#](https://roslyn.codeplex.com/discussions/560339) and [Swift](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language/Patterns.html) are getting there.

Dynamic Typing
--------------

Static vs dynamic typing is a highly combustible topic that only requires a tiny spark to burst into a flame war. *Most of the time*, I can live with either. For example, I appreciate both C# and Python roughly equally.

For Racket, my main point of comparison is with F# (I don't know Haskell and have too little experience with Scala), and I strongly prefer F# on this aspect.

While writing my compiler, I had a particularly complex recursive function that dealt with reassigning variable to registers at the end of branches. Without helper functions, the overall structure looked like this:

{% highlight racket linenos %}
(define (set-right var [seen (make-hash)])
  (define current-reg ...)
  (cond
    [(not (hash-has-key? original var))
     (...)
     (void)] ; <--------------
    [else
     (... some work ...)
     (define wanted-reg (hash-ref original var))
     (cond
       [(... condition1 ...) empty]
       [(... condition2 ...)
        (... some recursive work...)]
       [else
        (... some work...)]
        (define blocking-var (hash-ref current wanted-reg))
        (cond
          [(... condition3 ...)
           (... some recursive work ...)
          [else (... some recursive work ...)]
        )])]))
{% endhighlight %}

Notice on line 6, I return `(void)`, which is a mistake - I want to return `empty`, which represents the empty list and is semantically very different. The problem is, the code didn't crash at that point. It crashed in a separate file thousands of function calls later when I finally made use of the return value. It also just so happened that this situation only occurred when running very large test cases, the kind for which unit tests are either impractical or require a lot of work. This made it a pain to comb through the output to trace the problem back to its source.

> Racket [contracts](http://docs.racket-lang.org/guide/contract-func.html), which are a form of assertions, is a solution, but require two tradeoffs : more work for the programmer when the function returns a nested data structure and the need to verify the contract at runtime.

In an imperative language, I can live with it. Type-related errors are diluted among a sea of other possible errors - off by one errors during iteration (happens less with structural recursion), wrong assumptions about the values of particular variables at particular times, null pointer exceptions, etc. So static typing reduces the frequency of some types of bugs, but not all.

In a functional language, functional-style programming patterns such as immutability already eliminate a vast range of likely bugs. In Racket, most errors that I need to iron out could have been caught with static typing. In contrast, F# is a statically-typed functional language and my experience is that 99% of the time, if the algorithm is correct and the code compile, it will just work.

I strongly prefer to catch error at compile-time than runtime. Even if I have enough tests to catch all possible type errors at runtime, it still takes time to run those tests, more than it takes to compile the program.

I don't really mind the inconvenience of having to specify types. For function declarations, I would already have the types (the contract) in a comment. If the language has [Type Inference](http://en.wikipedia.org/wiki/Type_inference), I don't even need to specify types elsewhere in the program for the most part.

```racket
; This is an example of a contract.
; int int -> int
(define (sqr-add x y)
  ; No types declared.
  (define x-sqr (* x x))
  (define y-sqr (* y y))
  (+ x-sqr y-sqr))
```

```csharp
// In F#, the contract is part of the function declaration.
// Note that this is a toy example. For this particular function, we wouldn't
// specify any types to allow this function to work on any type
// supporting * and +, like the Racket version is capable of.
let sqr-add (x : int) (y : int) =
    // No types declared.
    let x-sqr = x * x
    let y-sqr = y * y
    (x + y)
```

It's also nice to be able to mix different types in a collection, which is easy to do easy dynamic typing. In my compiler, I have lists of either lists or structs, as well as hashtables whose keys and values can both be either integers or structs.

However, I find that situations requiring mixed types only involve a few types. For these purposes, [Algebraic Data Types (Haskell)](http://www.haskell.org/haskellwiki/Algebraic_data_type), [Discriminated Unions (F#)](http://msdn.microsoft.com/en-us/library/dd233226.aspx) and their equivalents handle this quite well. They are both lightweight in syntax and lightweight in execution.

```csharp
// A commonly-used union type to prevent null pointer exceptions.
type Option<'a> =
    | Some of 'a
    | None

// We could use this for nested list of integers representing n-way trees.
type NestedList =
    | Node of List<NestedList>
    | Item of int
```

There exists a variant of Racket called [Typed Racket](http://docs.racket-lang.org/ts-guide/), but I am not convinced at first glance that adding types to a language that was not designed for it upfront leads to very elegant syntax (I reserve the right to change my mind on this statement, should I get the time to look into it more).

Finally, given that functional languages still aren't mainstream, there are enough barriers to their adoption that I do not want performance to be an argument against using them - and statically typed languages are typically faster since more information is available to the compiler for optimization (again, this is up for contention, but the very fact that it *might* be an issue suffices for my point).


Classes vs Nested Functions
---------------------------

Generating [SSA instructions](http://en.wikipedia.org/wiki/Static_single_assignment_form) for my compiler involved recursion, but it also involved carrying around state during the recursion. In addition to returning the SSA instructions, I needed to build or keep track of :

1) The set of variables being read in the current code block.

2) The set of variables being written in the current code block.

3) Various miscellaneous information such as whether a variable needs to be on the stack.

4) A counter for global ids (e.g. label names - if0, endif0, if1, endif1, ...)

5) A counter for local ids (e.g. variables - x1, x2, temp1, temp2)

How might we do this?

We could have <del>global variables</del> no, of course not. Very funny.

We could pass along the state at every function call and return everything we need to aggregate as a tuple.

```racket
; In this context, `values` is used like a tuple
(define (big-fun state1 state2 state3 state4 state5 lst)
  (cond
    [(empty? lst) (values x y z)]
    [else
     (match-define (values x y z) (big-fun state1 state2 state3
                                           state4 state5 (rest lst)))
     (... modify state ...)
     (values (f x) (g y) (h z))]))
```

Having to type all the arguments every time we make a recursive call and having to unpack all the return values becomes quickly unmaintainable. We could alias the recursive call with a local helper function, but that quickly breaks down too when we need mutual recursion.

We could turn the recursion into a loop inside a function, and use local variables.

```csharp
void foo()
{
    int state;
    List<Something> moreState;
    while (...)
    {
        // What used to be a beautiful recursion.
    }
}
```

This is error-prone and does not work with mutual recursion either without [complicated solutions](http://en.wikipedia.org/wiki/Trampoline_(computing)).

We could have a class, and put the state in the class' fields. This would be the standard approach in OOP languages, since any task that requires carrying around a large amount of state is probably significant enough to warrant a class.

```csharp
class SsaBuilder
{
   int state;
   List<Something> moreState;

   void RecursiveFunction(...)
   {
       ...
   }

   void MutuallyRecursiveFunction(...)
   {
       ...
   }
}
```

This is similar to using a global variable, but in better practice. The state is private to the class and instanced along with the class so we don't need to clean it up if we need to use the class more than once.

Basic software engineering 101 so far.

What other alternatives are there?

I've tried two functional approaches in my compiler.

**1) Pass around a mutable state object**

In my code to generate SSA instructions, my co-recursive functions look like:

```racket
(struct recursion-state (write-set read-set proc-analysis
                                   global-counter local-counter) #:mutable)

(define (gen-ssa-expr state expr)
  (match-define (recursion-state write-set read-set proc-analysis
                                 global-counter local-counter) state)
  (define references (hash-ref proc-analysis analysis-references))
  (match expr
    ...
    [(...) (gen-ssa-expr state expr)] ; recursive call
    ...
    ))

(define (gen-ssa-stmt state stmt)
  (match-define (recursion-state write-set read-set proc-analysis
                                 global-counter local-counter) state)
  (define references (hash-ref proc-analysis analysis-references))
  (define nopropagate (hash-ref proc-analysis analysis-nopropagate))
  (match stmt
    ...
    [(...) (gen-ssa-expr state expr)] ; mutually recursive call
    ...
    ))

; Generate the ssa for some procedures.
(define (gen-ssa-proc global-counter funtable analysis procedure)
  (match-define (proc id params dcls stmts return) procedure)

  ; Initialize the state here.
  (define local-counter (counter (make-hash) (make-hash)))
  (define proc-analysis (hash-ref analysis id))
  (define references (hash-ref proc-analysis analysis-references))

  (counter-init-sym local-counter temp-sym)  ; Temporaries for expressions.

  (define state (recursion-state (make-hash) ; write set
                                 (make-hash) ; read set
                                 proc-analysis
                                 global-counter
                                 local-counter))

  (... calls to gen-ssa-stmt ... ))

; Generate the ssa code for all procedures
; Some state is initialized here.
(define (gen-ssa funtable analysis procedures)
  ; Counter for every symbol that may need one.
  (define global-counter (counter (make-hash) (make-hash)))

  ; Initialize special symbols.
  (counter-init-sym global-counter if-false-sym)
  (counter-init-sym global-counter if-end-sym)
  (counter-init-sym global-counter start-while-sym)
  (counter-init-sym global-counter end-while-sym)

  ; Generate ssa for all procedures.
  (for/list ([proc procedures])
    (gen-ssa-proc global-counter funtable analysis proc)))
```

I pass around a single struct containing all the state I need and unpack it at every function. The state is initialized in the "root" function calls, gen-ssa and gen-ssa-proc (these functions are in their own file and only gen-ssa is exported, so the other ones are really just helper functions).

The unpacking part is questionable. It is a form of code duplication and increases maintenance requirements, but is necessary to stay sane (otherwise every field access requires the heavyweight `(recursion-state-fieldname state)` syntax (more later on verbosity).

However, overall the solution is simple and all the functions are top level.

**2) Use Racket classes**

This is similar to passing around a mutable struct, except that unpacking is harder.

**3) Use nested functions**

I took a different approach for constant propagation and copy propagation.

```racket
; Some of the state is part of the function parameters.
(define (copy-constant-propagate-proc analysis procedure)
  ; Some of the state is created at the very top of the function.
  (match-define (ssa-proc id params type stmts locals) procedure)
  (define mappings (make-hash))
  (define constants (make-hash))
  (define references  (hash-ref (hash-ref analysis id) analysis-references))
  (define nopropagate (hash-ref (hash-ref analysis id) analysis-nopropagate))

  ; Helper functions have access to that state.
  (define (reduce-binop op target var1 var2) ...)
  (define (propagate stmts)
    (cond
      [(empty? stmts) stmts]
      [else (... recursive calls to (propagate stmts) ...)]))

  ; Call recursive helper function after everything has been defined.
  (ssa-proc id params type (propagate stmts) locals))
```

Here, `copy-constant-propagate-proc` is an outer function representing the root action I want to undertake, likely the one to be exported. However, the outer function is not recursive. Inner functions are recursive, and since they have been defined inside the outer function, all the parameters and definitions of the outer function are in the scope of the inner function, unless shadowed. This uses the concept of [nested functions](http://en.wikipedia.org/wiki/Nested_function).

Notice that this is extremely similar to using classes. We have the definitions (fields) on top followed by helper functions (methods) and end with an initial function call (with classes, probably the constructor or a run() method).

In fact, conceptually, it makes more sense than using a class. Fundamentally, we are trying to execute an action (here, perform constant propagation). Thus, it makes more sense for the action to be represented by a function than a class such as `ConstantPropagationMaker`. OOP programmers have an unfortunate tendency to turn everything into nouns, especially in Java (see [Execution in the Kingdom of Nouns](http://steve-yegge.blogspot.ca/2006/03/execution-in-kingdom-of-nouns.html)). Of course, in this case, it is unavoidable without first-class support for nested functions.

In practice, I find using nested functions a little bit more messy than using a class, but it does have less syntactic/OOP cruft surrounding it, so I wouldn't say one is better than the other.

The difficulty with functional languages here is not that they don't support carrying around large amounts of state, but that it is not taught. In imperative languages, not only does state comes more naturally, but the average programming article will have a focus on state.

Beginner level material for an OOP language might teach you how to make a simple game. Games happen to involve carrying around state. In contrast, beginner level level material for functional languages tend to focus on how elegantly problems can be decomposed into subcomponents. This happens not to involve a lot of state. Past the beginner level, resources are scattered all over and it is difficult to establish what "standard" solutions are (I will discuss later in the post why I think it is important to have standard solutions).

A similar difficulty arises concerning extensibility.


Extensibility
-------------

Suppose I have an abstract syntax tree composed of many different kinds of nodes. Now, I want to label some of those nodes with types, because the language I want to compile is statically typed. I also want to label the nodes corresponding to functions with a boolean indicating whether the function has a side effect or not, because while optimizing, I found that I needed that piece of information.

How do I do this?

If I was dealing with objects and classes, I would add a new field. Unless you have some obscure code that depends on the bytesize of your objects, you can add any number of fields you want to a class and everything will still compile and execute just the same.

**1) Add a field to a struct**

This is easy right?

```racket
(struct (node value left-child right-child))
=> (struct (node newfield value left-child right-child))
...
(displayln (node-newfield some-node))
```

Except that this breaks pattern matching. Every clause in which the struct appears will need to be updated, since pattern matching works by specifying every single field (even when they are left unused with `_`). Furthermore, we often like to pattern match against larger structs using `(match-define (struct field ..))` to unpack all the fields for more convenient access (as mentioned when I talked about passing mutable states).

**2) Use classes**

We could go back to the object-oriented way, but we lose pattern matching. While I did not have the time to learn Racket classes & objects for the compiler contest, [the documentation](http://docs.racket-lang.org/guide/classes.html) makes me think that classes were added to Racket for the sake of having classes. The syntax for accessing a field and calling methods is `(send object fieldname)`. Would anyone really want to use that? Racket simply isn't designed for objects.

**3) Create a wrapper structure**

Why not create another structure?

```racket
(define typed-structure (original-structure type))
```

This is clean if we *have* the new structure, but someone needs to construct it. When there are many different structures and they are nested into each other, this is a lot of work.


**4) Use an internal dictionary**

One method I've seen suggested was to include a hashtable field for every struct that may need to be extended. This is like adding a "misc" field. This method has merits - we can extend the struct by adding keys to the hashtable, access those keys only when needed and leave the rest of the code intact.

This is also similar to Javascript, where [every object is essentially a dictionary](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/keys).

This also has issues.

What if we want to copy the struct? We will need to copy the internal hashtable. What if we want to access the field in a more convenient manner?

```racket
; This is pretty verbose.
(hash-ref (structname-misc mystruct) myfieldname)`
```

That would require defining a slew of new functions. We could achieve it with a macro, but this feels like work that I should not have to do just to be able to extend structs without twisting my arm around.

From a performance perspective, how will the compiler optimize this? All the compiler sees is a hashtable, indexed by strings or [symbols](http://docs.racket-lang.org/reference/symbols.html). Even the programmer will have more difficulty keeping track of allowed fields.

Unlike Javascript, the hashtable accesses are explicit and indistinguishable from fields. Error messages for non-existing fields will be about missing keys. This is like a second layer of interpreted syntax on top of an interpreted language, which can't be very good.


**5) Use an external dictionary**

If we think about our program (here, compiler) as a pipeline, structs will be needed at various stages of the pipeline (e.g. the AST is only needed up until SSA generation). It may also be that certain fields are only needed in specific stages of the pipeline.

As such, we could have a hashtable of values, indexed by the things we want those values to label. In the compiler, this occurred naturally for symbol tables, where the argument and return types of a procedure were stored not in the procedure, but in the symbol table. I also used this approach during register allocation to annotate the instruction in which each variable last appears.

```racket
; Symbol table indexed with value equality (good if keys are strings/symbols)
(define symbol-table (make-hash))
; Symbol table indexed with reference equality (good if keys are objects)
(define var-appearances (make-hasheq))
```

Those coming from the imperative world will probably think this approach is very strange, but it is reasonable in a functional context. In fact, conceptually, it may make more sense than adding fields to a class, because the field we are adding is more a property of the pipeline stage we are in than the object itself. We would rather avoid bloating the class with temporary annotations from all the different pipeline stages.

This still causes a performance hit and has similar issues with reporting helpful error messages for the programmer, but is localized to a single field, so it's not as bad.

On the other hand, this approach is only viable if the use of the extra field is highly localized. Otherwise, we still need to pass the hashtable around which then offloads the syntactic cost to other parts of the program.

We can see that all of these approaches have their tradeoffs.


Verbosity
---------

In Racket (and all the Lisp variants in general), everything is an S-expression.

```racket
(element1 element2 ... elementn)
```

That is, everything is either an atom (e.g. `element1`) or a list of things, denoted with `()`. It is common for the first element to be a function and the rest of the elements to be the arguments the function is applied to (e.g. `(+ 1 2)`).

Outside of [esoteric languages](http://en.wikipedia.org/wiki/Brainfuck), you will be hard pressed to find a syntax as uniform as S-expressions. This has various benefits, [in particular in regards to macros](http://stackoverflow.com/questions/267862/what-makes-lisp-macros-so-special) - the Lisp family's powerful macros reign supreme.

However, at the same time, this severely reduces the range of permissible syntax, and some would be a lot more appropriate in certain contexts. My two main gripes are with structs and hashtables which the compiler needed everywhere.

With structs, I need to type the name of the struct in addition to the field I want to access, *every time* I want to access *any* field. Hashtables are quite bad too.

```racket
; Access a field - contrast with myobj.field
(obj-field myobj)

; Increment an element in a hashtable.
; Contrast with mytable[mykey] += 2
; Even mytable[mykey] = mytable[mykey] + 2 isn't as bad.
(hash-set! mytable mykey (+ (hash-ref mytable mykey) 2))

; Alternatively, create new lambda functions. Not the most
; straightforward way of coding.
(hash-update! mytable mykey (λ (val) (+ 2 val)))
```

By the nature of S-expressions, even macros won't allow the typical `.` and `[]`. Certain forms are just naturally more readable when it not in prefix notation. Sure, you can define some helper functions for things like incrementing in a hash table, but in which files are they going to be? What if I want to do something just slightly different? The more of this kind of work I need to do just to make the code readable, the less beneficial the language becomes.

Returning tuples are also a mess to deal with. In Racket :

```racket
(define (foo)
  (values 1 2))
(define-values (x y) (foo))
```

In python :

```python
def foo():
    return (1, 2)
x, y = foo()
```

In F# :

```csharp
let foo =
    (1, 2)
let x, y = foo()
```

On a toy example, this might not look too bad, but it becomes quickly annoying to deal with when writing mutually recursive functions that sum to 100s of lines.

For mathematical expressions, prefix notation isn't natural. It's one thing to ask programmers accustomed to loops to use recursion. It's another to ask people to switch from a universal notation learned in 1st grade.

```racket
; a * b + (c + d) * f
(+ (* a b) (* (+ c d) f))
```

To avoid extremely long nested expressions, it is good practice to split them up and name some of the intermediate expressions. That also bloats the code.

```racket
; Either use define or let

; Define is verbose - compare (define ...) with let ... = from the ML family
(define intermediate1 (...))

; Let is verbose - so many parentheses! Also, adds a level of nesting
; which I think increases cognitive load.
(let ([intermediate2 (... intermediate1 ...)])
  (dostuff (... intermediate2 ...)))
```

At this point, it will probably appear like I am nitpicking insignificant syntax details and indeed, it would not be an important consideration when choosing a language. Still, I think the requirement that everything be S-expressions might be too restrictive of a constraint.

> Alternative syntax like [Sweet-expressions](http://readable.sourceforge.net/) help with readability, to a limited extent.


Macros & Customization
----------------------

I'll be honest, I haven't used Racket macros much, nor am I anywhere near proficient with them.

Nevertheless, I can see how they could be very powerful and allow you to customize the language to your own taste. If the language is missing a functionality, just create it. Great tool.

However, unless I am tinkering just for fun, I think there is more value in having a fixed set of standard language features and idioms (as long as they are good) than a weak base that can easily be extended.

Java is on one end of the spectrum. The language itself is very rigid and there usually is only one way to do things (which leads to it being verbose at time, e.g. [lack of operator overloading](http://stackoverflow.com/questions/77718/why-doesnt-java-offer-operator-overloading)). On the other end are the Lisp family and Haskell at the very edge (one of the primary uses of Haskell appears to be programming language research).

Python lies somewhere in the middle. There are a lot of ways to do things but due to an emphasis on idioms by the Python community, Python code written by one Python programmer is more or less readable by another Python programmer. Unlike Java, there are still plenty of nice ways to express things, such as list comprehensions.

There's no problem with *me* using some macros to do a few more things nicely, but what about the next person? What macros will they use? If we're talking about helper functions (like increment in a hashtable), how will they name their helper function?

By using too many macros, everyone effectively ends up doing things differently, heck, almost using different languages. Learning the language also becomes more difficult. Our brain uses pattern matching too, and we usually pick up on programming patterns when we see them more than once. If all the existing articles, blog posts, tutorials, code snippets are different, pattern matching becomes difficult. If that is the case, how can the language itself (and it's user base) grow?

So while in theory, there are a lot of solutions to many of my issues in this post, I'm not convinced the kind that involves macros or defining helper functions are the good ones. In my opinion, Python is a language that does it right (C# is pretty good too - sufficiently standardized to be as good as Java for enterprise, much better language features. Alas, there are way too many roadblocks for it to replace Java).


Racket Debugging & Profiling
-----------------------------

Racket's default error handling is subpar. In a lot of cases, I would either get no stacktrace (and no line number) or an incomplete, unhelpful one (e.g. `define-values` with the wrong number of values). That made debugging rather tedious at times. There's [errortrace](http://docs.racket-lang.org/errortrace/using-errortrace.html), but shouldn't line numbers for error reports come by default? As for the instrumentation, I never managed to get it to report anything useful.


Conclusion
----------

If I were to do the compiler contest again in Racket, would I? Absolutely. Automatic memory management alone outweights most of these issues. Sometimes Java is allowed for the contest, but my Racket code is still much concise and straight-to-the-point than what I would write in Java.

If I really had any choice of language though, I would pick between Python or something in the ML-family (csharp, F#). Scala seems fine too, maybe Ruby if I'm not too rusty to still use it.
