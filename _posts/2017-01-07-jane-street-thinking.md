---
title: Learned at Jane Street - Thinking fast and slow
date: 2017-01-07 00:00:01
disqus: y
favorite: y
---

This is the first of two blog posts on my Summer 2016 internship experience at Jane Street, focusing on the company. For the technical aspect of working with OCaml, [read the second](/2017/01/07/jane-street-ocaml.html). I do not represent the company: take everything I say with a grain of salt. Other interns have their own unique experience which may differ from mine, my reconstructive memory could be telling lies, I may be rationalizing a lot, etc, etc.

I initially applied to Jane Street with a reasoning that went along these lines: I like functional programming and would like to be able to use it on big projects in the future. To do so, I would need to understand effective practices in industrial settings, which is sparsely scattered on the Internet. Jane Street is well known for having a large OCaml codebase and they seem to be a good company: the sentiment on the internet is positive and my school's [programming language professor](https://cs.uwaterloo.ca/~plragde/) occasionally lectures wearing a Jane Street t-shirt. Therefore, let's apply to Jane Street.

After a summer there as a developer intern, I did learn a lot about functional programming, but with their amazing internship program I also learned so, so much more.

A culture of learning
---------------------

In a good internship, you walk away knowing more than when you walked in. Many companies invite guest speakers and encourage their employees to give presentations, but Jane Street's intern "curriculum" is especially good and one of the strongest selling points of the internship.

