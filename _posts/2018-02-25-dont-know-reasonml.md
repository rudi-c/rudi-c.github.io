---
title: I don't know ReasonML
date: 2018-02-25 12:00:01
disqus: y
---

This blog post, "I don't know ReasonML" isn't really a blog post but more of an experiment. I'll put this as a disclaimer upfront: it's not meant to be well-written. My recent side project is to port a Typescript project into [ReasonML](https://reasonml.github.io/) for fun. I've never used ReasonML before and it's a new language. So inevitably, I run into tons of small issues that take me an hour to figure out because there isn't much documentation for them online.

I'm also keeping a journal of my progress as I go along which is sometimes useful if I run into an issue a second time and forget how I solved it the first time. The thought then occurred to me: "shouldn't I share these findings to save other people time?". Writing a blog post for each of these would be nice, but quality research & writing requires a lot of effort, so I wouldn't end up doing it. This format is meant to require less effort from me, hopefully little enough that it won't prevent my actual project from making progress (I mean that's why people typically don't do these right?).

Instead, these are short journal-like entries that you hopefully found on Google (which is also why I decided not to use something like Twitter for this, which would be arguably more suited). They'll each contain one problem and one solution, and maybe something that can help solve your problem. No promises.

### Entry 1

The first problem I ran into is that I wanted to port a file with helper functions (since it has no dependencies to other files, making it a good starting point).

Unfortunately, it doesn't look like ReasonML/Bucklescript has APIs for ES6 Map/Set yet (nothing in the [JS module](https://bucklescript.github.io/bucklescript/api/Js.html) at the time of writing). So no way to do `new Map()` without a type error or using raw JS.

On the Discord community, I get pointed to the [Hacker News sample project](https://github.com/reasonml-community/reason-react-hacker-news/tree/master/src) by @glennsl. It has some very minimal bindings for ES6 Map. It's not much, but it's still super helpful. One day I might learn enough ReasonML to contribute bindings but starting with it right off the bat would be a bit much.

### Entry 2

Related to the previous entry: at some point I might want to use a functional (immutable) map/set implementation. That can wait after I've ported more of the code. I know OCaml comes with such data structures built-in, but @chenglou points out that the [Belt standard library](https://bucklescript.github.io/bucklescript/api/Belt.html) has a faster implementation than the default OCaml one. I guess I'll have to try it out and find out!

### Entry 3

Why does running `bsb -make-world` not compile any files?

```
ninja: Entering directory `lib/bs'
ninja: no work to do.
```

It turns out I didn't setup my `bsconfig.json` properly. I put `"sources": "src"` as the folder where all my source files are located. Turns out you're supposed to put:

```
  "sources": [
    {
      "dir": "src",
      "subdirs": true
    }
  ],
```

I'm surprised that you have to explicitly specify folders as recursive and that it's not the default behavior. Isn't it common to organize the source files of any decently large project into folders? The docs state that "we don't want to accidentally drill down into some unrelated directories". Maybe people have run into issues with this in the past.

### Entry 4

I sometimes just run `bsb -make-world` to compile my Reason files when I don't need to test the whole compilation pipeline with webpack. However, it didn't work out. It turns out that I needed to add

```
  "package-specs": {
    "module": "es6-global",
    "in-source": true
  },
```

I already had this setting in `webpack.config.js`, but `bs-loader` takes these settings from the webpack config file whereas `bsb` takes them from the `bsconfig.json` file.

### Entry 5

...talk about the `export {}` problem...

--------------------------------------

***to be continued...***
