---
title: Medium-size software companies are the best default choice for internships
date: 2017-01-14 00:00:01
disqus: y
---

How do you decide which companies to invest time in applying to, or which offer to accept if you've successfully passed their interview?

Sometimes there's a unique factor that can make the decision easy. For example, if you really want to work on the Rust compiler, nobody but Mozilla will offer you that.

More often, you might have a variety of companies you can apply to: some small, some big, all of which have some cool products, and different flavors of technical challenges. During internships, you are still discovering what your interests are, so they might not be sufficient to guide your decision.

In the absence of major interests like "I want to work in healthcare" or "I want to do 3D graphics", I recommend going for medium-size companies. Generally, those are companies with an engineering team between 30-500 people (the total company size would be 100-2500 employees[^0]). The exact size doesn't matter so much as how big the company feels; the culture of the company may make the company feel smaller or bigger.

More specifically, they tend to have the following traits.

They tend to be large enough to have challenging technical problems worth solving
---------------------------------------------------------------------------------

In general, startups have a pressure to optimize for speed. This is especially true if they are still figuring out their market. For example, there's no point in refactoring the code to be decouple tangled logic if the whole thing could end up in the recycling bin next month.

Since they don't have many users, they don't run into many performance problems. Most technical challenges in programming fundamentally exist because of performance reasons. You can almost always come up with a naive solution to solve any problem, but algorithms exist because most naive solutions don't scale. If you only have 1000 users, your O(n^2) deduplication routine still only takes a millisecond.

That being said, [many startups](https://www.figma.com) do have technical challenges. Some are even born because of a technical challenge. But on average it's less likely.

If your main interest is the product and not the engineering, this point is less important. However, during internships, I recommend focusing on your technical skills. It builds a solid foundation that you can use to implement your product ideas later. Also, an internship is too short to own a product through its whole lifecycle.

Your job: Ask the engineers what technical challenges they've solved lately, and what's next on the roadmap.

They tend to be small enough to have technical challenges for you to solve
--------------------------------------------------------------------------

Even if a company has a lot of technical challenges, you want them to be accessible for an intern that only stays there 3-4 months. It's no good if there are no low-hanging fruits, which may be the case at companies whose infrastructure is too mature.

At Dropbox, I was told "there's too much important stuff to do to assign you to a trivial task". At larger companies, you may get unlucky and end up with little work to do, which I hear is quite common.

Your job: Ask what projects past interns have completed.

They tend to be small enough for you to have impact
---------------------------------------------------

Although having impact is possible at any company, it generally helps if the team is a little smaller, if the release cycle is a little shorter, if there's less legacy code to work with, if there are fewer hoops for you to jump through to get anything done, etc.

Your job: Ask about how you can have impact at the company.

They tend to be large enough to have a brand name _within tech_
-------------------------------------------------------------

A company like Quora won't compare with Google when it comes to impressing the average dude down the street, but you shouldn't care about that. You only need the company to be well-known among engineers and recruiters who may offer you a job.

Your job: Find people you respect and pick their brains for opinions. Make sure to get a variety of viewpoints since individual people have biases.

They tend to be small enough to have a consistent engineering reputation
------------------------------------------------------------------------

While the big companies have the best and most famous engineers in the entire tech industry, they're so big that the engineering quality can become inconsistent. For people in the know, an applicant with past experience at MemSQL provides a better signal than experience on some random team at Microsoft.

Also, you will often hear people saying that they intend to work at Facebook or whatnot for two years so that they will have it on their resume, but you rarely hear people say the same thing for, say, Pinterest.

Your job: Search around the Internet to get a sense of how well-respected the company is.

They tend to be large enough to have an organized internship
------------------------------------------------------------

They will often have a formal internship program. This involves a well-defined evaluation criteria, regular feedback that lets you know where you stand, and an assigned mentor. It's very important to have these because it's very nerve-wracking to be uncertain about how well you're doing. Companies like Airbnb believe that whether you receive a return offer or not should never be a surprise if the internship was well organized.

You can find those at any company if you're lucky enough to have a good manager, but having an internship program means that there's at least one recruiter or engineer who coordinates and owns the program. This person will do work behind the scenes to match interns with appropriate projects and engineers who would be good mentors. They will pressure the mentors to provide regular feedback, conduct weekly one-on-one sessions, etc. They can be someone to talk to if you're not comfortable with your mentor or manager.

Your job: Ask the recruiter how the internship is structured and who coordinates it. Ask how interns are evaluated. Ask what kind of mentorship is provided.

They tend to be large enough to have other interns
--------------------------------------------------

It's nice to have a large intern cohort. It means more people your age to meet and become friends with. The people you meet during your internship are very important, as you can learn just as much from them as you do from the day-to-day technical work. And as a general rule, it's easier to get along with people that are similar to you, namely in age.

However, you only need 10-50 other interns to meet at least a few people that you'll get along with. While there are more interns at larger companies (even thousands), it's not useful since you won't get to know most of them. It's better to know a few people well than many people superficially.

Your job: Ask how many interns they expect to hire. If the company is small, talk to as many of the full-time employees as possible to figure out if they seem like the kind of people you'd get along with.

They tend to be large enough to have organized engineering
----------------------------------------------------------

Small startups are less likely to have code reviews by virtue of being small and emphasizing speed. This means that you are less likely to get feedback on your code, and more likely to run into hastily written code. If you are new to programming, this will cause you headaches and lead you to pick up some bad habits, as we humans learn from example.

Small startups are also less likely to have decent infrastructure and developer tools setup, like a decent build system. Although this is a good opportunity to have more responsibilities and learn more things, you may need more experience to take full advantage of these opportunities.

Your job: Ask the engineers about the code review culture at the company. Ask them about their pain points as developers.

Don't worry about stability
---------------------------

Since you're only there for 3-4 months, the future of the company does not matter to you. Even the media sentiment around the company, the amount of "hype" they're getting, doesn't affect you. You only need to make sure that they're not doing so badly that all the good engineers left and that the morale isn't bad enough to make your internship miserable.

As an intern, you don't get equity and you are very unlikely to get laid off, so you should optimize for learning.

Cause v.s. effect
-----------------

I have described a few desirable properties of medium-size companies *for internships*[^1]. They both small enough and big enough to have most Nice Things.

It's important to never forget that you want to intern at a company that has those desirable properties, which **only correlates** with their size. Not all medium-size companies have those nice properties, and not all companies that have those nice properties are medium-size.

It's only a heuristic.

----------------------------------

[^0]: You may feel that 100-2500 feels like a really big range, but it's not as big as it looks. Tech companies easily grow 30-50% a year. In fact, double or tripling in a year is not unheard of. A range like 200-500 employees would therefore be too small because it would imply that the company goes from being a bad choice, to a good choice, to a bad choice again in only the span of 2-3 years.

[^1]: I am currently not qualified to give a nuanced view of full-time jobs. Ask me in a decade or so.
