---
title: Learned at Jane Street - Practical functional programming and software engineering
date: 2017-01-07 00:00:02
disqus: y
---

This is the second of two blog posts on my Summer 2016 internship experience at Jane Street, focusing on the technical aspect of working with OCaml. For my experience with the company, [read the first](/2017/01/07/jane-street-thinking.html). I do not represent the company: take everything I say with a grain of salt. Other interns have their own unique experience which may differ from mine, my reconstructive memory could be telling lies, I may be rationalizing a lot, etc, etc.

I've enjoyed functional programming a lot in the past. I've only written a few significant projects using them (mainly F#, [Scheme](/2014/08/08/compiler-optimization-i.html) and [Rust](https://github.com/rudi-c/cs444-java-compiler-in-rust)) but they have all been among my most fulfilling and enlightening programming experiences.

However, in the grand scheme of things, that isn't obviously a good thing. Perl has a reputation for being fun to use and write, but producing arcane, [write-only code](https://en.wikipedia.org/wiki/Write-only_language). Functional languages have the reputation of over-complexifying simple tasks with academic ideas. While some of that reputation may be deserved, my experience working with engineering at Jane Street was not at all like that.

Quite the opposite, Jane Street's code is not only very practical, but probably the clearest I've ever had the pleasure to read and work with. I'm not big on type theory so this won't be about how to use OCaml to do Clever Things™. Rather, I'll share some aspect of software engineering that made an impression on me at Jane Street.

In fact, let's start with something that has nothing to do with OCaml at all.

Code review were immensely valuable (part 1: Iron)
--------------------------------------------------

I thought that the code reviews I got at Jane Street were rock solid, helped me learn the language and the coding conventions very quickly, and consistently helped make great improvements to the architecture of my code.

There's a historical element to code reviews at Jane Street. Due to the high-risk nature of the business, code reviews have historically been highly emphasized. In the early days, the founders would review every new line of code. However, the developers do more than just spending more time on code review. The system that was developed, Iron[^1], also has a few innovations of its own.

One major difference between Iron and other popular code review systems (e.g. Github, Phabricator) is that code reviews are written inline in the text. Rather than have a web view where you can attach comments to specific lines of code, code reviews are added directly into the code in the form of comments that start with `CR`.

```ocaml
(* CR rudi: I don't think the naming of this function is very clear *)
let foo x y = ...
```

Once the code review is addressed, the `CR` tag is changed to `XCR` and the original reviewer may delete it if they feel like the concern was addressed, otherwise changes it back to `CR`.

I initially felt that this system was rather primitive, but I soon noticed it had a few advantages. I could easily categorize and list out all the reviews based on their status, such those that were unaddressed or those whose changes were waiting for approval. Unlike Github comments, they never got lost either. Github has to figure out where to attach the comments in the code even in the face of rebase and merges, which is a non-issue for Iron.

Another aspect I liked is that since code reviews are written by editing the source file, the reviewer is free to make their own changes to the code while reviewing. This prevents holding up an urgent change from being merged because of a few nits. Instead of waiting for the reviewee to fix those nits and send the change back for approval, the reviewer can fix those nits immediately themselves. There are also types of suggestions for improvement that are difficult to communicate in words. However, they can be communicated by just implementing them and showing how it's done, which this system allows the reviewer to do. For the reviewee, this is also great for learning. Having my functions fixed for me helped me ramp on the Jane Street way of writing OCaml really quickly.

It is worth thinking about the preconditions necessary for such a code review system to be viable. In particular, I think that it requires engineers to have a lot of trust in each other, to be motivated for self improvement, and to have their egos kept in check. This system would not work if people were protective of their code.

Besides reviews on coding style, I also found that I received a lot of insightful high-level reviews on the structure of my code. In particular, I felt that the reviewers had read and understood my code, and thus were able to communicate very specific issues that addressed the root of the problems.

A lot of that credit obviously goes to the reviewers themselves. I thought both my mentors were super sharp and throughout my internship, would understand very quickly the source of my confusion on various problems and would have very clear answers or replied with another question that allowed me to immediately figure out the answer.

That being said, I also believe that there are a few aspects of OCaml itself that facilitated good code reviews. So let's move on to OCaml now, and some of my hypotheses on why OCaml functional programming might be part of the causation.

For context, here's a 100x speed intro to OCaml (to actually learn anything about it, [Real World OCaml](https://realworldocaml.org/) is not only the best OCaml resource, but probably one of the best programming books period). In the interest of not making this blog post drag on too long, the next part has to assume a fair bit of experience with programming languages :(

OCaml is...
-----------

...statically typed. Every variable and every function needs to be resolved during compilation and has a type.

...uses arrow notation for types. For example, the map function has type `~f:('a -> 'b) -> 'a list -> 'b list` . This is more than a trivial detail because it's the clearest, most composable and most compact notation I've yet seen to communicate the functions provided by an interface.

...type inferred. You don't need to explicitly write types except at a few key points. The compiler infers most of them for you, saving the need from typing a lot of boilerplate.

```ocaml
(* This function has type `int list -> int -> int list` but we didn't need to
   specify the type of `lst` or `number` or the return type. By breaking down
   the first argument into `first` and `rest`, the compiler infers that `lst`
   must be a linked list. By applying `+` to `first`, which adds two ints,
   the compiler infers that `lst` is not just a generic list, but an `int list`
*)
let addToFirstElement lst number =
match lst with
| [] -> [] (* don't do anything if the list is empty *)
| first :: rest -> (first + number) :: rest (* :: means "append to front" *)
```

...garbage collected. You don't need to be explicit about memory.

...communicates a lot of information in the types through ADTs. It's very clear what the possible states of your program are when functions return types like `Result of string | Error of NoServerFoundException.t | Timeout`

...has a clear execution model. Although OCaml is fairly high-level, arguably more than Java/C# and closer to Python, it's easy to make a fairly accurate guess as to what the code compiles down to.

...not pure, but mostly pure in practice. The default is immutability, but you don't need to use it when it's not convenient (e.g. when passing around a hash table).

...has `.ml` files for code and `.mli` files for interfaces. The interface file stores types of functions and modules (see [example](https://github.com/janestreet/incr_dom/blob/master/src/app_intf.ml)).

Code review were immensely valuable (part 2: Being explicit)
------------------------------------------------------------

I came to appreciate how OCaml's strong type system and idioms, expressed through interface files, help code reviews a lot.

Reviewing a large changeset for a large feature is difficult. Reading a large diff is hard [^2]. Understanding it is also hard, because the reviewer must build the same mental model of the program that the coder used to write it, except that the changes are presented in a flat format that mixes the high-level ideas with the implementation details. Files are unhelpfully ordered alphabetically, rather than in a logical format.

At past companies I've worked at, I would sometimes sit down with the reviewer when I wrote large features to walk them through my changes. This is helpful to make sure they understand the high level idea, and I can tell them know which changes are useful to read first, which ones are important, and which ones are trivial refactors. The more a reviewer understands the changes, the more helpful they can be. However, a code walkthrough is verbal: a lapse of attention from the reviewer and the information is gone.

If the high level ideas were naturally visible in the code, this would help reviewers immensely. And this is what interface files are great for. In many situations, they provide a high-level summary of the changes that can always be referred to. While it's a bit of extra work to write them, even the act of writing them has benefits. It encourages the [writer to design better abstractions](http://digitalfreepen.com/2015/10/12/dropbox-first-internship.html).

But interface files are useful only if they contain enough information. I found the following features and idioms of OCaml to be really helpful at conveying information in the interfaces:

- Immutability by default: If a function is pure, then all data dependencies of the function must be passed through the arguments. All inputs to the function are explicit and readable at a glance. There is also going to be a return value, which is going to communicate what the function changes/produces. OCaml isn't pure so in theory, you can't rely on knowing everything about a function. In practice, however, this isn't a problem[^3].
- Heavy use of Algebraic Data Types: This puts a lot of information in the type of a function that the reviewer can immediately see. For example:
  - `compute_value_from_list: string list -> string option` makes it clear that there is an edge case where the function may not return a result.
  - `get_file: ~path:string -> (string, IOError) Result` is a more explicit way of communicating failure cases than exceptions.
  - `apply_update: string list -> Update -> string list` with `Update` declared earlier as `type Update = Insert of string | Delete of int` makes it easy to see at a glance what the possible updates can be, better than searching for all the possible subclasses of an `Update` abstract class (which can sometimes be difficult).
- First-class lambdas used as arguments:

  `setup_listener: int Pipe -> ~handler:(int -> unit) -> unit`

  provides a little more information than the OOP equivalent

  `void setup_listener(Pipe<int> pipe, IntegerEventHandler handler)`

  because fundamentally, the class IntegerEventHandler would exist solely to provide the method `void handle(int i)`, which the functional style communicates directly without needing to create an abstract class.
- Interface files in OCaml, unlike header files in C++, are restricted to interfaces (i.e. it can't contain implementations). Consider how, for example, class declarations in C++ header files must also contain private helper functions and private fields. This minimizes clutter in the interface file.

Basically, the reviewer can spend way less time building a mental model of interacting components when all the information needed is in the same place. The less scattered throughout files and lines of code as possible, the better.

Finding out how to do things was way easier than expected
---------------------------------------------------------

One concern with non-mainstream languages and tools (i.e. most functional languages) is that documentation is harder to find online, and it's harder to figure out how to do things. Given that Jane Street uses a functional language whose use is not that prevalent, in addition to a lot of custom built in-house tools, I expected that finding information would at least be somewhat of an issue. And while there were situations where I wished I could Google something, those situations arose less often than I would have guessed.

It's not that the Jane Street codebase is particularly well documented or commented. It's quite average from my experience. However, the OCaml `mli` (interface) files come to our rescue once again. It's a form of compiling documentation: it never goes out of date and is easier to access than opening an autogenerated doc (by using "navigate to definition"). They provide a lot of information to you, exactly like how they provide a lot of information to the reviewer. The lack of clutter makes it really easy to skim through the file and see all the available utilities in a file. This is helpful to discover your toolset really quickly, in contrast to a framework like Rails where all the utilities are scattered throughout examples in documentation files.

A nice thing about OCaml's type system is that the type of functions end up feeling like nice building blocks that assemble nicely into each other[^4]. I felt that once I knew what the blocks were, the way to arrange them was generally obvious. Which is probably a good thing. I think in the ideal world, it would always be obvious how to write the correct code without having to search for examples[^5]. And while I don't think any language or coding environment allows you to do that, I certainly felt I got reasonably close with OCaml.

If it compiles, it works
------------------------

The best feeling I get with coding in a strongly typed functional language is that when the code compiles, it tends just to work.

The process of programming looks something like [write code] → [compile] → [fix compile errors] → [test code] → [fix runtime errors or bugs].

Essentially, programming in OCaml moves the time spent on fixing mistakes found at runtime to fixing mistakes found at compile time. From a personal perspective, I love this since I fundamentally enjoy writing code, and find debugging to be a bit tedious. I often even save large coding tasks (e.g. refactors) to the parts of the day when I'm getting sleepy because I can stay awake and focused if I'm typing.

From a more general perspective, if you believe the notion that the earlier a bug is caught, the less costly it is to fix, then this is probably a good tradeoff. A useful metric people care about is iteration speed. People like dynamic languages because it allows them to iterate faster. Here, I'm arguing that OCaml can _enable faster iteration speed_ than dynamic languages. There are cases where debugging fundamentally has to happen at runtime (e.g. UI programming, checking whether the visual output looks nice), where the goal should be to propagate the changes onto the screen as fast as possible. However, this is less true of say, server-side programming, where I think the goal should really be to reduce the length of the cycle taken to _produce a working program_. There, I would be more skeptical of using dynamic languages on the server side under the argument of iteration speed.

The benefits of "it compiles, it works" become especially apparent when it comes to being confident to [refactor code](https://blogs.janestreet.com/ocaml-the-ultimate-refactoring-tool/). Eliminating the fear of introducing a regression reduces a significant amount of friction towards taking on refactoring tasks. This goes a long way towards fighting technical debt.

A static analysis is not a substitute to tests. Jane Street has plenty of tests and testing tools to cover a wide range of scenarios. In addition to unit and integration tests, they also have [“unified tests/expect tests”](https://blogs.janestreet.com/testing-with-expectations/). However, tests are also not a substitute for static analysis either. In my experience, they are expensive to write, which tends to lead to incomplete coverage. They introduce a lot of boilerplate and often essentially being an expensive type check that's actually slower to run in large codebases than incremental compilation.

It's hard to nail down exactly what about the language or the coding practices allowed things to ‘just work'. I can make some conjectures using some jargon, like immutability, referential transparency, algebraic data types, etc. But even if I were to elaborate, it wouldn't communicate the feeling of how nice it is to have those things in a large codebase. It's like VIM. You understand how it improves productivity only when you use it and _feel_ the improvement. And some people won't feel it. That's ok - this blog post isn't a technical essay or a research paper, just a recollection of my experiences.

The code was very easy to understand
------------------------------------

I thought that, with a [few exceptions](https://realworldocaml.org/v1/en/html/command-line-parsing.html), the code at Jane Street could be understood both quickly and correctly. This is less trivial than it sounds.

The part about being understood **quickly** is something that everyone would agree is important and valuable, but often fails to be achieved in practice in many places.

Understandability is something that becomes important when code is complex. So first, it's worth having a good understanding of the concept of complexity. The classic "no silver bullet" makes the distinction between essential complexity and accidental complexity. From the wikipedia definition:

> Accidental complexity relates to problems which engineers create and can fix; for example, the details of writing and optimizing assembly code or the delays caused by batch processing. Essential complexity is caused by the problem to be solved, and nothing can remove it; if users want a program to do 30 different things, then those 30 things are essential and the program must do those 30 different things.

The key point is that accidental complexity can be fixed, but essential complexity can't be reduced without reducing the scope of the problem the software is trying to solve. From the paper:

> In most cases, the elements [software components] interact with each other in some nonlinear fashion, and the complexity of the whole increases much more than linearly. The complexity of software is an essential property, not an accidental one. Hence, descriptions of a software entity that abstract away its complexity often abstract away its essence.

I liked the Jane Street codebase because I felt that it was low on accidental complexity, and developers didn't get scared by essential complexity.

It was low on accidental complexity which made the code relatively quick to read. This was helped because OCaml is very idiomatic. It's a multi-paradigm language, and there are many ways to solve a problem. You can take an OOP approach or functional approach, a mutable approach or immutable approach. However, **most of the time, there is one obvious way to do it**, which is important in an environment where the number of developers is more than one. In contrast with Scala, which encourages every type of coding roughly uniformly. There are a lot of nice things about Scala, but a common complaint is that there are too many ways of doing things and the code is hard to understand as a result. OCaml is also very terse. There are very few extraneous keywords, class definitions that aren't really essential to the problem. For example, Java and C# require every function to be a method inside a class. But sometimes, in the case of static methods, what you really want conceptually is just a function. The function is the essential part of the program, the class definition is an accident.

On the other hand, there are times where a lot of information is presented on one line, and understanding it takes a bit of time. But that should be expected if the information represents the program's essential complexity. Consider:

```ocaml
    val startHttpServer:
         ~initialState: State
      -> (HttpRequest -> (String, HttpError) Result.t Deferred.t)
      -> (unit, Error.t) Result.t Deferred.t
```

There's a lot of information in this type definition for a function, but they are all essential parts of starting an HTTP server that serves strings. The server needs an initial state. The server needs a way to handle HTTP requests, some of which may return an error instead of a string. Each request is asynchronous. Starting the HTTP server itself could fail and return an error, and starting the HTTP server needs to be asynchronous.

The part about being understood **correctly** is a criteria less often brought up, but in my opinion equally important.

Developers often aim to produce readable code, but I think that might not be the correct criteria to aim for. Readable code is psychologically comfortable and looks accessible, but will lead to mistakes if it is not understood correctly. For example, [Ruby's RSpecs](https://github.com/airbnb/hypernova-ruby/blob/master/spec/request_spec.rb) aim to be read naturally like English. This looks nice but when you need to modify the specs, the order of execution of the bindings is not obvious, and it's easy to trip yourself when things don't behave how you'd expect.

Correct understanding should be the criteria to aim for. One needs to be careful if too much magic happens under the hood. [Abstractions leak](http://www.joelonsoftware.com/articles/LeakyAbstractions.html) and the hardest bugs are often the ones a level below the level of abstraction you usually work in.

In that sense, OCaml is nice because despite having a fairly high level of abstraction, it's easy to get a sense of what the code compiles to, and Real World OCaml does a really good job at documenting what you need to know about the runtime (the "Real World" part of the title isn't just for show).

But it's not a magic bullet
---------------------------

That being said, OCaml, or functional programming, is not a magic bullet. If I claimed otherwise, you should probably call bullshit.

We had a two day event at Jane Street where we built a trading bot on a simulated exchange. Our goal was to get points by making a profit, and points would start counting as early as an hour into the contest, which emphasized speed. Almost nobody chose to use OCaml, Python was by far the majority language among both traders and developers. I also chose to use Python - I felt like I could get something running more quickly, since every minute counted. And we did indeed have our bot ready to trade as the "markets" opened. Of course, this carried risks: a coding mistake cost me and my teammate over an hour worth of points in just 5 minutes (not unlike what happened to Knight Capital actually). If I were to do this again, I would still probably pick Python, but it's an interesting illustration of the tradeoffs.

The other problem is that one that always come up - as good as a language is by itself, there's still the issue of ecosystem. Jane Street has open sourced a lot of its libraries, but a single company cannot create a whole ecosystem. There's not an obvious option to quickly create a web server in OCaml for example. And as great as my coding experience was inside Jane Street, setting up that environment locally (with auto-compilation, go-to definitions, etc) is quite hard, even if the pieces are available. It's definitely far too much friction for passerby to get started on a new project compared to most other languages.

Further reading
---------------

[Hear about why Jane Street uses OCaml from the man who introduced it himself](https://blogs.janestreet.com/why-ocaml/)

OCaml has a generational garbage collector with incremental collection for the large heap. [Jane Street has worked on it a lot](https://blogs.janestreet.com/building-a-lower-latency-gc/) in order to minimize the length of GC pauses, especially on the tail end, given that they have a real-time system handling huge amounts of data (meaning it produces huge amounts of garbage). Whether this is advantageous to you depends a lot on your use case. However, the interesting implication is that OCaml could actually be one of the more viable options in applications where GC pauses are a problem (e.g. apps, games).

There's no official engineering values, but [these ramblings of one engineer](https://blogs.janestreet.com/13-virtues/) do illustrate the engineering values decently well.

[Coding with interfaces as a strategy](https://blogs.janestreet.com/simple-top-down-development-in-ocaml/). I've yet to learn to do that consistently...

Or generally, read their blog. It has tons of good stuff, I promise.

----------------------------------

<small>*Thanks to Bai Li, Corwin de Boor, Jason Xiong, Leila Clark, Manu Goyal, Saahil Mehta, Shida Li for comments & corrections.*</small>

----------------------------------

[^1]: To read more about Iron, see
    https://blogs.janestreet.com/designing-a-code-review-tool-part-1/
    https://blogs.janestreet.com/designing-a-code-review-tool-part-2-patches-or-diffs/
    https://blogs.janestreet.com/patch-review-vs-diff-review-revisited/
    https://blogs.janestreet.com/code-review-that-isnt-boring/
    https://blogs.janestreet.com/scrutinizing-your-code-in-style/
    https://blogs.janestreet.com/ironing-out-your-release-process/

[^2]: A code reviewer must, in broad terms, go through the following steps:
    1. Read the code
    2. Understand the code
    3. Find a better alternative if one exists
    4. Verbalize/communicate that alternative

    All of those steps are hard. It might not be obvious that reading the code is necessarily a hard step compared to understanding it, but it actually is, from a psychological perspective. Not everyone finds reading code very fun. Personally, my attention span when reading anything, code or not, is not very high. In cases where the information density is low (such as a lot of fairly straightforward business logic), my eyes start glazing over quite quickly, and my reading becomes increasingly superficial. I think this is not uncommon among developers.

[^3]: The lack of pureness isn't a problem in practice because at Jane Street:
    - People are trained to write immutable code as much as possible. Therefore, when the function produces side effects, it is well-understood that it should be documented.
    - A function with return type `unit` (void) is understood to have side effects, and generally functions with side effects do return `unit` .
    - If a function that takes a mutable data structure as an argument it is understood that it might have side effects. For example, passing a hashtable throughout nested helper functions.
    - Finally, in an internal codebase, either the function is simple enough that its implementation is trivial to infer and it can assumed that it won't have side effects, or complicated enough that it's not possible to communicate everything about the function in its type, and you'd take a look at its implementation to make sure to understand what it does. It should be very rare that you both used a function without taking a look at its implementation _and_ assumed incorrectly that it was pure.

[^4]: It's a bit like playing with trigonometric identities. You have some start and want to go to some finish using some transformation rules.

[^5]: It's a commonly accepted meme is that programming is about searching stuff on StackOverflow all the time. I also internalized it for the longest time because it's correct in the sense that searching for things can be better than memorizing, which takes undue cognitive space. However, searching stuff on Google (or in a codebase) is not writing code.
