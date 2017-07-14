---
title: My first six weeks at Recurse Center
date: 2017-07-05
disqus: y
---

It has been six weeks since I've started at [Recurse Center](https://www.recurse.com/) (RC) in New York. Since this is the half-way point, I thought it would be a good time to write a check-in of what I've been up to so far, since I get asked about it frequently.

Why Recurse Center?
-------------------

First, I should start by explaining what Recurse Center is and why I decided to join. It's quite unique in its goals and how it approaches them, so it's easy to get into all sorts of misconceptions.

To me, Recurse Center is both an educational program and a physical space where people go and engage in self-learning. The main goal is to improve as a programmer, and it's up to you to set your own curriculum and learning goals. The level of experience of attendees is very wide, ranging from beginners to industry veterans with years of experience. As such, some people focus on developing fundamentals, like learning algorithms or how code is compiled to assembly. Others have an ambitious exploratory side project and take Recurse Center as an opportunity to have dedicated time to work on it. It's also free (though living in NY is not).

People join in batches of 6 or 12 weeks at a time, and batches overlap, ensuring a continuous transmission of knowledge and culture.

It's not a bootcamp. No one gives you lectures. Not everyone is looking for a job. It's also far more than a way of allocating a three-month block of free time. I've done [something like that before](/2016/01/13/nomad-thoughts.html) as a "digital nomad". It worked alright, but the main thing I missed was being around other motivated people. Recurse Center provides both.

