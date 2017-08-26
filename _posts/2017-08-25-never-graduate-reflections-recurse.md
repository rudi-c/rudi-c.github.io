---
title: Never graduate! Reflections on Recurse Center
date: 2017-08-25 12:00:01
disqus: y
toc: true
---

I recently finished a 3-month stay at Recurse Center. This post is about what I did in the second 6 weeks of my batch, following my previous [mid-term check-in](/2017/07/05/six-weeks-recurse.html). I'll also highlight the interesting bits of RC culture and how my stay at RC influences my future directions.

Writing a collaborative text editor
-----------------------------------

My main project for the second half was to write a real-time collaborative text editor, much like Google Docs. One motivation for this project is that I heard that Phoenix was good at handling WebSockets, so I wanted to try it out and see what it was all about. A text editor is a high-interaction application that requires WebSockets. Plus, the conflict resolution algorithms seemed fun to learn and implement.

I first started writing some Phoenix boilerplate to handle user authentication, creating new documents, etc. They're basic things and honestly not that essential, but useful to learn in any web framework. Then, when I got to WebSockets…it mostly just worked. Turns out I don't have much to say there, I didn't run into any challenges. And most of the text synchronization and conflict resolution logic needed to be in the frontend, so this turned out to be more of a Typescript project than an Elixir project.

During the project, I got to learn a bunch of things, including [Javascript setup pains](/2017/07/14/how-to-typescript-react-phoenix.html) (trying to fix the build system + writing tutorials ended up taking almost a week), testing with the Ava framework (testing edge-case-y synchronization is quite hard), setting up linting, and a bunch of other things to make the project nice and professional.

