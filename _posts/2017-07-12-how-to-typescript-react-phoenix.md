---
title: How to use React with Typescript in Phoenix
date: 2017-07-12
disqus: y
---

Introduction
------------

This is a tutorial on setting up an (Elixir) Phoenix project that can be used to write React apps that use Typescript, a combination of nice things (IMO). Previous tutorials have been written to use [Phoenix with React](https://medium.com/@diamondgfx/phoenix-v1-1-2-and-react-js-3dbd195a880a) or [Typescript with React using Webpack](http://blog.tomduncalf.com/posts/setting-up-typescript-and-react/) but not all 3 together. I ran into a few difficulties while setting it up myself (namely because Phoenix uses Brunch by default rather than Webpack) so here's a guide on how to do it to make things faster for you!

Versions that I've used
-----------------------

**Phoenix**: v1.2.4

**NPM**: v3.10.10

**Brunch**: v2.10.9

**Typescript**: v2.4.1

**React**: v15.6.1

Phoenix
-------

As usual, start by creating a new Phoenix project and install the dependencies. This is just here for convenience, make sure to follow the [official docs](http://www.phoenixframework.org/docs/up-and-running) on how to setup postgres and other considerations.

<div class="highlighter-rouge">
<pre class="highlight code">
$ <b>mix phoenix.new typescript_react_phoenix</b>
...
* creating typescript_react_phoenix/web/views/layout_view.ex
* creating typescript_react_phoenix/web/views/page_view.ex

Fetch and install dependencies? [Yn] Y
* running mix deps.get
* running npm install && node node_modules/brunch/bin/brunch build

We are all set! Run your Phoenix application:

    $ cd typescript_react_phoenix
    $ mix phoenix.server

You can also run your app inside IEx (Interactive Elixir) as:

    $ iex -S mix phoenix.server

Before moving on, configure your database in config/dev.exs and run:

    $ mix ecto.create
</pre>
</div>

You can test if it worked:

```
mix ecto.create
mix phoenix.server
```

If you want, you this could also be a good time to setup your git repository.

```
git init .
git add .
git commit -m "Initial commit"
```

Setting up React
----------------

Let's start by setting up just React, so that have an intermediate step that we can test, which makes things easier to figure out if anything goes wrong.

First, as you probably know, React uses JSX syntax which allows embedding HTML inside Javascript code. Also, React is written in ES6 nowadays, so we typically use Babel to compile the ES6 JSX down to plain ES5 to make sure it runs on all browsers. So we'll need to install React and the Babel plugin that does that (Babel itself already comes by default with Phoenix).

```
npm install --save react react-dom babel-preset-react
```

Then let's tell Babel to use it. Add the following in your `.brunch-config.js`

<div class="highlighter-rouge">
<pre class="highlight code">
plugins: {
  babel: {
    <b>presets: ["es2015", "react"],</b>
    // Do not use ES6 compiler in vendor code
    ignore: [/web\/static\/vendor/]
  }
},
</pre>
</div>

Then, we can add a React component to our page. First, let's make an HTML node that React will get rendered from. You can replace the default contents of `web/templates/page/index.html.eex` with just:

```html
<div id="react-main"></div>
```

Let's create a simple React component that we want to show in `web/static/js/hello.jsx`.

```js
import React from "react"

export default class HelloJSX extends React.Component {
    render() {
        var type = "JSX";
        return (<h1>Hello from {type}!</h1>)
    }
}
```

Finally, to show that component, we need to render it under the `react-main` div. Add the following to the end of `web/static/js/app.js`:

```js
import React from "react"
import ReactDOM from "react-dom"

import HelloJSX from "./hello"

var main = document.getElementById("react-main")
if (main) {
    ReactDOM.render(
        <HelloJSX/>,
        main
    )
}
```

And this should just work! Go to your browser and see if it looks as expected.

<center><img src="/images/2017/phoenix_hello.png" width="500"/></center>

Typescript
----------

Getting Typescript to compile our code is a bit work, though it's not that bad. First, have Typescript installed globally:

```
npm install -g typescript
```

It doesn't hurt to have it locally too:

```
npm install --save-dev typescript
```

Now that we have an additional compilation step, we'll want to put it in the brunch pipeline too. Basically, we're going from `.tsx -> .jsx -> .js`.

First, update the Brunch version in `package.json` to `2.10.9`:

```
"devDependencies": {
 ...
 "brunch": "2.10.9",
 ...
}
```

This is important because at the time of writing, the latest Phoenix version (`1.2.4`) ships with `2.7.4` which doesn't have the `targetExtension` API. This means that the `.tsx` files' extension doesn't change after compilation. Babel ends up ignoring them, and we end up with a syntax error because there's still HTML elements left that can't be parsed in a plain Javascript file.

> Phoenix v1.3.0 will be using the newer version of Brunch.

Now, it *also* turns out that `typescript-brunch`, the Brunch plugin for Typescript, doesn't use `targetExtension`. I've forked the repository and until my PR is merged, you can add my repository in `package.json`. Note that Brunch will execute plugins in the order that they show up in `package.json`, so it's very important that it is placed before `babel-brunch`! Your `package.json` should contain this:

```
"devDependencies": {
  "typescript": "^2.4.1",
  "typescript-brunch": "github:rudi-c/typescript-brunch",
  "babel-brunch": "~6.0.0",
  "brunch": "2.10.9",
  "clean-css-brunch": "~2.0.0",
  "css-brunch": "~2.0.0",
  "javascript-brunch": "~2.0.0",
  "uglify-js-brunch": "~2.0.1"
}
```

Then `npm install`. You can run `mix phoenix.server` now to check that everything still works.

We're getting close! Let's configure the Typescript compiler to output ES6 and JSX. This allows the output of the Typescript compiler to be very close to the original source, with just the type annotations stripped away. It'll be more consistent with other JSX files we might add into the project (e.g. if you copy over an older file without type annotation) and Babel will take care of the rest. Otherwise, if you let Typescript compile to ES5, you could run into incompatibilities such as how module imports with `require` are handled. Add the following options in `brunch-config.js`.

```
plugins: {
  babel: {
    ...
  },
  brunchTypescript: {
    target: "ES2015",
    module: "ES2015",
    jsx: "preserve"
  }
},
```

The Typescript compiler has other options that you may want to add, but I'll keep the tutorial simple. Make sure to take a look at the [docs](https://www.typescriptlang.org/docs/handbook/compiler-options.html). Also note that the options in `brunch-config.js` will override any in `tsconfig.json`, the usually place where compiler settings go.

For our last bit of setup, install type definitions for React and ReactDOM:

```
npm install --save-dev @types/react
npm install --save-dev @types/react-dom
```

Writing a Typescript component
------------------------------

To test if this all works, let's create a Typescript component in `web/static/js/world.tsx`.

```js
import React from "react"

export default class WorldTSX extends React.Component<any, any> {
    render() {
        var type: string = "TSX";
        return (<h1>{type} World!</h1>)
    }
}
```

It doesn't do much, but I've added two type annotations to try it out. And let's change `web/static/js/app.js` to show this component

```js
import HelloJSX from "./hello"
import WorldTSX from "./world"

var main = document.getElementById("react-main")
if (main) {
    ReactDOM.render(
        (<div>
           <HelloJSX/>
           <WorldTSX/>
         </div>
        ),
        main
    )
}
```

Refresh, and we're done!

<center><img src="/images/2017/phoenix_world.png" width="500"/></center>

If you got lost along the way, or would prefer to use a template that already works, you can find a barebone project here: [https://github.com/rudi-c/typescript-react-phoenix](https://github.com/rudi-c/typescript-react-phoenix)

Next steps
----------

Make sure to also take a look at [Tom Duncalf's tutorial](http://blog.tomduncalf.com/posts/setting-up-typescript-and-react/) on setting up Typescript in Webpack. He explains various flags of Typescript in more depth, talks Visual Studio Code, and provides a few other suggestions to make Typescript work more smoothly.

If you intend to use Visual Studio Code for Typescript (it works great!), you may also be interested in using it for Elixir using the [vscode-elixir plugin](https://marketplace.visualstudio.com/items?itemName=mjmcloug.vscode-elixir).

Since you may end up building a SPA (Single-Page App) now that you're using React, you'll probably end up using the `/api` endpoint much more in `router.ex`. You might even find it easier to use channels for everything.

Enjoy! Let me know in the comments if you have any questions.