In fact, that is exactly what motivated me to apply to RC. I read their [FAQ](https://www.recurse.com/faq) and [manual](https://www.recurse.com/manual) and thought it sounded great, very much in line with my values. I even recommend reading them even if you have no interest or time for RC, it's quite insightful. I figured that such a program would self-select for motivated people that would be great to be around.

I have more thoughts about the culture which I'll write about later, but basically I applied on a whim, thinking it'd be a good way to spend the summer before I start working full-time. And here I am.

Choosing what to work on
------------------------

I had a couple of general ideas about things I could work on upon applying. I thought I could learn to make a large front-end app from scratch, which is not something I had done much of. In particular, I was thinking of making a web application to [visualize Facebook chat history](https://github.com/rudi-c/facestats.py). I ended up starting this at the beginning of the school term, and decided it was not a good fit for RC. It's not finished yet (and it will eventually be!), but I already learned a lot of new things from it (combining React, Redux, D3, TypeScript and Web Workers). The rest is just product and polishing work, whereas time at RC is better spent learning new concepts.

Another application I was thinking of building was a sort of "YouTube of coding sessions" that can replay coding sessions inside an actual text editor rather than a video of a text editor (which is inefficient, you can't scroll whenever you want, resolution is bad, etc). This would actually be quite novel to me as somehow, I managed to go through undergrad doing minimal conventional full-stack work [^1]. But in the meantime someone else released [exactly what I wanted to build](https://scrimba.com/), better than I could have done.

I also thought about using my time at RC to properly understand Rust. This could have been done through writing a graphics project. Or perhaps even using a new technology like Vulcan. I could also have implemented a database, since I don't know very much about databases in general, and even less about their internals.

Final choice: Elixir
--------------------

I ended up deciding to focus my time at RC learning the Elixir language (and the Phoenix web framework).

It's not just about learning a particular language of course. It's also learning more about writing distributed systems and doing more full-stack programming.

Elixir is built on top of Erlang, which was designed for building highly-reliable distributed systems very easily. It implements a system of lightweight processes that are very easy to use and are extremely cheap. As you'll see mentioned in [every article about Erlang/Elixir](http://www.creativedeletion.com/2015/04/19/elixir_next_language.html), it powers systems with high uptime and reliability requirements, such as the phone network. It also allowed [Whatsapp to power nearly a billion users](https://www.wired.com/2015/09/whatsapp-serves-900-million-users-50-engineers/) with a tiny team by Silicon Valley standards. Elixir is also created by José Valim, a former Ruby on Rails core team member, leading it to be well-suited for web development.

Therefore, projects that make good use of Elixir features were probably going to be full-stack applications with some non-trivial backend logic.

Which is why I decided to build [Stressed Syllables](https://github.com/rudi-c/stressed-syllables), a (working, but unfinished!!) application that takes in English text and tells you where the [stressed syllables](https://en.wikipedia.org/wiki/Stress_(linguistics)) are. My motivation came from doing [communications training](/2017/04/13/journey-valedictorian.html) and from being a non-native English speaker that frequently mispronounces words.

This project was interesting for a web app in that I need to:

- Do potentially long-running background work to fetch data from Merriam-Webster, while rate-limiting my own requests to avoid hitting *their* rate limiter
- Wrap Python processes in Elixir to do NLP and communicate between them
- Deploy the application on two servers (I don't *need* to, but it's not much of a distributed system if there's only one machine!)
- Write a load balancer (I could use Nginx, but writing your own is a good exercise and keeps deployment simple since it's integrated into the application)
- Share a key-value cache between two machines
- Write a simple frontend component (which was an opportunity to try Vue.js)

The app is currently running at [stressedsyllables.com](http://stressedsyllables.com). It's not quite finished, but much of the remaining work is polishing (e.g. dealing with NLP edge cases). That, I can do outside of RC. I will probably keep the application running after RC, since there seems to be demand for it.

When I decided to learn Elixir, I made an hypothesis. Not only could it be a pleasant language to use, but it may directly address legitimate business problem and as such, adopting could be a very practical choice at a company. That is, I wouldn't just have to wave my hands and gospel about how nice types are. I like to have the [support of a good type system](/2017/01/07/jane-street-ocaml.html), but it's pretty hard to use that as a argument to convince people to change languages. So far, evidence is weighing in favor of that hypothesis, but I will discuss that in another blog post closer to the end of the batch.

Side project: studies on distance field ray marching and noise functions
------------------------------------------------------------------------

After choosing to focus on Elixir over Rust, I thought I wouldn't be doing any graphics while at RC. However, one afternoon, Tim Babb gave a presentation on [automatic differentiation](https://en.wikipedia.org/wiki/Automatic_differentiation). It's a really cool technique for computing the derivative of any function (including programming functions with for loops).

I mentioned that I'd played with it before to find the [range of Perlin Noise](https://github.com/rudi-c/perlin-range) and started investigating applications to distance estimated functions, but I didn't get too far and abandoned the project. He suggested that some people doing [hobby rendering](https://www.shadertoy.com) might be interested in the results so I decided to take some time to finish up that project and publish what I found.

This ended up taking two whole weeks, way longer than I expected. Part of it is because there's a lot of details I wanted to get right and had to think hard about. Part of it is because writing technical blog posts is really hard and takes a lot of time, because you want to write them carefully and be very precise. Nevertheless, I eventually got that done in a series of four blog posts: [Part I](/2017/06/20/range-perlin-noise.html), [Part II](/2017/06/21/consistent-distance-fields.html), [Part III](/2017/06/22/restricted-perlin-noise.html) and [Part IV](/2017/06/23/fast-mostly-consistent.html).

Pair programming
----------------

One of the most notable aspects of RC's culture is the emphasis on [pair programming](https://en.wikipedia.org/wiki/Pair_programming). It makes the environment more social and is a great way to diffuse knowledge between people.

I've been making an effort to find opportunities or excuses to pair with people, since it's not something I was very familiar with and RC alumni commonly wish they paired more. I've mostly been doing one-off sessions with different people (usually lasts about an hour), but I think I should also try pairing on longer projects next half-batch.

Pairing sessions I've participated in include:

- Writing a Python algorithm
- Looking at Spark and vim configs
- Looking at Purescript and discussing Elm/React-style UIs
- Solve a compiler problem in Rust deciding which language feature to use
- Solve a D3 problem on selecting images and magnifying them independently
- Working on understanding rainbow tables
- Fixed a pinch-zoom-rotate bug in Fractal Photographer
- Implement NLP in my stressed syllables an NLP expert
- Write some tests for a Python AWS deployment tool
- Implement a shader in book of shaders
- Implement parallel mergesort in Elixir (next: implement MapReduce)
- Show someone how to write a distance field ray tracer
- Implement detaching links from nodes in a visual editor in React
- Got help on deploying to servers
- Implement a load balancer
- Got a bunch of help understanding Erlang/Elixir, such as clearing up a misconception I had about the Erlang VM automatically distributing processes among machines [^2]

Writing & blogging
------------------

Something that is highly encouraged at Recurse Center is to write about what you're doing, usually in the form of a blog post. The brilliant, yet simple way in which this happens is through [Blaggregator](https://github.com/recursecenter/blaggregator). It's just an internal feed of blog posts published by Recursers, that hooks in Zulip (our chat system) so that people can discuss them as they are published. It creates an audience, happens automatically (so it doesn't feel like you're self-promoting) and it makes it look like blogging is just a thing people do.

Of course, not everyone blogs, nor does everyone need to. The point is that it establishes that blogging is a good use of RC time. In theory, people can spend their time however they want at RC, but most people are motivated to be productive and contribute to RC culturally by staying on-topic.

This is how I felt comfortable spending most of a week writing the series of four blog posts on graphics I described earlier. Since the start of RC, I've also published a blog post on [beliefs and emotions](http://digitalfreepen.com/2017/06/11/beliefs-and-emotions.html) and [what motivates me to write](http://digitalfreepen.com/2017/06/19/why-want-to-blog.html). They were both things I've been meaning to write for a while, but never quite made the time for them. I also have a few more blog posts in the pipeline.

I've also spent time [writing about internships](https://github.com/evykassirer/playing-the-internship-game), which I intend to continue doing for a while.

Finally, Blaggregator combined with going back to Waterloo to attend convocation inspired me to compile a [list of blogs by Waterloo students](https://github.com/rudi-c/the-waterloo-blogger). For now, it's nothing more than a simple experiment. But I am hopeful that small things like this can make a positive contribution to student culture.

Presenting
----------

At Recurse Center, Thursday is presentation day. You can sign up to give a 5 minute presentation and there's usually 6-10 presentations at 5 PM. Additionally, there's many meetings throughout the week on common topics of interest (machine learning, haskell, security, web programming, etc) and it's common for one Recurser that has expertise in the area to give a presentation.

Following my recent interest in public speaking, I've been making an effort to take those opportunities to present. So far I've given a 5 minute presentation on green threads implementation, GPGPU programming and my stressed syllable app. I've also given two longer talks: one where I walked through the architecture of my WIP chat history visualization app and highlighted points of interest, and another introductory talk on Big Data since I had just taken [a class](https://lintool.github.io/bigdata-2017w/) on the subject.

Culture
-------

I've alluded throughout this blog post that RC gets a lot of things right about its culture. I am liking it quite a bit so far. I think I'll save a longer discussion and analysis of what makes RC work for an end-of-batch blog post. It's the kind of topic that's best simmered for a long time before it becomes really clear in your head.

Next 6 weeks
------------

Since I already managed to learn a lot of things from my stressed syllable app, the halfway point is a good time to switch to another project.

I still want to focus on Elixir, since I feel that I have much, much more to learn about how to use it well. One project I would like to do is to write a collaborative text editor. I've always wondered how those work, and it makes good use of different features of Elixir and the Phoenix web framework. Apparently, the latter has very good support for channels (websockets). This kind of high-interaction use case should be something Elixir is good at. Along the way, I'll need to do things like user authentication. Nothing too hard, but I should know how those basic things are done. I don't have a great sense of how long it would take me but if time allows, a more ambitious extension would be to write a simple collaborative 3D modeling tool.

There's also a bunch of readings I've been meaning to do that I can hopefully get to. A lot of them involve web technologies and having a deep understanding of them. This includes understanding the use cases of WebAssembly, why Servo is exciting, how the browser rendering engine works, how it is optimized, how to understand [Javascript semantics properly](https://github.com/getify/You-Dont-Know-JS) and what the difference between all the different databases are. With some luck, I'll get to a subset of them.

Finally, since the Summer 2 batch will be starting with new faces and new interests, that could also influence my plans.

See you again in 6 weeks!

----------------------------

[^1]: Instead I did mostly native development (e.g. C++ on the desktop, iOS) or random topics like research, compilers.

[^2]: It doesn't, you have to tell it which machine to spawn the process on. Rather, the benefit that Elixir provides is that calling processes look just like calling a class, so the code is the same the same whether they're local or remote. This makes it very easy to write code as microservices in separate modules right from the start and those modules out to their own nodes when the load becomes heavy.
