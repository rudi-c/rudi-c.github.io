---
title: Consistent distance fields for ray marching
date: 2017-06-10 12:00:02
layout: post
type: post
disqus: y
published: false
---

$$
\newcommand{\norm}[1]{\left\lVert #1 \right\rVert}
$$

Introduction
------------

The classical way of writing a ray tracer represents objects in your scene with a triangle mesh. You then shoot some light rays out of your camera and do some algebra to see if it intersects with any triangles.

In recent years, an alternative to triangle-based ray tracing has emerged. While slightly less general, it's fast enough to ray-trace scenes in real-time. It's been popular in the hobbyist community for being able to produce cool results with few lines of code. The key is to use something called a ["distance field"](www.iquilezles.org/www/material/nvscene2008/rwwtt.pdf).

A distance function \\( D(x,y,z) \\) tells you, for any point \\( (x,y,z) \\) in space, how far the *closest* object is. It doesn't tell you what direction, just the distance to the closest object. Using such a function, however, makes ray marching really easy. You start the ray at the position of the camera. You calculate \\( d = D(x,y,z) \\). This tells you that you can move the ray forward by distance \\( d \\) without hitting any object. Repeat this process until you get within some epsilon distance of the object.

<center><img src="/images/2017/distanceestimate.png" width="400"/></center>

The code for this process is equally simple:

```glsl
float castRay(vec3 pos, vec3 rayDir) {
    float dist = 0.0;

    for (int i = 0; i < ITERATIONS; i++)
    {
        float res = distanceFn(pos + rayDir * dist);
        if (res < EPSILON || dist > MAX_DIST) break;
        dist += res;
    }

    return dist;
}
```

How do you find these distance functions? Constructing them for some primitives is very simple. Here is a sphere and the distance function of a sphere:

[ INSERT IMAGE ]

```glsl
float distanceSphere(vec3 pos, float radius)
{
    return length(pos) - radius;
}
```

You can find many more examples of primitive shapes, as well as how to combine them and modify them, on [Inigo Quilez's website](http://www.iquilezles.org/www/articles/distfunctions/distfunctions.htm).

It can be difficult, however, to create distance functions for complex shapes using only primitive operations. What people will often do in practice is to create functions that give you an estimate of the distance to the closest object. For example, I've obtained the funky-looking shape on the left by using the distance function the right.

[ INSERT IMAGE ]


```glsl
float distanceFunkySphere(vec3 pos, float radius, float frequency)
{
    float noise = sin(pos.x*frequency)*sin(pos.y*frequency)*sin(pos.z*frequency);
    return length(pos) - radius + noise;
}
```

Where the original distanceSphere function gave me the exact distance to the closest object, the new `distanceFunkySphere` function doesn't do that. It gives me an estimate to the distance of *some surface* (that's no longer just a sphere). But my ray marching code never needed the exact distance to begin with, since it gets closer to the surface step by step.

Finally, you can render this super fast because each of these ray marching procedures on distance functions can be evaluated independently for each pixel on the screen (you just change the ray direction). This is the kind of work that the GPU is best at!

If this is new to you so far and you find this interesting, I recommend taking a look at cool demos on [Shadertoy](www.shadertoy.com) and exploring [Inigo Quilez's website](www.iquilezles.org/index.html) who gets a lot of credit for popularizing this technique. If you're already familiar with distance field ray marching, read on, as I'm going to get into some technical details that are important for producing good distance functions.

Overstepping
------------

The example above where I multiplied some sin functions and added it to a distance function of a sphere to get a sphere with bubbles should feel a little familiar to you if you're acquainted with the hobbyist community that uses distance functions. You do some random math operations, get something physically incorrect, stick some random constants for adjustment, wave your hands and say "hey, the result looks nice!".

A friend of mine, [Veit Heller](https://veitheller.de/) coined a good term for this: **voodoo math**.

Getting a physically incorrect result isn't always a problem. You could, for example, divide your distance function by 2. It'll never answer the question "how far is the closest point?" correctly, but at worst it'll take twice as many steps for ray marching to hit the surface of the object.

Problems occur when your distance function gives you a result that's too large. Then you might take a ray marching step past the surface of your object.

[ INSERT EXAMPLE ]

This kind of overstepping will either fail to render thin objects (jump past it) or render the inside of an object, leading to weird results.

To see how this is important, consider the animation below. On the left side, I'm ray marching 25% faster than the safe "speed limit" (more on that in a second). On the right side, I have the reference, correct image. If you squint your eyes and look carefully at the surface as it's moving, you should see some "ripples" that appear at random times. That's caused by overstepping.

[ EMBED SHADERTOY ]

I used this particular shape as an example since it's used in the [primitives demo](https://www.shadertoy.com/view/Xds3zN) I noticed that the rippling happens as the object gets close to the camera.

Preventing overstepping
-----------------------

How do you guarantee that overstepping won't happen? A useful heuristic is to look at how fast the function changes. If the *magnitude of the gradient of the function is less or equal to one everywhere that it's defined*, then you will never overstep.

To get an intuition of how this is true, consider the one-dimensional case, where \\( d(x) \\) is the distance to a point at \\( x = 0 \\). Then the line \\( d(x) = x \\) is the maximum allowed value of \\( d(x) \\) and has gradient (derivative) equal to 1 everywhere except at \\( x = 0 \\) where it's not defined. If the gradient can only be smaller, \\( d(x) \\) can also only be smaller.

[ INSERT EXAMPLES (HAND DRAWN?) ]

This is a rather strong condition. You could have functions that are consistent distance fields (that do not overstep) that have a large gradient in some small area that doesn't matter, like the one below.

[ INSERT EXAMPLE ]

In that case, dividing by the gradient magnitude would be unnecessarily conservative. However, if we start adding it to other distance functions, than that small area with large gradient suddenly starts to matter.

[ INSERT EXAMPLE ]

In the case of our sin noise function, that is what we do.

Anyway, what is the gradient of our noise function? Recall that it's defined as:

$$
n(x, y, z) = sin(wx)*sin(wy)*sin(wz)
$$

[ INSERT CALCULATIONS HERE ]

So the gradient of \\( n(x, y, z) \\) is at most \\( w \\), the noise frequency. That means that \\( \frac{n(x,y,z)}{w} \\) is a distance function guaranteed not to overstep.

But wait, the distance function that we used was \\( d(x,y,z) = d_{sphere}(x,y,z) + d_{noise}(x,y,z) \\)!

The gradient of d_sphere is exactly 1 everywhere (exercise for the reader). We can use the triangle inequality to get that \\( \norm{\nabla d(x,y,z)} <= \norm{\nabla d_{sphere}(x,y,z)} + \norm{\nabla d_{noise}(x,y,z)} = 1 + w \\). So it suffices to divide \\( d(x,y,z) \\) by \\( (1 + w) \\). Now, using that distance function, we are guaranteed not to overstep.

In practice, we adjust the strength of the noise component by using linear interpolating \\( d(x,y,z) = (1 - ratio) * d_{sphere}(x,y,z) + ratio * d_{noise}(x,y,z) / w \\). In GLSL, this can be done with the `mix` function.

Useful properties of gradients and gradient maximums
----------------------------------------------------

Triangle inequality

Fast ray marching
-----------------

The method we used to find a scaling factor for our distance function uses the maximum of the magnitude of the gradient as well as the triangle inequality. It gives us a conservative estimate. This means that we are probably overestimating the scaling factor and marching slower than we need to. Can we do better? See my next blog post.
