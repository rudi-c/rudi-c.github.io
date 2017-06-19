---
title: Porting to Jekyll
disqus: y
---
I just ported this website, which used to be hosted on webhostingpad and run on Wordpress, to be hosted on [Github itself](https://github.com/rudi-c/rudi-c.github.io) and generated with [Jekyll](http://jekyllrb.com/).

I did this over 3-4 days, although the total amount of work involved was closer to a single full day (I've been moving and unpacking in my new apartment at the same time).

If you've never heard of Jekyll before, it is a static webpage generator. That is, you write content (either directly with HTML or in [Markdown](http://daringfireball.net/projects/markdown/) format), add some tags and configurations, and it will generate a static webpage (only HTML, CSS and Javascript files). In contrast, Wordpress stores content in databases and generates pages on-demand using PHP.

**Motivation**

This approach was appealling for several reasons. First, static webpages are faster to load. Whereas loading a page in Wordpress would require fetching a post via SQL, creating the page via a PHP script, then sending the resulting webpage to the user, I can simply send the page to the user directly. Because the website is only made of static pages, it can also be hosted for free with [Github pages](https://pages.github.com/) which is faster than my previous webhost. That's 50$/year saved - all I need to do is pay for the domain name.

I started by forking muan's [scribble repo](https://github.com/muan/scribble), which has a very nice minimalist Jekyll theme. One area where Wordpress has the advantage is the countless themes created over the years, whereas Jekyll is quite new and only has a few dozen. However, because Wordpress supports a number of widgets like "Recent comments", the themes are usually designed around them. While those can be disabled to achieve a minimalist look, theme design assumes that they will be enabled (and hence, resulting in a multi-column layout) and the result is not as clean.

Porting the content from Wordpress was a simple matter of exporting the XML file, and running the following command :

```bash
ruby -rubygems -e 'require "jekyll-import"; JekyllImport::Importers::WordpressDotCom.run({ :source => "digitalfreepen.wordpress.2014-04-30.xml" })'
```

**Writing**

I had many permalinks coded in my posts and pages, which needed to be changed. I ran a little bash script to convert all image links and manually dealt with inter-page links. This shows another advantage of Jekyll's static page generation approach.

As all files are stored locally on my computer, I can use my favorite text editor (Sublime Text in Vintage Mode) and all of Unix's utilities (grep, sed, etc). This is much better than using Wordpress' clunky editor. While more friendly to the average user, it is not very well suited for developers. Here, I am writing my posts while using version control just as I would for any programming projects.

**Plugins**

None of my plugins would be available, and the conversion generates a lot of wordpress metadata which I no longer need. Going through all the posts and pages to make sure everything looked nice required some time - fortunately, my website is still quite small, so it wasn't too bad.

Some plugins which I needed came built-in with Jekyll, such as syntax highlighting and Google analytics. Other required some more work, but nothing was very truly time consuming. LaTeX formatting could be obtained by simply including [MathJax](http://www.mathjax.org/), similarly for opening up images with [Lightbox](http://www.lokeshdhakar.com/projects/lightbox2/?u=9). The Haiku plugin for music player could be replaced with a simple HTML5 player.

Comments are trickier to handle, due to the lack of a database to store and display them dynamically. The standard solution is to use the [Disqus](http://disqus.com/) platform, which embeds commenting into the website via Javascript.

The rest was mostly small tweaks to the CSS to configure the webpage to my own tastes.

**Caveats**

As noted by others on the web, Jekyll isn't perfect. Previewing a post requires recompiling the entire website, which can be slow as the website gets larger.

Because my website is now repository-based, it is also more difficult to write posts on the fly, especially on a computer where I do not have all my developer utilities set up.

Additionally, updating plugins will require more work than simply pressing the "update" button.

Fortunately, in my situation, these are just minor inconveniences. My website is small and is unlikely to grow into thousands of pages. I rarely need to write and publish posts urgently, and do not require the latest gadgets.

And there we go! I am not a web developer and usually go with the path of least effort when it comes to websites, but the process of converting to Jekyll was quite fun and well worth the time invested.
