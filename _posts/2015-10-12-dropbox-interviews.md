---
title: Learned at Dropbox - maximizing signal in interviews
date: 2015-10-12 00:00:03
disqus: y
---

This is one of four blog posts on my experiences interning at Dropbox in Fall 2014 and Summer 2015. Read more about [my first](/2015/10/12/dropbox-first-internship) and [second internships](/2015/10/12/dropbox-second-internship.html) and [the social, cultural and business aspects](/2015/10/12/dropbox-misc.html).

_Important note: while the words “Dropbox” and “interview” are both present in the title, this isn’t a guide on “how to pass Dropbox interviews” so much as a discussion on the design of tech interview questions._

I’m interested in how companies’ interview process are designed and evolve, because it has strong impacts on the culture. For most candidates, it is their first direct interaction with the company, their first impression. I anticipate that one day, I will have to conduct interviews myself [^0].

Interviews are an attempt to predict one measure from another. They want to predict one set of measures such as “technical performance” and “will I get along with this person?” using another set of measures such as “past achievements” and “ability to solve coding problems”.

To make predictions effectively, the interview process needs to minimize variance and control bias. This is a very hard problem to solve. Besides having gone through Dropbox’s interview process myself, I also shadowed a few interviews and referred a number of people, some of whom passed and some of whom did not. This gives me a good sense of how Dropbox approaches it and how hard the questions are.

A key concept is that of “maximizing signal”. This term shows up a lot in internal training documents and discussions. You want the interview to tell you as much as possible about the candidate and minimize the number of ways the candidate could fail due to “bad luck”.

Reducing noise
--------------

For example, interviewers at Dropbox don’t want to have the candidate stuck, especially on little things. Everyone has certain kinds of problems with which they don’t click and everyone can experience a blank in the middle of an interview. That’s noise: something that tends to happen randomly, even for qualified candidates. Therefore, giving a hint helps keep the interview moving. The candidate might do perfectly well after asking for just one hint. In the real-world, people ask questions and discuss problems with each other.

Alternatively, while it is nice when the candidate has a mastery of their language of choice, it isn’t a big deal if they forgot the particular interface for a certain function. In real-world situations, search engines are available [^1]. This is why I'm not fond of running the program in an interview. That often requires a trivial mechanical process of fixing some syntax errors. Getting the right understanding of the problem is the non-trivial part.

However, ‘being willing to give hints’ (from the interviewer’s perspective) and ‘being willing to ask for hints’ (from the candidate’s perspective) are both easier said than done. One story I heard is that for a while, Dropbox had trouble with European candidates. Some would stubbornly refuse to take any hints and would keep heading down dead-end paths. After a while, an intern pointed out that in some European countries, students are taught to ignore hints because it was typical for interviewers at local firms to test the candidate by trying to mislead them. These cultural differences introduce noise that can be very difficult to account for [^2].

Maximizing signal
-----------------

In order to learn as much as possible from the candidate, it is useful to have a broad set of questions that test for the desired set of skills in many different ways. It is easy to see why by imagining an extreme example where all questions are graph search problems: it would just be redundant.

Of all the interviews I’ve had personally, Dropbox’s was the most comprehensive. For one, even interns have 5 technical interviews to go through. What I found most interesting was that all questions seemed to have a purpose. There’s the standard algorithm questions, which are common. They involve common concepts like hash tables and recursion. Those are just mentally intense and measure how much complexity can fit into your head at once.

Dropbox also has some interview questions that are not particularly difficult conceptually, but have a lot of edge cases that could easily be missed. Those are useful to measure “attention to details”. There are also design questions where the algorithm or data structure that solves the problem is not that advanced, but you have to figure out which you would use in practice given a similar problem in the real-world. Finally, concurrency often shows up in some of the questions.

In contrast, I've sometimes had interviews at other companies where I felt I was asked a question that sounds like an interview question but it's not clear what it measures beyond basic ability to write code. It can feel a little artificial. Seeing Dropbox’s interview process inspires me to choose questions I might ask myself more carefully, if nothing else.

_Of course, everybody's experience will vary._ I think Dropbox does a good job at training the interviewers but it's not amazing to the point where everyone will have a good experience - at least one of my friends who applied did not. While interviewers are trained in ways to maximize signals, some interviewers might be less experienced, less motivated, less sharp, less friendly, having a bad day, etc. If you've never interviewed with Dropbox but are planning to, please do maintain reasonable expectations even though I'm saying some good things about the process.

I personally don’t find that the questions are significantly harder than those of other major tech companies. What I think gives Dropbox [the reputation](http://qr.ae/RoSicS) [of being selective](http://qr.ae/RoSix9) really lies on the process being very comprehensive. Otherwise, the questions aren’t domain specific and there’s not much to do to prepare for them besides work on a variety of software and write lots of code.

Controlling bias
----------------

After having interviewed at Dropbox and many other companies, I’ve been noticing more and more the connections between the company’s engineering problems and the interview process [^4]. Dropbox’s main product needs to solve a massive amount of edge cases and getting a single one of those wrong could mean the loss of customer data. The amount of data processed on a daily basis is enormous, meaning a more efficient algorithm can lead to huge savings in server costs. Everything ends up involving concurrency. Considering that, it’s no surprise that the interview aims to be very comprehensive.

Alternatively, I’ve had a startup ask me to make a small modification to their main product which is open-sourced. Seems very sensible - there's hardly any way to make the evaluation process closer to the job responsibilities than this. Jane Street’s interview process is as long as Dropbox’s, but the problems are slightly harder and slightly less comprehensive - makes sense, their product is more specialized.

Every once in a while, I’ll see an article show up on Hacker News or a question on Quora about how tech interviews are broken[^5] and how one approach is better/less discriminatory than others. In comments/answers, the same points get brought up every time: “no one implements algorithms in real-life” “I’ve never used recursion” “I did have to use recursion” “I want my candidate to know how to write efficient code” “I don’t have the time to prepare for those kinds of interviews” etc. Given that it’s all engineers discussing this topic, I find it interesting how a lot of time, these discussions miss the big picture: interview processes should be tailored to whatever the organization needs, and that’s always a different answer for each company.

Interviewing is an art, and it is one that I will inevitably need to learn.

-----------------------

[^0]: Every time I hear a new graduate talk about their experience entering the work field, they almost always say “it feels weird that you already start interviewing candidates when just 6 months ago, you were the one being interviewed”.

[^1]: I was careful not to say “always” available. Google is a source of information, and function interfaces/language features are purely information. Google doesn’t solve problems for you. I could spend forever talking about this but that it’s very common to hear the excuse “I could Google it” when it’s besides the point. Yes, you would use a binary search library in production when applicable rather than writing one yourself. No, it's not always applicable - I don't know how many times I've seen problems that required subtle variations on binary search, and implementing a solution requires a good understanding of the fundamentals.

[^2]: This is one situation that is hard to mitigate in a concrete way besides having a diverse group of employees who, collectively, are aware of these differences and can share this knowledge with each other.

[^4]: As for the companies where the connection was missing, I felt like they didn’t care enough about hiring/getting the best people.

[^5]: The interviews are broken, and there won't be perfect fix anymore than there will be 'perfect criteria for university admission', 'perfect criteria for determining eligibility for government programs', etc. [This article by one of the most experienced interviewers does a good job at explaining why.](http://www.gayle.com/blog/2015/6/10/developer-interviews-are-broken-and-you-cant-fix-it)
