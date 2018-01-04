---
title: Is implementing Operational Transform hard?
date: 2018-01-04 12:00:01
disqus: y
---

[Operational Transform (OT)](https://en.wikipedia.org/wiki/Operational_transformation) is a class of algorithms used in tools like Google Docs or Dropbox Paper to support collaborative editing, where multiple people work on the same document at the same time. It's also reputed to be quite complex. There's a famous quote by Joseph Gentle, one of the early people to have implemented OT, that shows up on Wikipedia and in nearly every blog post that talks about OT:

> Unfortunately, implementing OT sucks. There’s a million algorithms with different tradeoffs, mostly trapped in academic papers. The algorithms are really hard and time consuming to implement correctly. […] Wave took 2 years to write and if we rewrote it today, it would take almost as long to write a second time.

However, what is less known is that the same Joseph Gentle later retracted that statement in two [Hacker News](https://news.ycombinator.com/item?id=12311984) [comments](https://news.ycombinator.com/item?id=10003918):

> Yes thats me! For what its worth, I no longer believe that wave would take 2 years to implement now - mostly because of advances in web frameworks and web browsers. When wave was written we didn't have websockets, IE9 was quite a new browser. We've come a really long way in the last few years.

and

> You're right about OT - it gets crazy complicated if you implement it in a distributed fashion. But implementing it in a centralized fashion is actually not so bad. Its the perfect choice for google docs. Here is my implementation of OT for plain text: https://github.com/ottypes/text Note that its only 400 lines of javascript, with liberal comments. To actually use OT code like that, you need to do a little bookkeeping. Its nowhere near as bad as you suggest.

But as it often happens, the quote took a life of its own while the retraction is buried in the archives of Hacker News comments.

I bring this up since the quote is getting relevant again now that CRDTs are arriving into the scene. CRDTs are a newer class of conflict resolution algorithm. Thus, people will inevitably start comparing OTs and CRDTs to understand the differences and decide which of two to implement.

So what's the conclusion? I've never personally implemented an OT system, so I can't speak from first-hand experience. But I'm acquainted with a few people who've tried to implement various flavors of OT. My understanding so far is that:

- It takes effort to understand OT and makes for a fun and challenging side project
- OT with a central server is not too hard to implement, especially for plain text OT
- OT with a central server has been implemented enough times that there's a lot of resources and knowledge floating around
- In those cases, the code for OT won't be too complicated either
- Fully distributed OT and adding rich text operations are very hard, and that's why there's a million papers
- The most difficult part of OT is not the code, but the difficulty in proving that your system is correct. Therefore, *maintaining* OT code is difficult. Either you need to prove your code correct repeatedly (and historically people make mistakes), or you need a powerful testing infrastructure for concurrent/distributed systems (which is also hard to write)
