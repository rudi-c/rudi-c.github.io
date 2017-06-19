---
title: Compiler optimization contest (Part I) - In the Zone
disqus: y
---

"Foundations of Sequential Programs" is a second-year course at University of Waterloo, which teaches how high-level imperative programs are understood, compiled and ultimately translated into machine code. The course begins with an introduction to writing in MIPS assembly, assemblers and linkers. Then, it moves on the parsers and ends with compiling a (very small) subset of C++.

The best part of the course is the compiler optimization contest that concludes it. The goal is to extend our compiler to produce the smallest machine code for a hidden input program (it is much easier to evaluate which code is smallest than which code is fastest). This post is a log (written after the contest) of how I got 2nd place.

*Note : This contest happens every time the course is offered, but I am not too concerned about publicizing my solution. The core of it (SSA + register allocation) is difficult enough that anyone capable of implementing it should be able to achieve a high score in the contest without my help.*

The language
------------

To give some more context, the language we are trying to compile is, for the most part, a valid C++ program. A sample program might look like the one below.

```cpp
int sumArray(int* a, int b) {
    int count = 0;
    int sum = 0;
    while (count < b) {
        sum = sum + a[count];
        count = count + 1;
    }
    return sum;
}

// This program is a convoluted way of printing a * b;
int wain(int a, int b) {
    int array = NULL;
    int sum = 0;
    int count = 0;
    int sumptr = NULL;
    sumptr = &sum;
    if (a > 0) {
        array = new int[a];
        while (count < a) {
            array[count] = b;
            count = count + 1;
        }
        *sumptr = sumArray(array, a);
        delete [] array;
    } else {}
    println(sum);
    return 0;
}
```