In my cohort, we were roughly 30 developer interns and 70 trading interns. For both devs and traders, Jane Street follows the model "if you can learn, [we will teach you](https://blogs.janestreet.com/making-making-better/)". While knowing to code is a useful prerequisite for devs, and knowing math is a useful prerequisite for traders, neither are assumed or [expected to know anything about functional programming](https://blogs.janestreet.com/no-functional-experience-required/) or finance.

During the summer, as a dev intern, I can think of at least:

- 13 tech lectures (and countless informal ones over lunch). Jane Street builds a lot of tools and libraries in-house and they cared to teach us how they were designed and why they were using it. The attitude was not "Not Invented Here, we have our own stuff, deal with it". One great talk, [available online](https://blogs.janestreet.com/seven-implementations-of-incremental/), covered how a library evolved through seven versions, each solving new uses cases.
- 11 lectures on finance. They covered a lot about how markets work: types of securities traded on markets, market microstructure. In addition, they talked a lot about the history of markets and what incentives led them to be created and evolved into what they are now. There were also a lot of stories of how great firms crashed and burns, to emphasize how even smart people can fail.
- 4 lectures on human topics related to psychology
- 9 talks by guest speakers such as [Tyler Cowen](http://marginalrevolution.com/)

For trading interns, they attend fewer tech lectures and more finance lectures, naturally. In addition, they participate in many training activities like mock trading and various betting games and contests that teach how to think critically and under pressure. Sometimes, the devs would join in too.

Intern curriculum aside, having these types of classes and inviting guest speakers is just a general part of the culture. They're the only company I've seen so far that has an office with a room labelled specifically "classroom". Books are plentiful in the library. More importantly, the employees themselves read a lot and will frequently talk about recent things they've read and give recommendations over lunch. Being personally very interested in psychology, it's also fun to be somewhere where most people are at least familiar with concepts of behavioral psychology, which allows for more honest discussions of our biases.

Work-life balance
-----------------

From within the bubble of my social demographic (university students & techies under 30), the general sentiment is that tech culture > finance culture, no doubt in part due to the many misconceptions people have about finance.

In many ways, the culture is very much tech-like. Jane Street serves breakfast and lunch, and there's free snacks stations scattered around. People use sound effects as alerts giving the office a funky arcade vibe. There's no dress code: some people wear dress shirts, but more walk around in shorts and hoodies. This is actually quite funny given that the building next door is occupied by Goldman Sachs employees. Even after 3 months, I couldn't help but smirk whenever I saw a Jane Streeter coming to the office in jogging attire heading for the gym showers, among a crowd of suits.

As an intern, we worked reasonable hours and we would go get dinner by 6. Sometimes I saw full-time employees staying a bit longer, but nothing close to the infamous investment bank hours. There were many special interest mailing lists like board games that people participate in. Personally, I went rock climbing twice a week with full-timers and interns. Between that and weekly intern dinners or activities, I was out on most evenings. Among other things, we went to play escape the room, laser tag, bowling, went to watch a Yankees game, etc. Another fun aspect of the internship is that Jane Street arranged NYU housing for the interns, which meant most of us lived together and could hang out easily.

For more on Jane Street intern life, see <https://www.quora.com/What-is-it-like-to-be-an-intern-at-Jane-Street-Capital>

Profit center
-------------

A common concern for programmers with finance companies is that IT is a [cost center, not a profit center](http://www.kalzumeus.com/2011/10/28/dont-call-yourself-a-programmer/). I do generally agree[^1]  that it is better career-wise to be working in a company's profit center. Now as far as Jane Street is concerned, tech is also part of the company's profit center. My perspective on this matter is limited since as an intern, I haven't had to deal with any internal politics, but as far I could observe, I did not ever feel that the developers were less valued. I think the traders have higher pressure with higher upside but otherwise, traders are also [taught OCaml](https://www.janestreet.com/2013/11/18/ocaml-bootcamp/) and lots of people blur the lines between trading and developer roles, so there's no "us v.s. them".

On the topic of blurring the roles, another unique and interesting aspect of Jane Street is that it has the flattest organization structure I've seen to date. You can't really tell who the managers are unless you ask, and the answer often ends up having a tone like "That guy...on paper. We needed to fill in someone's name in the regulatory compliance form." That doesn't mean that they're a holacracy, nor that they pretend to be. Even in the absence of titles, there are people who are clearly more senior than others, easily observed by watching who gets asked for help most often. However, as far as work distribution is concerned, there wasn't much top-down directions. It felt a lot more like a marketplace with some employees raising their hands saying "we need this" and other employees raising their hands saying "I'll take ownership of that and build it".

Is that necessarily a good thing? I don't know, organizational culture isn't exactly a topic where there's a lot of consensus. This could be debated in management classes all day long. However, I feel like it's a pretty good system for empowering developers.

While having a flat, casual culture is not what's typically associated with finance, that's only because most people typically associate finance with big Wall Street banks, and maybe some hedge funds. Many proprietary quantitative finance firms also have a flat & casual culture. The unique part of Jane Street is that they are probably the quant firm with the highest emphasis on hiring and training new grads. As I fall into the bucket of new grads, this is obviously something that appeals to me.

Thinking fast
-------------

One notable aspect of Jane Street's culture is that employees, especially the interns, bet a lot with each other all the time, on random things.

For example, I once had dinner with 5 other interns, and we bet actual money on the sum total number of countries represented by passport stamps in our passports[^2]. If each stamp is worth a dollar and there are X stamps, then you can buy or sell a contract worth X$. Someone offered "at 26" which meant they were willing to sell an obligation to pay X, at 26$. I bought the contract, which meant that my profit would be (X - 26) and thus, that I expected the contract to be worth more than 26$. I thought 26$ was a good deal because I had an advantage: I knew I had stamps from 10 different countries, which meant the five other people only needed to average ~3 countries in each of their passports. I thought it was likely given that one of them was an international student from Singapore and probably had as many stamps as I did. Unfortunately, that intern has just renewed his passport and no one else had traveled much. There ended up being 25 stamps, so I lost a dollar.

The traders also play [betting games](https://www.janestreet.com/2014/04/22/figgie/) to learn trading concepts. In general, it's an accepted part of the culture for people to propose a bet at any time.

It took me some time to get used to being asked to bet, in addition to learning specific betting terminology (X bid, at Y, make a market Z wide, etc). I felt ambivalent about this at first, but I realized it had one major positive impact on the culture: because people can always ask you how much you're willing to bet on any claim that you make, it _incentivizes people to be very accurate in their degree of confidence_. That doesn't mean you always have to be right (an emphasis on being right would degenerate into a shouting match), but rather, it means a willingness to admit that you're only 80% sure.

This is perhaps the aspect of Jane Street's culture that I liked the most. In most other places, there's value in being slightly to significantly overconfident. However, a large part of me values what I call "understanding how the world works" and I value being able to admit and discuss ways in which we could be wrong. It's a very hard thing to do. I fail at it _all the time_. So I appreciate how honest the people there I talked to were, in the sense of self-awareness. They _know what they don't know_[^3].

We had a lot of fun games aimed at improving our critical thinking. One day, we had a contest called Estimathon, where we were asked to guess the value of things like "lowest price of oil in the last 5 years" and "number of tires produced in the US in 2015". The narrower the range of the guess, the better your score. I was not good at all at those games, but it was fun and educational.

Thinking slow
-------------

Being able to think fast is useful to react quickly to unexpected events, which happen rather frequently in the markets. In day-to-day work however, Jane Street is quite willing to do things well, even if it means slowly.

For one thing, I was encouraged to write very good code. My projects went through multiple cycles of code review which made the process feel a little slow but every time, I received legitimately great and constructive reviews and the end result was always an interface that was much more clear and an implementation that was more concise. Since this seems to be common across the company, most of the codebase was clean and understandable. To say that there was no technical debt would be a lie as every company has technical debt, but it was the most enjoyable codebase I've ever worked with, and the first time that I touched a codebase that I would call "beautiful".

People at Jane Street are also quite good at taking the time to investigate and search for the best solution. One example is that a lot of ideas are taken from academia, but only The Good Parts™. The [Incremental library](https://github.com/janestreet/incremental) is an example of one, and adding a thin-wrapper over it to make an Elm-like [UI library, Incr Dom](https://github.com/janestreet/incr_dom) that's a joy to use is another. During the internship, we also had a weekly paper seminar where interns would volunteer to present systems & networks papers.

There's a famous quote from Blaise Pascal that I like a lot: _If I had more time, I would have written a shorter letter_, which I now realize applies equally well to coding as to writing. The combination of being open to new ideas, and the emphasis on understanding problems clearly, helped make the Jane Street internship a great learning experience.

Incentives and cultures
-----------------------

The astute reader will observe that much of the things I like about Jane Street are things that you would expect given the business and hiring incentives of being in finance. Sudden events in the markets require people to be able to react quickly. Trading requires more self-awareness and knowledge of psychology on a day-to-day basis than tech because the cost of being wrong is higher. There's value to being the best, meaning there's value to searching carefully for good solutions.

Jane Street is a liquidity provider: they help the market run more smoothly and help people make trades. They operates entirely on public markets. They're a rare type of company that has no product to sell directly to external clients[^4]. Having little for salesmanship, it becomes much easier to eliminate the need for chest-thumping displays of confidence, which allows more honesty and directness. On the other hand, while Jane Street is one of the most open finance companies and routinely blogs about their tech stack, they can't quite match tech companies who are under significantly less scrutiny.

Companies are still companies, and I do believe their culture can only be as good as their incentives will allow them to be. The shape of the upper-bound on what a good culture looks like is still limited by the needs of the company. That being said, it's not possible to reach that upper-bound without a lot of effort, and I was quite impressed by the care Jane Street put into its culture. It's as good as any other, just different and they're less vocal about it.

-----------------------------------

[^1]: Whatever that may be worth: I'm just a lowly intern that repeats what other more enlightened Hacker News commenters say

[^2]: To be more precise, each country could only count at most once in each passport. That is, if I have 2 entry stamps to the US and 2 exit stamps from the US, those 4 stamps only count for one. However, if 4 interns all have stamps to Mexico, then Mexico is counted 4 times, not one.

[^3]: (Addendum August 2017): "Knowing what you don't know" is an ideal that I keep striving for. A year after the internship, I'm still appreciating how non-trivial this is. It's not merely about being well-educated, smart or rational. Those qualities can easily cause overconfidence and [loss of self-awareness](http://digitalfreepen.com/2017/06/11/beliefs-and-emotions.html) that goes against that ideal. But at Jane Street, everyone is smarter than you, and everyone can ask you to bet on your claim, a very effective calibration tool.

[^4]: This is almost true: they offer an order execution service called JSES, but that department is isolated from the rest of the company.