The editor in its current state can be found at [http://alchemy.digitalfreepen.com/](http://alchemy.digitalfreepen.com/)

I have a blog post that explains all the technical details in the works. While the core synchronization logic works up to the extent of my current testing, there's still a bunch of little things to fix (e.g. cursors disappearing sometimes) and polishing that I want to do on this project to make it more presentable and advertisable.

So many things to read
----------------------

I spent a fair amount of time just reading stuff, trying to trim my over-growing reading list by a little bit. That included:

- Lots and lots about Elixir and Erlang, details of their implementations, pros and cons, etc
- Read the [Raft paper](https://raft.github.io/), which is indeed a fairly understandable introduction to consensus algorithms. Also quite implementable. This is unlike Paxos, where I always struggled even to get an intuition for it
- Read the [State of JS](https://stateofjs.com/) survey which is quite cool
- Learned about [Kalman Filters](http://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/) from the blog post of a fellow recurser
- Read about WebAssembly well to understand it well. It's interesting that it's heralded as a way to bring new languages to the web when it's technical abilities are mostly the same as Emscripten, but with [faster parsing times](https://blog.figma.com/webassembly-cut-figmas-load-time-by-3x-76f3f2395164). But maybe that's a good thing (Emscripten is not that well known)
- Did a lot of research about Ruby history and implementation, for a very far-off project I'd like to do that involves running Ruby on the web as a subcomponent
- Took Udacity's [Browser Rendering Optimization](https://www.udacity.com/course/browser-rendering-optimization--ud860) class, which I've been meaning to take for a while and only takes 3-4 hours at 1.5x speed if you skip some of the exercises. In particular, that course taught me the importance of latency for user experience (along with other discussions with a game developer at RC and [Dan Luu's blog post](https://danluu.com/term-latency/))

Meeting new people & pairing
----------------------------

With a new half-batch comes new people (>30 new people!). It's always a little overwhelming to have so many new people to meet. I was excited though, as I got to know a rather large fraction of my own batch (and the previous one), therefore thought I might keep this up for the remaining 6 weeks.

That didn't really happen unfortunately. I mean, I did meet new people and make new friends, but there's also plenty of people I never talked to. This should have been fairly predictable as I have a consistent introversion-extroversion cycle. My last 5 years have involved living in a new environment every 4 months (due to Waterloo's schedule). What I found was that I would consistently get excited and motivated to meet new people and socialize at the start of one of those 4 month periods, which I could maintain for up to 2 months. Then the social energy levels would crash and I wouldn't find the will to bother anymore. I still showed up for lunches, talked to people and hung out with people I'd already met (because it was already habit at that point), but I didn't actively seek to get to know everyone. Sorry to all the new folks with whom I've exchanged "you look familiar, but I've never talked to you yet" glances!

I also paired on a few things, though not as often as the first half:

- Added a word count feature to my (still unreleased) Facebook chat history app (I figured it was a good project to "onboard" people to pairing)
- Finished implementing a replicated cache for [Stressed Syllables](stressedsyllables.com)
- Small toy project implementing basic MapReduce in Elixir
- Trying to inherit from NumPy objects in Python
- Get OpenCL working and do a basic Gaussian blur

On the social side, I went to the Guggenheim Museum and the Hans Zimmer Live concert which was pretty awesome.

Presenting
----------

I had the chance to give 3 more presentations. One on Elixir, one on my text editor as it was getting presentable, and a totally improvised one on [AA trees](https://en.wikipedia.org/wiki/AA_tree) and how it's implementable in contrast to Red-Black trees.

I was thinking of doing a lecture series on garbage collection but ended up too absorbed in my own project ^^' (it's a lot of preparation!).

Write, revise, review, post, write, ...
---------------------------------------

As I mentioned in the previous post, Recurse Center is an environment that encourages blogging implicitly by virtue of the fact that a lot of other people do it. I got to write a few more things. The most important one for me personally is the blog post on [skill granularization](/2017/07/18/how-to-learn-anything.html). I also wanted to make sure to have my [thoughts](/2017/08/03/why-offer-mock-interviews.html) and [experiences](/2017/08/03/guide-mock-interviews.html) on mock interviewing down since it's relatively uncommon, and I remember finding that there was a lack of resources on how to conduct good mock interviews when I was looking for them. Finally, I finished writing down [all the advice I could think of on internships](/2017/08/01/everything-about-internships.html), so I can move on from that.

Recurse Center's culture
------------------------

Recurse Center puts a lot of emphasis on its culture. Having a good culture is important anywhere, of course. But it's especially important at Recurse Center whose goal is to help people become better programmers by challenging themselves with projects, often beyond their current abilities. This is difficult to do if you think you might be judged for failure.

> "Fear is the enemy of will. Will is what makes you take action. Fear is what stops you and makes you weak. You must ignore your fear. When you're afraid, you can't act." - some movie I haven't watched, but hey, the quote sounds cool!

Other recursers have blogged in length about RC's culture, so I won't go into all the details here. Rather, these are just a few points that particularly stood out to me, that made me feel that a lot of thought had been put into the culture.

- Show don't tell: the welcome speech started with something along the lines of "*We welcome* you whether you're an introvert or an extrovert, *we welcome* you whether you use Windows, Mac or Linux, *we welcome* you whether you're an early bird or a night owl, *we welcome* you..." (and this goes on for another minute). This leaves far more of an impression than a plain statement like "our company values inclusivity and blabla..."
- Recurse Center has [4 social rules](https://www.recurse.com/manual): no feigning surprise, no well-actually's, no back-seat driving and no subtle-isms. They cover a lot of ground and are well explained in my opinion. They also say "We expect you to break these social rules and it does not mean that you are a bad person. Just apologize, and here's how you do it" (followed by a little sketch of each of the rules). This I think is quite important, as it assumes the best of people, giving them a chance to become that "best".
- The idea of good culture at RC is not some narrow definition of "you have to be cool enough", which is about particular sociable personality traits. For example, one of the roles you can sign up for on the first day of the next overlapping batch is to sit in a side room and just chill. This is to signal that it's not mandatory to be in the main space to socialize (the first day is quite intense!). After all, RC's culture won't fundamentally solve human issues like awkwardness or imposter syndrome. But it does make it possible to be much more open about it.
- RC pays for itself via recruiting fees, but they do seem to mean it when they say "we don't run the Recurse Center so we can recruit, we recruit so we can run the Recurse Center". This makes all the difference.

Looking back and looking forward
--------------------------------

The richest experiences don't necessarily have to have an immediate effect on your life. They only need to pay dividends in the long run. When I went on a [solo trip two years ago](http://digitalfreepen.com/2016/01/13/nomad-thoughts.html), I didn't come back as a drastically different person. But subsequent experiences many months later would end up tying to what I had experienced during the trip and gave more insights about myself.

This is why I expect that most of the benefits I'll get from having attended Recurse Center are *yet to come*. That being said, there are *some* changes I can perceive immediately.

Some changes have to do with specific things I've learned. By learning Elixir, I've started to get interested in distributed systems and devops, for example. Furthermore, the Typescript + Phoenix stack is the first one I've found myself at home yet, being both pragmatic (easy to get stuff done with) and satisfying my affinity for writing good code and designing systems.

But the most important effect is that Recurse Center got me **excited about side projects again**. I started university very motivated to do side projects, and I would keep an ever-growing list of project ideas and things to learn. After a few internships though, that motivation gradually decreased. I did keep learning: reading Hacker News, going to meetups, etc. But I no longer made much plans to write projects. I no longer kept a to-do list of things I wanted to do. Instead, I caught up on socializing, traveled, had various life experiences which have been helpful in [approaching life with more confidence](http://digitalfreepen.com/2017/07/18/how-to-learn-anything.html). I think having different periods in life like that is for the best. But life comes in cycles, I'm now ready to start making use of the stuff I learned. Being at Recurse Center helped me get back into the mode of coming up with new project ideas all the time, and I have enough ideas right now to occupy me for at least 2-3 years. We'll see how that goes as I start working full-time, but it's good to be finally in the mood for it again.

Therein lies the genius in Recurse Center's motto, **Never Graduate!** While RC is amazingly immersive and interesting enough to always focus on the present, it all ultimately sets you up for the future. It motivates people to keep learning. So to you, the reader of this blog post, whether you've never graduated, are soon to graduated, or have graduated already:

Have you considered not *(really)* graduating ;)?
