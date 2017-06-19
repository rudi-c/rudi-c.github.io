---
title: Learned at Dropbox - 1st internship, Carousel iOS team
date: 2015-10-12 00:00:01
disqus: y
---

This is one of four blog posts on my experiences interning at Dropbox in Fall 2014 and Summer 2015. Read more about [my second internship](/2015/10/12/dropbox-second-internship.html), [maximizing signal in interviews](/2015/10/12/dropbox-interviews.html) and [the social, cultural and business aspects](/2015/10/12/dropbox-misc.html).

In my first internship at Dropbox, I was assigned to work on the Carousel iPhone app. In a nutshell, [Carousel](https://carousel.dropbox.com/) is a photo gallery app that auto-uploads your photos to the cloud and allows quick access to any of your photo stored in Dropbox. My first project would be high-resolution zooming on images stored in the cloud, as the app originally displayed only a screen-size thumbnail.

<center><img src="/images/2015/10/carousel_ios.png" width="350"/></center>

This was an interesting project because I got to design and implement the entire feature while keeping in mind the many practical constraints that go into doing it well. The simple approach would be to download just the higher resolution image and display it. Then I’d be done in very little time. However, the full image could be arbitrarily large and downloading the entire file could be very bandwidth intensive. In a mobile app, bandwidth is a limited resource. Furthermore, why download the full-image if the user just zooms into a portion of the screen? Therefore, I split the image into tiles and fetched the tiles on a per-need basis.

Among other projects, I also helped ship Carousel for iPad by maximizing the usage of the screen real estate. Photos are grouped into events. If all the images were the same size, then events that only have a few images would be left with whitespace. Those projects were interesting exercises in understanding the distinction between doing something and doing it well, and I learned that the culture at Dropbox leans strongly towards doing it well. They call it “sweating the details”.

From doing it to doing it well
------------------------------

A photo gallery app sounds mundane, but as I learned more about its functionality and dove into the codebase, I quickly realized that Carousel was far from “just a photo gallery”. There’s a [series of 3](https://blogs.dropbox.com/tech/2014/04/building-carousel-part-i-how-we-made-our-networked-mobile-app-feel-fast-and-local/) [blog posts](https://blogs.dropbox.com/tech/2014/08/building-carousel-part-ii-speeding-up-the-data-model/) [describing the engineering](https://blogs.dropbox.com/tech/2014/10/building-carousel-part-iii-drawing-images-on-screen/) behind Carousel that reveal the magic behind the scenes.

In a nutshell, the two technical aspects of Carousel I was most impressed by are the performance and the handling of edge cases. One of the nice features of Carousel is that I can quickly scroll through my entire photo library to look at my old photos. This sounds simple but when you have thousands of pictures going across the screen, even decoding the JPEG becomes a bottleneck. All kinds of prefetching and caching techniques went into the scrollbar alone.

Carousel is also a view into both the local photo gallery and the photos stored into the cloud. By having both, along with the ability to hide photos, the edge cases just explode. What happens if the user deletes a local photo? If the user deletes a photo on the server side? Both at the same time?

While I didn’t work on the main Dropbox application that everybody uses, Carousel gave me a good view into the complexity of the problems Dropbox needs to tackle. When all your products need to consider concurrent modifications (read/write/delete) of the data, everything becomes a couple orders of magnitude harder (the best way to get a sense of this type of problem is to read about [Operational Transformations (OT)](https://en.wikipedia.org/wiki/Operational_transformation)). However, when done right, the experience can be very nice and seamless, and the typical feedback users give is that they really appreciate that Dropbox just “works”.

Code sharing
------------

The other aspect of working on Carousel iOS which was very educational is the unusual architecture of the codebase which works out great. Half of the iOS and Android app’s code is a shared layer of C++. To interface with C++ from Objective-C and Java, Dropbox developed an open-source [language interface generator](https://github.com/dropbox/djinni).

It is desirable to share code across mobile platforms. How can it be done? You could write a [Java to Objective-C compiler](https://github.com/google/j2objc). But let’s assume that you don’t have unlimited resources [^0]. You could go with a portable approach like Web or one of the many cross-platform toolkits out there. However, it will be difficult to achieve a native feel, it will not have the same polish. Or you could share some native code (native in the sense of light on the runtime) [^1].

A shared layer in C++ also has performance benefits, and C++11 with smart pointers is reasonably ergonomic to work with. I also found that having a distinct codebase for shared code forces the design of better abstractions. For example, in the context of MVC, the C++ code takes on the role of model, and it’s harder to slip up by putting model logic in the view or controller, and vice-versa.

Finally, most companies would not have chosen this approach because the tools did not exist and had to be developed. This is the great thing about working at a top tech company. Risks are taken and new approaches to software engineering are discovered.

-------------------------------------------

[^0]: I’m curious as to how well that approach works. Among other complexities, making a transition from tracing garbage collection to reference counting can be very hairy, from my experience working on compilers. There’s always ways to make it work, but at the cost of developer effort.

[^1]: For high-performance apps like Carousel, latency induced by GC pauses is significant. The shared layer should not be in a language with a tracing GC. Having two separate garbage collectors kicking off at random times is going to lead to very challenging scenarios.
