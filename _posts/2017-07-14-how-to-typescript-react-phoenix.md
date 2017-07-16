---
title: How to use React with Typescript in Phoenix
date: 2017-07-14
disqus: y
---

Introduction
============

This is a tutorial on setting up an (Elixir) Phoenix project that can be used to write React apps that use Typescript, a combination of nice things (IMO). Previous tutorials have been written to use [Phoenix with React](https://medium.com/@diamondgfx/phoenix-v1-1-2-and-react-js-3dbd195a880a), [Typescript with React using Webpack](http://blog.tomduncalf.com/posts/setting-up-typescript-and-react/), or [just Webpack](http://matthewlehner.net/using-webpack-with-phoenix-and-elixir/) [in Phoenix](https://lpil.uk/blog/integrating-webpack-with-phoenix/), but not all 3 together. I ran into a few difficulties while setting it up myself so here's a guide on how to do it to make things faster for you!

I'll try to keep this tutorial up-to-date, but the web ecosystem changes quickly and things break every few months. A lot of the tutorials I read are recent, but they're already out of date (e.g. written for Webpack 1). Let me know in the comments below if there's something to update!

Versions that I've used
-----------------------

**npm**: v3.10.10

**Phoenix**: v1.2.4

**Webpack 2**: v3.2.0

**Typescript**: v2.4.1

**React**: v15.6.1

Phoenix
=======

As usual, start by creating a new Phoenix project and install the dependencies. This is just here for convenience, make sure to follow the [official docs](http://www.phoenixframework.org/docs/up-and-running) on how to setup npm, postgres and other considerations.

If you already have a Phoenix project, skip to the next section.

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

Webpack
=======

The first thing we need to do is setup Webpack as our build system.

> What's a build system? Think of it as a way to package and transform all your code in a way that can be sent to the user's browsers. Once upon a time, we would write Javascript and CSS and sent it directly to the user. However, as our tooling progressed, people have using more libraries and have created more powerful languages such as JSX, Typescript, SCSS, etc that need to be transformed into simplified versions that can be sent to the user.

This means that we don't need the default Brunch system anymore, and we can remove it.

```
rm brunch-config.js
```

Remove all Brunch dependencies in `package.json` (in a new project, this should leave `devDependencies` empty).

And install Webpack and some loaders and plugins we'll need (more on that in a second)

```
npm install --save-dev webpack webpack-notifier
npm install --save-dev css-loader style-loader file-loader
npm install --save-dev extract-text-webpack-plugin copy-webpack-plugin
```

Setting up Webpack will require us to do extra work compared to just using Brunch, but Brunch is fundamentally designed in a way [incompatible with Typescript](/2017/07/12/how-to-typescript-react-phoenix-1). Webpack is currently well-maintained and is a better future-proof solution.

> Why not create the project without brunch using `mix phoenix.new --no-brunch`? It's actually easier to create it with Brunch and remove it, because it also sets up other parts of the project like directory structure in a particular way. This also allows this tutorial to be used with existing Phoenix projects.

Configuring Webpack
-------------------

Our first goal will be to display the default Phoenix app using Webpack. Update `package.json` to call Webpack instead of Brunch.

```json
{
  ...
  "scripts": {
    "deploy": "webpack -p",
    "watch": "webpack --watch-stdin --progress --color"
  },
  ...
}
```

Change the `watchers` in `config/dev.exs` to use `npm`.

```elixir
  ...
  watchers: [npm: ["run", "watch"]]
```

And create a file called `webpack.config.js` in the project root directory with the following contents:

```js
const path = require("path")
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin")

const config = {
    entry: ["./web/static/css/app.css", "./web/static/js/app.js"],
    output: {
        path: path.resolve(__dirname, "priv/static"),
        filename: "js/app.js"
    },
    resolve: {
        extensions: [".ts", ".tsx", ".js", ".jsx"],
        modules: ["deps", "node_modules"]
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    use: "css-loader"
                })
            },
            {
                test: /\.(ttf|otf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/,
                loader: 'file-loader?name=fonts/[name].[ext]'
            },
        ]
    },
    plugins: [
        new ExtractTextPlugin("css/app.css"),
        new CopyWebpackPlugin([{ from: "./web/static/assets" }])
    ]
};

module.exports = config;
```

You can run `mix phoenix.server` now and you should be able to see content in `localhost:4000`. However, the layout is wrong - there's no CSS!

> There's a lot going on in there! Let's explain what all of this is for:
> - We import some plugins whose main job is to copy files from one directory to another. Normal Webpack setups don't need this, but our folder structure is different within Phoenix.
> - We have two entry paths: one for Javascript and one for CSS. Everything imported by `app.js` will eventually end up in a single file that contains all the dependencies and gets sent to the client. Similarly, everything import in `app.css` will end up in the CSS that gets sent to the client.
> - We want Webpack to only process Javascript/Typescript code dependencies. Normally, the field `modules` is set to `node_modules` by default and we don't need to specify it. But Phoenix also installs some of its own dependencies in `deps/` and some of those dependencies contain Javascript that the application needs, such as `phoenix_html`.
> - We have rules to bundle CSS and static assets. That's where the loaders come in handy, they handle all the processing.

CSS
---

Previously, Brunch would package everything in `web/static/css` into a single CSS file. In contrast, Webpack will only package CSS files recursively imported by `app.css`.

> Keeping that in mind, if you don't want any of the default CSS (including Bootstrap) that comes with Phoenix, feel free to skip this section.

All the CSS that comes with Phoenix is in `web/static/css/phoenix.css` so we need to import that in `web/static/css/app.css`.

```css
@import "phoenix.css"
```

But if you try to run your server now, you'll get a Webpack error.

```
ERROR in ./node_modules/css-loader!./web/static/css/phoenix.css
Module not found: Error: Can't resolve '../fonts/glyphicons-halflings-regular.eot' in '/home/rudic/Documents/elixi
r/typescript_react_phoenix/web/static/css'
 @ ./node_modules/css-loader!./web/static/css/phoenix.css 6:3414-3466 6:3484-3536
 @ ./node_modules/css-loader!./web/static/css/app.css
```

This is because Phoenix doesn't come with the fonts that Bootstrap wants by default, and Webpack doesn't resolve them like Brunch does. As [suggested by lpil](https://lpil.uk/blog/integrating-webpack-with-phoenix/), you can just download them.

```
mkdir web/static/fonts
cd web/static/fonts
curl -O 'https://raw.githubusercontent.com/twbs/bootstrap/master/fonts/glyphicons-halflings-regular.eot' \
     -O 'https://raw.githubusercontent.com/twbs/bootstrap/master/fonts/glyphicons-halflings-regular.svg' \
     -O 'https://raw.githubusercontent.com/twbs/bootstrap/master/fonts/glyphicons-halflings-regular.ttf' \
     -O 'https://raw.githubusercontent.com/twbs/bootstrap/master/fonts/glyphicons-halflings-regular.woff' \
     -O 'https://raw.githubusercontent.com/twbs/bootstrap/master/fonts/glyphicons-halflings-regular.woff2'
cd -
```

If you run `mix phoenix.server`, you should be able to see the default "Welcome to Phoenix" page now!

React
=====

Alright, next let's setup React! We'll get to Typescript later, but let's do this step by step to make any potential issues easier to diagnose.

First, you'll need to install React and Babel.

```
npm install --save react react-dom
npm install --save-dev babel-loader babel-core babel-preset-es2015 babel-preset-react
```

<br />
> What is Babel? It allows you to transpile Javascript with new features (including JSX with HTML tags that React uses) into older Javascript that's well supported by all browsers. We don't technically need Babel since the Typescript compiler can do that too, but there's a few advantages to using Babel:
> - You'll be able to use Babel plugins
> - Babel tends to support newer Javascript features faster than Typescript
> - If you mix in plain Javascript (or JSX) with Typescript files, you'll be less likely to run into issues by using Babel which makes the compilation more uniform

Let's create a file called `.babelrc` in the project root directory. This is just to configure Babel to handle React syntax and ES6 (i.e. new Javascript features).

```json
{
    "presets": ["es2015", "react"]
}
```

And add a rule to `webpack.config.js` to process Javascript files with Babel.

```json
module: {
    rules: [
        {
            test: /\.jsx?$/,
            use: "babel-loader"
        },
        {
            test: /\.css$/,
        ...
```

Writing a React component
-------------------------

We can test that this works by creating a very simple component in React. First, let's make an HTML node that React will get rendered from. You can replace the default contents of `web/templates/page/index.html.eex` with just:

```html
<div id="react-main"></div>
```

Make a new file `web/static/js/react-entry.jsx` with

```js
import * as React from "react"
import * as ReactDOM from "react-dom"

class HelloJSX extends React.Component {
    render() {
        var type = "JSX";
        return (<h1>Hello from {type}!</h1>)
    }
}

export default function render(node) {
    ReactDOM.render(
        <HelloJSX/>,
        node
    )
}
```

To show that component, we need to render it under the `react-main` div. Add the following to the end of `web/static/js/app.js`:

```js
import render from "./react-entry"

var main = document.getElementById("react-main")
if (main) {
    render(main)
}
```

And this should just work! Go to your browser and see if it looks as expected.

<center><img src="/images/2017/phoenix_hello.png" width="500"/></center>

> Why not put the code in `app.js` directly? Webpack doesn't like non-JS entry points.

Typescript
==========

Finally we're getting to Typescript! First, install Typescript if you don't already have it installed and packages that make it play nice with Babel and React:

```
npm install --save-dev typescript ts-loader @types/react @types/react-dom
```

It's also a good idea to install Typescript globally to be able to use it from the command-line with `npm install -g typescript`.

Next, Typescript needs to be configured, just like Webpack and Babel. Create a `tsconfig.json` file in the project root with

```json
{
  "compilerOptions": {
    "target": "es2015",
    "module": "es2015",
    "jsx": "preserve",
    "moduleResolution": "node",
    "baseUrl": "web/static/js",
    "outDir": "ts-build"
  },
  "exclude": [
      "node_modules"
  ]
}
```

There's many compiler options you might be interested in changing, but the main thing we want to configure here is to have Typescript emit ES6 code and keep the HTML in JSX files. This allows the output of the Typescript compiler to be very close to the original source, with just the type annotations stripped away. It'll be more consistent with other JSX files we might add into the project (e.g. if you copy over an older file without type annotation) and Babel will take care of the rest.

Setting `moduleResolution` to `node` is necessary otherwise the Typescript compiler won't look inside `node_modules`.

We'll also want to add a processing step in `webpack.config.js` to process `.ts` and `.ts` with Typescript, followed by Babel.

```json
module: {
    rules: [
        {
            test: /\.tsx?$/,
            ["babel-loader", "ts-loader"]
        },
        ...
```

Writing a Typescript component
------------------------------

To test if this all works, let's create a Typescript component in `web/static/js/world.tsx`.

```typescript
import * as React from "react"

export default class WorldTSX extends React.Component<any, any> {
    render() {
        var type: string = "TSX";
        return (<h1>{type} World!</h1>)
    }
}
```

It doesn't do much, but I've added two type annotations to try it out. And let's change the `render` function in `web/static/js/react-entry.jsx` to show this component

```js
...
import WorldTSX from "./world"
...

export default function render(node) {
    ReactDOM.render(
        (<div>
          <HelloJSX/>
          <WorldTSX/>
         </div>),
        node
    )
}
```

Refresh, and we're done!

<center><img src="/images/2017/phoenix_world.png" width="500"/></center>

If you got lost along the way, or would prefer to use a template that already works, you can find a barebone project here: [https://github.com/rudi-c/typescript-react-phoenix](https://github.com/rudi-c/typescript-react-phoenix/).

Next steps
==========

Make sure to also take a look at [Tom Duncalf's tutorial](http://blog.tomduncalf.com/posts/setting-up-typescript-and-react/) on setting up Typescript in Webpack. He explains various flags of Typescript in more depth, provides Hot Reloading, talks about Visual Studio Code, and provides a few other suggestions to make Typescript work more smoothly.

If you intend to use Visual Studio Code for Typescript (it works great!), you may also be interested in using it for Elixir using the [vscode-elixir plugin](https://marketplace.visualstudio.com/items?itemName=mjmcloug.vscode-elixir).

Since you may end up building a SPA (Single-Page App) now that you're using React, you'll probably end up using the `/api` endpoint much more in `router.ex`. You might even find it easier to use channels for everything.

If your project grows big, you may want to follow good software engineering practices such as using a linter and testing frameworks. You might also want to use state management tools like Redux. Additional instructions on how to set these up can be found in Microsoft's [official Typescript-React starter](https://github.com/Microsoft/TypeScript-React-Starter#typescript-react-starter).

And if you're like "wtf so much stuff" after reading this tutorial, relax by reading this [comedy piece by Jose Aguinaga](https://hackernoon.com/how-it-feels-to-learn-javascript-in-2016-d3a717dd577f) on front-end development.

Enjoy! Let me know in the comments if you have any questions.