Notice the language has pointers, memory allocation, procedures, and a number of restrictions. All declarations must appear in the beginning of the procedure. Every procedure returns an int and can only call previously declared procedures (recursion is allowed, mutual recursion isn't). If statements always have an else block. There are only two types : integers and integer pointers.

The language is compiled to 32-bit MIPS, giving us 32 registers to work with.

Before the contest
------------------

In all of our assignments for this course, we have the choice between using C, C++ or Racket (a dialect of Scheme/Lisp taught in first year). I went with Racket.

The choice was easy: lately, I have been finding programming in classical C-style imperative languages (Java/C#/C++) less exciting than it used to be. I don't feel I improve very much by writing code in those languages anymore. Like going to the gym and lifting 15lb weights when I could be lifting 25lb, I found the need for some heavier weight to work out my mental muscles. Functional Programming (FP) requires more thinking upfront, but leads to concise code that requires significantly less debugging. Real-world constraints (ecosystem, support on particular mobile platforms, jobs, etc) make opportunities to use functional languages rare, so I try to use them whenever I do get the chance.

Compilers are the kind of programs where using FP makes a lot of sense. They inherently require a great deal of recursion and tree traversal, for which languages like Racket are optimized.

The compiler ultimately ended up being the largest functional program I have ever written - I reflect on lessons learned from this experience in [Part II](/2014/08/08/compiler-optimization-ii.html).

A previous assignment consisted of implementing symbol tables and type checking, so I already had the infrastructure needed to work with the [parse tree](http://en.wikipedia.org/wiki/Parse_tree). In particular, I had already written code to construct an [abstract syntax tree (AST)](http://en.wikipedia.org/wiki/Abstract_syntax_tree) from the parse tree (also known as concrete syntax tree). The difference is that parse tree is a direct representation of the grammar rules and contains a lot of cruft such as parentheses and brackets, e.g.

```
statement → IF LPAREN test RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE
```

Whereas the AST is a much more lightweight representation, ultimately represented by a few structs holding only relevant data.

```racket
(struct proc (id params dcls stmts return))
(struct stmt ())
(struct stmt-set stmt (lvalue expr))
(struct stmt-if stmt (test true-stmts false-stmts))
(struct stmt-while stmt (test stmts))
(struct stmt-print stmt (expr))
(struct stmt-delete stmt (expr))
(struct param (id type))
(struct dcl (id type val))
(struct expr (type))
(struct expr-binop expr (op e1 e2))
(struct expr-unary expr (op expr))
(struct expr-id expr (id))
(struct expr-const expr (val))
(struct expr-funcall expr (id args))
(struct test (op e1 e2))
```

While the assignments did not require the use of an AST, it makes life much easier.


July 6th-July 11th
------------------
*preparation*

In anticipation for the contest, I made some preliminary research on compiler optimization. Wikipedia has a [decent](http://en.wikipedia.org/wiki/Static_single_assignment_form) [selection](http://en.wikipedia.org/wiki/Constant_propagation) [of](http://en.wikipedia.org/wiki/Dead_code_elimination) [articles](http://en.wikipedia.org/wiki/Global_value_numbering) on optimization techniques. Many of them are fairly obvious (e.g. removing unused code), but it is helpful to see them clearly written down. I am particularly intrigued by Single Static Assignment which is in an intermediate form for the program that helps with the implementation of many optimization techniques. Since I only have three weeks to write the compiler, I decided not to dig into academic literature - I will most likely run out of time before I run out of ideas.

The technique for code generation shown in class is based around the idea of recursing through the parse tree and is very simple, in that it only uses a fixed set of registers and avoids a lot of edge cases. However, it is terribly, terribly inefficient. The MIPS assembly code to add two variables corresponding to the grammar rule (`expr → expr1 PLUS expr2`) would look like

```
// By convention, $30 is the stack pointer
code(expr) =
    sw $3, -4($30)      // push $3 to the stack
    code(expr1)         // returns the result of expr1 in $3 (register 3)
    sub $30, $30, $4    // decrement stack - $4 always contains the value 4
    code(expr2)         // returns the result of expr2 in $3
    add $30, $30, $4    // increment stack
    lw $5, -4($30)      // places result of expr1 in $5
    add $3, $5, $3      // computes the sum and returns in $3
```

This technique is nice for pedagogical purposes. It works. Every variable is stored on the stack: register `$3` is, by convention, the register for return values and `$5` is the register for a temporary result when dealing with binary operations.

However, it is clear that this is very wasteful. For example, if we knew the result of expr1 and expr2 were in two registers, say 16 and 17, then we could simply have written

```
add $3, $16, $17
```

In other words, the solution shown in class uses as much as *five times* more instructions than needed. That's insane, and shows that there is *a lot* of room for improvement. I like efficient code, so I couldn't even bring myself to write such an inefficient compiler.

As such, I decided to write the compiler directly with register allocation, rather than starting with the solution shown in class and iterating from there.


July 12th (Sat) - July 13th (Sunday)
------------------------------------
*SSA and register allocation*

The compiler is split into three assignments over three weeks. The first requires implementing support for declarations, assignment and printing, expressions involving arithmetic operations, while loops and if statements.

I began during the weekend by converting the abstract syntax tree into an intermediate representation, single static assignment. The idea is to convert code that looks like :

```cpp
x = 0;
x = x * 2 + 1;
```

into

```cpp
x1 = 0;
temp1 = x1 * 2;
x2 = temp1 + 1;
```

Such that each variable is assigned exactly once (incrementing a counter whenever a variable is reassigned, creating a "new" variable), and expressions are flattened to have a closer correspondence with assembly instructions via the use of temporary variables. In this form, each variable is immutable - they only ever represent a single value. This helps make subsequent analysis much easier.

Generating these SSA statements for assignment and arithmetic expressions is fairly straightforward and only took me a few hours. The intermediate results are stored in a few structs.

```racket
(struct ssa-binop (op target var1 var2))
(struct ssa-unary (op target var))
(struct ssa-print (var))
(struct ssa-return (var))
```

The harder part is register allocation. I began with a timetable of the first and last occurrence of each variable as it appears - i.e., the lifespan. When a variable is assigned (recall that in SSA, this only happens once for each variable), a mapping of that variable to a register is added to the symbol table. If there are no more free registers, a variable needs to be pushed to a virtual register (e.g. $32). Variables might need to be loaded from virtual registers when they are read. When a variable is seen for the last time, it can be removed from the symbol table, freeing up a register.

This is fairly straightforward, but quite time consuming to implement. I handled all of this at the same time, which involved a fair amount of repetitive code that needed to push and pop registers to virtual registers and update the symbol table in exactly the right order.

It also took a lot of debugging to make sure variables are always assigned to valid registers and it ended up with somewhat brittle code. If I were to redo register allocation, I would consider allowing any operations on virtual registers (e.g. add $40, $11, $89) and dealing push/pop in a separate pass. By the time my compiler could handle all expressions and assignments, I was already well into Sunday.

Dealing with branches is also challenging. Code such as

```cpp
x = 0;
if (y > 0) {
    x = x + 1;
} else {
    x = x + 2;
}
x = x + 1;
```

Translates into what, in SSA form?

```cpp
x1 = 0;
if (y > 0) {
    x2 = x1 + 1;
} else {
    x3 = x2 + 2;
}
x? = ???
```

To deal with this, phi functions are typically introduced.

```cpp
x4 = phi(x2, x3)
```

Which represents the "merging" of the same variable from two different branches while meeting the constraint that `x1, x2, x3, x4` represent fixed distincts value.

Typically, SSA code containing branches is generated by first creating a [control flow graph](http://en.wikipedia.org/wiki/Control_flow_graph) and determining the relevant phi functions using dominance frontiers. This handles the general case where labels and gotos allow jumping into any point in the code. However, I felt like that would be too much work since our language only specifies if branches and while loops.

July 14th (Mon) - July 16th (Wed)
---------------------------------
*still stuck on register allocation and branches*

Implementing branches took considerably more time than expected. While phi functions are simple to understand conceptually, figuring out what to do with them during register allocation was more challenging.

Most resources (Wikipedia, lecture slides from other universities, etc) explain how to generate SSA, but not how to deal with SSA during register allocation. It did not appear too hard at first but I did not yet have a clear picture of how the various edge cases would influence the requirements. So rather than starting with a working algorithm design upfront and implementing it, which is everyone's ideal scenario, I ended up writing code, bumping into an edge case, fixing the edge case using a ad-hoc solution, bumping into another edge case, repeatedly. For example, after I finally had a solution for while loops, I couldn't handle nested while loops. After I got that working, loops would occasionally fail when I need to spill registers, due to the complexity of my register allocation.

I eventually managed to get while loops working. Unfortunately, that took until 4 AM on Wednesday - I did not succeed in completing if statements. The assignment was due on 5 PM on the same day, so after the day's classes, I implemented the class solution from 3:00 to 4:30 and passed all the automated tests. The solution I submitted was a 100 line file, less than 10x the optimized compiler I had so far.

Despite these difficulties, implementing the optimized compiler was already a lot of fun. In recent months, I found myself having difficulty finding a sufficiently interesting problem that I could get into and focus on for a long time (when I don't, I tend to procrastinate, checking emails/facebook every 15 minutes). This is a problem, because most of my best work happened while I was fully focused - in "The Zone", so to speak. Being in The Zone feels like transforming into a super saiyan, where I get to use all my programming abilities to the fullest extent.

<center><img src="/images/2014/08/super-saiyan.jpg" width="300"/><br/>Hell yeah</center>


July 19th (Sat) - July 20th (Sun)
---------------------------------
*finish branches, implement pointers and procedures*

The following weekend, I continued working on implementing branches, and managed to get it working by Sunday. That was exhausting but fun - I basically (re)invented a register allocation in a few days.

The next assignment is implementing pointers.

Pointers can be tricky. Allocating and freeing are fairly straightforward - it is simply a matter of calling a procedure of one parameter. So are pointer arithmetics. On the other hand, what about pointers to stack variables? If we have code such as:

```cpp
int a = 0;
int b = 0;
int* ptr = NULL;
if (x == 0) {
    ptr = &a;
} else {
    ptr = &b;
}
*ptr = 1;
```

Then both `a` and `b` need to be stored in memory on the stack (or at the very least, have a corresponding stack address) as we can't take the address of a register. However, do they always need to be on the stack? Is it possible to know whether a pointer points to a stack variable or a heap location?

There is an interesting paper that [extends SSA numbering](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.17.1802) (C. Lapkowski, 1996) that deal with analysis of pointers in the context of SSA. The method presented is quite understandable, but it was not clear that the time investment to implement it would pay off for the contest.

For the sake of getting something working, I chose a simpler approach, which is an initial pass over the AST to make a list of all local variables whose address gets taken (&'ed) and store them on the stack. They are loaded from the stack whenever they are read, and stored to stack whenever they are written.

Note that pointer arithmetics on stack variables is undefined, such as in the code below:

```cpp
int a = 0;
int b = 1;
int* ptr = &a;
println(*(ptr + 1));
```

While some compilers might print the value '1', the behavior is undefined, because the language does not specify any requirements for the ordering of local variables on the stack. This is good - as our professor Brad Lushman says, "undefined behavior is your best friend when writing a compiler - you can do whatever you want".

After finishing pointers, I moved on to procedures. This is actually closely related to pointers, because both are intricately linked to the layout of the stack. In fact, my procedure stack frames ended up being quite complicated.

```
Format of the stack frame (grows from high addresses to low addresses):
n ('param) = number of parameters
m ('saved) = number of saved registers
  ('$31)   = for storing $31 when calling a function
p ('local) = number of local variables that need to be on stack
q ('temps) = number of temporaries = (max reg encountered - 31)
  ('total) = n + m + 1 + p + q
top of the stack frame
4 * (0) param 1
4 * (1) param 2
4 * ...
4 * (n-1) param n
4 * (n)   saved reg 1
4 * (n+1) saved reg 2
4 * ...
4 * (n+m-1) saved reg m
4 * (n+m)   for storing $31 when calling a function
4 * (n+m+1) local variable 1
4 * (n+m+2) local variable 2
4 * ...
4 * (n+m+p) local variable p
4 * (n+m+p+1) $32
4 * (n+m+p+2) $33
4 * ...
4 * (n+m+p+q) $max-encountered
Bottom of the stack frame (current $30)
```

The top of the stack frame needs to contain procedure parameters. This is because parameters are written to the stack frame by the caller, whose frame is adjacent to the callee's stack frame. To make my code more consistent, parameters are loaded into registers at the beginning of the procedure. The parameters on the stack are then never accessed again, except through pointer operations.

When a procedure is called, it needs to save all the registers that it might use, otherwise it might end up clobbering the registers of the caller. I have a special slot to store the register `$31`, which by convention, contains the return value of any procedure (including wain). `$31` is different from other registers, in that it needs to be saved by the caller (otherwise, by the time we call the procedure, it will already be clobbered). Therefore, I set aside a slot in the stack frame to store `$31` when calling a procedure.

Then, I need slots to store some local variable. While most local variables will remain in register, those whose address gets taken (&'ed) need to be on the stack.

Finally, I need a few more slots to allow for register spilling.

There are still inefficiencies in my calling convention. When I evaluate procedure parameters (i.e. `foo(expr1, expr2, ..., exprn)`), the result of each expression is not stored immediately on the stack. This avoids function calls inside the parameter expression from clobbering parameters of the outer function call being written to the stack, but it can involve extra instructions (the registers containing the early parameters might need to moved onto and back from the stack during spilling, if the later parameters expressions require a lot of registers).

Implementing pointers and procedures went fairly smoothly. It seems that after doing a lot of upfront work with SSA and register allocation, the pace accelerates.

Unfortunately, I can't pass one of the assignment's automated tests.


July 21st (Mon)
---------------
*debugging*

That one test case seems to elude me. I already have a solid testing framework set up where I used Racket's unit testing framework to make `(system* ...) calls` to run the compiler, assembler, linker and simulator, but my tests don't seem to be catching the bug.

To find the bug, I created some pretty nasty stress tests, including a call to a function of 32 parameters where each parameter expression is another call to a function of 32 parameters. But to no avail.

A few people have already submitted their program to the bonus (which contains the code that our compiler needs to compile while producing the shortest assembly). To get bonus marks, the output of the compiler needs to be less than 180,000 bytes. A few people have obtained a score of 200,000 bytes (as seen on the leaderboard), suggesting that an straight implementation of the solution shown in class will yield ~200,000 bytes.


July 22nd (Tue)
---------------
*debugging with black-box testing*

After two days, I still couldn't find what causes my compiler to fail the automated assignment tests (the particular one I am failing is a blind test, meaning that I can't see what it is), despite correcting a variety of other mistakes along the way. Finally, I decided to resort to "extreme" measures. I disabled optimizations in my compiler in a binary search manner and kept testing the partial compiler at every step. This allowed me to narrow down on the problem.

Finally, as expected, the source of the failure is a dumb mistake - I forgot to check for &'ed variables in println statements. Duh!

After fixing the bug, I submitted my compiler for automated testing again and obtained a score of **109,876 bytes**, which is a bit over half the "baseline" score. This put me in second place.

After two weeks, I finally have a working compiler.


July 23rd (Wed)
---------------
*down to 3rd*

Some person that I don't know submits a compiler producing 90k bytes, putting me in 3rd place. That's fine, I barely even got started.


July 24th (Thu) - July 25th (Fri)
---------------------------------
*constant folding*

This is where the fun begin - I can begin implementing optimization. Surely, writing the compiler to support register allocation was already a large (if not largest) optimization I could do, but there is still PLENTY to be done.

The first technique I wanted to begin with is [Constant Folding](http://en.wikipedia.org/wiki/Constant_folding). The idea is that code such as

```cpp
int x = 60 * 60 * 24 * 7 * 365;
```

can easily be reduced by the compiler down to

```cpp
int x = 220752000;
```

A basic implementation of this optimization is straightforward. Whenever we have an AST node of the form `expr1 op expr2`, where `expr1` and `expr2` are constants, the compiler can reduce this node to a leaf node.

But we can do better can't we?

The above technique would fail in an expression such as

```cpp
int x = (((x + 1) + 1) + 1) + 1;
```

which does not contain any node where both children are constants. However, simple visual inspection suggests that we should be able to deal with this.

The approach I took is to flatten the expression tree for addition and multiplication, which allows combining constants together. In prefix notation, this would lead to reductions as such :

```racket
(+ (+ a 1) (+ b 2))
=> (+ a 1 b 2)
=> (+ a b 1 2)
=> (+ a b 3)
```

For subtraction, I create a special wrapper "minus", that allows me to combine addition and subtraction.

```racket
(- (+ c 4) (- 3 (- c d)))
=> (+ (+ c 4) (minus (- 3 (- c d))))
=> (+ (+ c 4) (+ (minus 3) (minus (- c d))))
=> (+ (+ c 4) (+ -3 (+ (minus c) (minus d))))
=> (- (+ c 4 -3) (+ c d))
=> (- (+ 4 -3) (+ d))
=> (- (+ 4 -3) d)
```

In other words, separating positive and negative terms into two groups. This also cancelling identifiers that appear on both sides (`c`, in the above example).

Not every term will necessarily be an integer. Some could be pointers which invalidates certain reductions. For example, int\* - int is defined, but not int - int\*. For addition (without subtraction), we don't actually need to do anything. A flattened tree of nested addition will always contain at most one int* term, otherwise it would not pass the type checker. For pointer subtraction, we simply avoid flattening the parse tree at that node.

There are other arithmetic properties that allow further reductions. For example,

```racket
(+ x 0) => x
(* x 1) => x
(* x 0) => 0
```

However, note that multiplication by zero is a little tricky. If x is an expression containing a function call, the function call could have a side effect such as printing. In that case, removing the function call changes the behavior of the program.

Then there is division by zero, which we have no choice but to leave there and let the program crash at runtime.

```racket
(/ x 0) => (/ x 0)
```

Implementing constant folding wasn't too hard, summing up to a ~200 line Racket file. In fact, unlike the rest of the compiler, it was a clean, pure functional implementation. I did, however, struggle with an infinite loop bug. Again, it was a really dumb bug, which I somehow failed to catch (the student #1 on the leaderboard helped me find it after a bit of code review).

I expected the test program to contain a massive amount of constants, since this was the first optimization discussed in class. Unfortunately, it did not reduce the size of my code significantly. My score only went down to **105,256** bytes.

A constant normally needs to be loaded using two instructions as follows (lis is an instruction made up by the instructors, which loads the next word into a register and skips that word):

```
lis $3 // load 4 into $3
.word 4
```

However, by convention, we already use some registers for specific values. Namely, `$0` contains 0 (this is true on any MIPS architecture), `$4` contains 4, `$5` contains 1. Making use of those registers reduced the output size to **101,144 bytes**.


July 26th (Sat)
---------------
*dead code elimination*

Up until now, every time I made a call to a procedure (including `new/delete/print`), I would store `$31` into its designated slot, and load it back after the procedure returned. This is unnecessary, given that I could load and store $31 only once per procedure, and only if the procedure calls another procedure. This simple optimization gave a significant boost of 3k, getting me down to **98,484 bytes**.

[Dead code elimination](http://en.wikipedia.org/wiki/Dead_code_elimination) is an important one, and is a simple graph reachability problem solved by going through the SSA instructions in reverse order. Instructions such as `println(x);` or `return x;` mark the variable `x` as "needed", and a variable `y` is needed if it appears on the RHS of an assignment where `x` is the LHS. In the case of branches, it is assumed that all the branches are executed. This gave a considerable drop, down to **82,240 bytes**. Now I'm back in 2nd place.

Can't work on the compiler more this weekend though. I have three assignments due next week (the last day of classes) that I kept pushing back to work on the compiler contest.


July 27th (Sun) - July 28th (Mon)
---------------------------------
*OS, Numerical, constants table, copy propagation*

I finished the operating systems assignment (CS 350) on Sunday, which involved implementing virtual memory, and the numerical computation assignment (CS 370) on Monday. Honestly, I am not sure why people make such a big deal about OS being one of the hardest classes, but I will leave that for a later blog post.

During class, I also got time to implement constants table, which is easy enough that I can code it while (mostly) paying attention to the lecture. Recall that we need two instructions to load a constant. However, if we load the same constant multiple times, it may be possible to do it more efficiently. Suppose I needed to load the constant '10' 5 times in the program.

```
lis $8
.word 10
...
lis $19
.word 10
...
lis $6
.word 10
...
lis $7
.word 10
...
lis $15
.word 10
```

It would be nice if, somewhere in the beginning of the program, we had a constants table

```
beq $0, $0, constants_end   ; skip the constants table
constants_begin:
    .word 10                ; offset 0
constants_end:
lis $29
.word constants_begin       ; store the location of the constants table
```

so that subsequent accesses to that constant can be done in a single instruction

```
lw $8, 0($29)
...
lw $19, 0($29)
...
lw $6, 0($29)
...
lw $7, 0($29)
...
lw $15, 0($29)
```

by storing the location of the constants table in a fixed register (here, `$29`).

This optimization saved a humble 2k bytes, down to **80,836 bytes**.

Another easy optimization is [Copy Propagation](http://en.wikipedia.org/wiki/Copy_propagation). Given code involving the immediate assignment of one variable to another

```cpp
x1 = a1;
x2 = x1 + b1;
```

can be reduced to

```cpp
x2 = a1 + b1;
```

by substituting all instances of `x1` with `a1`. However, my ad-hoc implementation of SSA and phi functions does not allow certain cases of copy propagation to spread into branches, so this optimization is only half functional. It would be too much work at this point to go back and fix it, and probably not worth the effort. I still get a reasonable reduction, down to **79,928 bytes**.

July 29th
---------
*constant propagation, rank ordering, dead procedures*

Now that I finally finished all my assignments for the term (after working until 2 AM twice in a row - mostly because I started the assignments fairly late to begin with), I can focus on the compiler contest!

Another major optimization I have not yet implemented is constant propagation. This differs from constant folding in that it works across statements, rather than just on a single expression.

```cpp
// This is handled by constant folding.
x = ((y + 1) + 1) + 1) + 2;
// This is handled by constant propagation.
a = 0;
b = 1;
c = 2;
d = a + b;
e = d + c; // simplified to e = 3
return x + e;
```

Dead code elimination, which we implemented earlier, is necessary for constant propagation to work well. For example, the above code would have been reduced to

```cpp
x = y + 5;
a = 0;
b = 1;
c = 2;
d = 1;
e = 3;
return x + 3;
```

Which does not reduce the size of the program. However, at this point, only the first and last statement are still useful - the rest are cleaned up by dead code elimination.

This gave me more than twice as much gain as constant folding, down to **71,944 bytes**.

Constant propagation can also be extended to branches. Indeed, if we encounter

```cpp
if (1 < 2) {
    ...
} else {
    ...
}
```

Then all the statements in one of the branches can be removed. While loops that always evaluate to false can also be removed. This also gave substantial gains of 11k, down to **60,956 bytes**. This is neat, our output assembly is now more than 3x smaller than the baseline output.

Another optimization I wanted to try is rank reordering. Suppose we have an expression of the form.

```
expr -> expr1 + expr2
```

Does it matter whether we evaluate `expr1` first, or `expr2` first? It turns out that it does. Suppose evaluating `expr1` requires 2 registers and `expr2` requires 3 registers. If we evaluate `expr1` first, we need to store the result in a register before evaluating `expr2`. Then, `expr2` requires 3 more registers. Thus, we use a total of 4 registers.

However, if we evaluate `expr2` first, we use three registers and then store the result in one of those registers. The other two can be used to evaluate `expr1`. Thus, we use a total of 3 registers. It is always better to evaluate the subexpression that uses the most registers first.

Apparently, this optimization gave substantial gains to a lot of people in past offerings of this course. However, I suppose that because I already had full register allocation implemented, I only got a tiny gain of 24 bytes, down to **60,932 bytes**. I still hoped for more though, using less registers should imply less instructions to handle spilling.

Another optimization I had not done yet was to remove unused procedures. That only saved a few bytes also - it seems only 1-2 procedures were not used. Down to **60,748 bytes**.

July 30th
---------
*last day, global value numbering, load/store improvements, instruction reordering*

This is the last day for the contest. I am sitting quite solidly in 2nd place, but still a distance away from 1st, whose compiler outputs 54,316 bytes.

A cool technique to eliminate redundant code is [Global Value Numbering (GVN)](http://en.wikipedia.org/wiki/Global_value_numbering). The idea is to assign each variable and expression (of 1 node) a number, which represents an identifier of a possible value at some point during execution. If we have

```cpp
c = x * y;
z = x;
d = z * y;
e = c + d;
```

then we can assign `x`, `y` the "numbers" 1 and 2. Then, `c` can be assigned the "number" 3, which represents the product of the "numbers" 1 and 2. The variable `z` is assigned "number" 1 since it is assigned `x` directly. Then, note that `z * y` represents the product of the "numbers" 1 and 2 again, so `d` can be assigned the "number" 3.

Thus, after copy propagation and dead code elimination, global value numbering reduces the above to :

```cpp
c = x * y;
e = c + c;
```

This optimization is similar to [Common Subexpression Elimination (CSE)](http://en.wikipedia.org/wiki/Common_subexpression_elimination). According to wikipedia, GVN handles some cases that CSE can't (such as the above, where the expressions on the RHS are different) but can't handle some cases that CSE can. I opted to implement GVN over CSE as it requires less work given that my program is already in SSA form.

Implementing GVN got a small reduction, down to **58,428 bytes**.

Next, I wanted to do something about my local variables. My current compiler would compile the return statement of

```cpp
int a = 5;
int* ptr = NULL;
ptr = &a;
return a + a;
```

down to

```
lw $6, offset($30)
lw $7, offset($30) // redundant
add $3, $6, $7
````

Which contains redundant instructions. The variable `a` needs to be loaded from the stack because a pointer points to it, but it doesn't need to be loaded twice in a row if no memory write occurs between the two memory reads.

So I removed all the redundant memory reads and writes. Unfortunately, this did not reduce the output size *at all*. I suppose there aren't many test cases with stack references. Bummer.

At this point, I only had a few hours left and 4,000 bytes to match the 1st place score. I could still think of a lot of little optimizations, but a dozen optimizations that save 100-200 bytes each wouldn't be sufficient. I needed something better. But what? I had already implemented most major optimizations.

For inspiration, I went back into the assembly generated by compiling some of my larger test programs. One area that I found inefficient was in regards to register spilling. It would occasionally happen that a variable used in the very beginning of the program wouldn't be used until the very end. For example, suppose we had a procedure where

```cpp
x = a + b;
...
5000 instructions not involving x, but involving a, b
...
return x + y;
```

Then the variable `x` takes up a register for most of the procedure, so the rest of the procedure needs to spill variables more often. It would be nice if the procedure could be rewritten as

```cpp
5000 instructions not involving x, but involving a, b
...
x = a + b;
return x + y;
```

which suggests that reordering instructions to appear as late as possible could be beneficial, keeping in mind that certain instructions can't be moved, notably memory operations and printing.

I initially thought that this would be too hard to implement in the three hours that I had left (it's very easy to mess up instruction reordering) but it turned out to be fairly easy. Implicitly, all this optimization does is a topological sort on instructions implemented in a specific way.

This gave a reasonable improvement, bringing my score down to **57,760 bytes**. However, that was still not less than 54k, and thus, I stayed in 2nd place until the end of the contest at midnight.

Final stats (`wc -l *.rkt *.ss`)

```
   198 wlp4gen.ss
    33 analysis.rkt
   125 analyze-ast.rkt
    72 analyze-subtree.rkt
   230 constant-folding.rkt
   203 copy-constant-propagate.rkt
   140 dead-code-elim.rkt
    43 gen-code.rkt
   389 gen-mips.rkt
   502 gen-ssa.rkt
   157 gvn.rkt
    66 load-store-reduce.rkt
    98 print-ssa.rkt
   258 read-ast.rkt
   713 reg-alloc.rkt
   231 reorder.rkt
    84 ssa-structs.rkt
   874 test.rkt
    79 utils.rkt
  4495 total
```


Final scoreboard (top 10)
-------------------------

Position | ID  | Size  | Person
:-------:| --- | ----- | ---
1  | 11382 | 54316  | [Geoffry Song](https://github.com/goffrie)
2  | 11365 | 57760  | me
3  | 11735 | 88372  | Liang Chen
4  | 11487 | 90916  | [Shane Creighton-Young](https://github.com/srcreigh)
5  | 11371 | 104532 |
6  | 11351 | 106432 |
7  | 11391 | 127964 |
8  | 11379 | 141644 |
9  | 11488 | 142156 |
10 | 11370 | 153548 |

A few closing comments on the contest :

* This contest was primarily about free time and coding speed. There are tons of little optimization that I didn't have time to do. Although some students might find SSA and register allocation to be black magic, there's nothing particularly fancy about any of the technique I used (in this context, I define fancy as "found in academic literature" in contrast to "found on Wikipedia").
* Although a lot of work was required upfront to implement SSA (I didn't make it for the first assignment deadline!), subsequent optimization where a lot easier once I had it. It paid to skip the class solution entirely.
* Using Racket was a significant advantage, with automatic memory management, pattern matching and easier to use built-in library than C++. I estimate that the equivalent C++ compiler would have been somewhere around 10,000 lines.
* Geoffry (#1), myself (#2) and Shane (#4) all used Racket. I have no idea about Liang. It is not clear which way the correlation goes (probably both ways).
* The result of the contest was fairly predictable. I never expected to beat Geoffry. He's just a much better programmer than I am. While vastly different in implementation, our solution were similar. However, if he can code twice as fast, he can implement twice as many optimization. That I could get within 5% of his score is a satisfactory achievement as far as I'm concerned.
* Shane, the runner-up did a remarkable job to finding simple optimizations (e.g. rank ordering) that gave massive code size reductions in the last few days. Unfortunately, he ran out of time, but another hour or two and he could have made it to Top 3.
* Unfortunately, not everyone takes this course at the same time. In particular, the [one person with whom I would have had a really tight race](http://www.lishid.com/) did not take the course had already taken the course a term earlier, due to having a different course sequence.
* Very few people participated in the contest, which was somewhat disappointing.
* This contest was enjoyable - in fact, it is the only assignment I've truly enjoyed for the whole term. I've been able to put 100% of my abilities into the contest, something which I have had difficulty doing in the last two years as my standards for "challenging" keeps increasing.
* Lessons learned from Racket in the [next post](/2014/08/08/compiler-optimization-ii.html)
