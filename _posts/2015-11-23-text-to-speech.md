---
title: Proofreading with text-to-speech (diff included)
date: 2015-11-23 00:00:04
disqus: y
---

Today I discovered the idea of proofreading using text-to-speech software. It helps find improvements to make in sentences when they sound off.

This sounds like a nice writing trick in theory, so I decided to immediately put it into practice to try it out (and if I don't do it now, I might forget about it by the time I need it). I downloaded [NaturalReader](http://www.naturalreaders.com/index.html) and copied my [Dropbox blog posts](/2015/10/12/dropbox-first-internship) one paragraph at the time and let "David" read them out for me.

<a href="/images/2015/11/texttospeech.png" data-lightbox="texttospeech"><img src="/images/2015/11/texttospeech.png" alt="David reading" class="alignleft size-full" /></a>

The result was that I caught quite a few typos and imperfections. Since my blog is hosted on Github pages, you can see [all the corrections I made in this diff](https://github.com/rudi-c/rudi-c.github.io/commit/0ad55f4f777cae7b2256aa0a715432830ee4ddc0).

Here are some examples:

> ...as the app originally *only* displayed a screen-size thumbnail (before).

> ...as the app originally displayed *only* a screen-size thumbnail (after).

I often have difficulties with the placement of modifiers such as _only_ and _just_. Hearing the two different versions in speech accentuates any awkwardness in their placement.

> Those projects were interesting exercises in understanding the distinction between doing something and doing it well, and I learned the culture at Dropbox leans strongly towards doing it well, *“sweating the details”*. (before)

> Those projects were interesting exercises in understanding the distinction between doing something and doing it well, and I learned that the culture at Dropbox leans strongly towards doing it well. *They call it “sweating the details”*. (after)

This was one of the longer sentences. It doesn't look _too_ long on the screen, but it would be hard to follow someone saying that sentence to you.

> I can still list 30 or so interns from pure recall and I *can to* more than 60 from recognition... (before)

> I can still list 30 or so interns from pure recall and I *can do* more than 60 from recognition... (after)

This is a simple typo. They are surprisingly hard to catch. The brain is being too clever here, as [the huamn mnid deos not raed ervey lteter by istlef, but the wrod as a wlohe](http://www.mrc-cbu.cam.ac.uk/people/matt.davis/cmabridge/).

> Or you could share some native *(in the sense of light on the runtime) code* (before)

> Or you could share some native *code (native in the sense of light on the runtime)* (after)

Similar to the above. Not only does the brain read whole words at a time, it can sometimes read whole sequences of words at a time. The quick context switching with the parentheses is much more jarring in speech, in the absence of a birds-eye view on the sentence.

In general, text-to-speech is the closest thing to a third-party reader without having a third party reader. The writer of a piece will be most vulnerable to the brain's automatic error-correction power, as he already knows what to expect. After all, humans don't perceive the world solely through their eyes, but also [reconstruct it based on expectations](http://www.iflscience.com/brain/how-do-our-brains-reconstruct-visual-world), such as prior knowledge about objects.
