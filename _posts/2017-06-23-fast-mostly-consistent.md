---
title: Fast and mostly consistent distance field ray marching
date: 2017-06-23
disqus: y
---

Speed limits
------------

In [my previous blog post](/2017/06/21/consistent-distance-fields.html) on distance field ray marching, I explained how we can avoid overstepping by making sure that the distance function has gradient magnitude less than 1. This condition is especially useful when we start doing voodoo math adding distance functions together. It gives us a safe "speed limit".

In this sin noise example, this led me to conclude that I needed to divide the noise component by some factor \\( w \\) in the distance field \\( D(x,y,z) = (1 - ratio) * D_{sphere}(x,y,z) + ratio * D_{noise}(x,y,z) / w \\).

However, there is one issue that I swept under the rug. While *in theory*, you should see rendering artifacts from going above my speed limit, *in practice*, I need to step as much as **50% faster** than the mathematically-derived "speed limit" in order to see any obvious rendering artifacts.

The situation was even worse in another similar demo I created:

<center><iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/4ssfzX?gui=true&t=10&paused=true&muted=false" allowfullscreen></iframe></center>

<!--
#define MAX_DIST 4.
#define EPSILON 0.0005
#define ITERATIONS 256

// Uncomment to plot the distance to the object
// instead of using regular light-based shading
// #define RENDER_DISTANCE

// Uncomment to artificially magnify differences
// between the left side with artefacts and the
// reference right side by five times
// #define MAKE_OBVIOUS

#define NOISE_PROPORTION 0.85
#define NOISE_FREQUENCY 25.
//#define NOISE_GRADIENT_MAGNITUDE (1. * NOISE_FREQUENCY * 2.793) // max
#define NOISE_GRADIENT_MAGNITUDE (1. * NOISE_FREQUENCY * 1.32) // 95th percentile
#define SPHERE_GRADIENT_MAGNITUDE 1.
#define OVERSTEP_FACTOR 1.3

// Perlin noise function
// Adapted from https://www.shadertoy.com/view/Ms2yWz
// -----------------------------------------------------------

#define mod3_           vec3(.1031, .11369, .13787)

vec3 hash3_3(vec3 p3) {
    p3 = fract(p3 * mod3_);
    p3 += dot(p3, p3.yxz + 19.19);
    // random3 has range 0 to 1
    vec3 random3 = fract(vec3((p3.x + p3.y) * p3.z, (p3.x+p3.z) * p3.y, (p3.y+p3.z) * p3.x));
    return normalize(-1. + 2. * random3);
}

float perlin_noise3(vec3 p) {
    vec3 pi = floor(p);
    vec3 pf = p - pi;

    // 5th order interpolant from Improved Perlin Noise
    vec3 pf3 = pf * pf * pf;
    vec3 pf4 = pf3 * pf;
    vec3 pf5 = pf4 * pf;
    vec3 w = 6. * pf5 - 15. * pf4 + 10. * pf3;

    return mix(
        mix(
            mix(
                dot(pf - vec3(0, 0, 0), hash3_3(pi + vec3(0, 0, 0))),
                dot(pf - vec3(1, 0, 0), hash3_3(pi + vec3(1, 0, 0))),
                w.x),
            mix(
                dot(pf - vec3(0, 0, 1), hash3_3(pi + vec3(0, 0, 1))),
                dot(pf - vec3(1, 0, 1), hash3_3(pi + vec3(1, 0, 1))),
                w.x),
        w.z),
        mix(
            mix(
                dot(pf - vec3(0, 1, 0), hash3_3(pi + vec3(0, 1, 0))),
                dot(pf - vec3(1, 1, 0), hash3_3(pi + vec3(1, 1, 0))),
                w.x),
            mix(
                dot(pf - vec3(0, 1, 1), hash3_3(pi + vec3(0, 1, 1))),
                dot(pf - vec3(1, 1, 1), hash3_3(pi + vec3(1, 1, 1))),
                w.x),
        w.z),
    w.y);
}

float restricted_perlin(vec3 pos) {
    float perlin = perlin_noise3(pos);
    float x = abs(perlin);

    float p = 0.5;
    float q = 0.95;
    float x1 = 0.5;
    float x2 = 0.867;
    float new = 0.0;

    float a = (q*p - x1) / x1 / x1;
    float b = 1.;
    float c = 0.;
    if (x < x1) {
        new = a * x * x + b * x + c;
    } else {
        float n = - (x2 - x1) * (2. * a * x1 + b) / (q*p - p);
        float d = (q*p - p) / pow(x2 - x1, n);
        new = d * pow(x2 - x, n) + p;
    }

    return new * sign(perlin);
}

// -----------------------------------------------------------

// Distance to a sphere centered at the origin
float sdSphere(vec3 pos, float radius)
{
    return length(pos) - radius;
}


// Distance to a sphere with perlin noise perturbations
// centered at the origin.
float sdWeirdSphere(vec3 pos) {
    float noise = perlin_noise3(pos * NOISE_FREQUENCY) / NOISE_GRADIENT_MAGNITUDE;
    return mix(sdSphere(pos, 0.2) / SPHERE_GRADIENT_MAGNITUDE,
               noise,
               NOISE_PROPORTION);
}

float distanceFn(vec3 pos, bool artefacts) {
    if (artefacts) {
        return OVERSTEP_FACTOR * sdWeirdSphere(pos);
    } else {
        return sdWeirdSphere(pos);
    }
}

// Copied over from https://www.shadertoy.com/view/Xds3zN
vec3 calcNormal(vec3 pos, bool artefacts)
{
    vec2 e = vec2(1.0,-1.0)*0.5773*0.0005;
    return normalize( e.xyy*distanceFn( pos + e.xyy, artefacts ) +
                      e.yyx*distanceFn( pos + e.yyx, artefacts ) +
                      e.yxy*distanceFn( pos + e.yxy, artefacts ) +
                      e.xxx*distanceFn( pos + e.xxx, artefacts ) );
}

// Ray marching using distance-estimation
// Adapted from https://www.shadertoy.com/view/Xds3zN
float castRay(vec3 pos, vec3 rayDir, bool artefacts) {
    float dist = 0.;

    for (int i = 0; i < ITERATIONS; i++)
    {
        // More precision when the object is closer
        float precis = EPSILON * dist;
        float res = distanceFn(pos + rayDir * dist, artefacts);
        if (res < precis || dist > MAX_DIST) break;
        dist += res;
    }

    return dist;
}

// Copied over from https://www.shadertoy.com/view/Xds3zN
// setCamera(origin, target, rotation)
mat3 setCamera(vec3 ro, vec3 ta, float cr)
{
    vec3 cw = normalize(ta-ro);
    vec3 cp = vec3(sin(cr), cos(cr),0.0);
    vec3 cu = normalize( cross(cw,cp) );
    vec3 cv = normalize( cross(cu,cw) );
    return mat3( cu, cv, cw );
}

// Copied over from https://www.shadertoy.com/view/Xds3zN
vec3 shade(vec3 camera, vec3 rayDir, float dist, bool artefacts) {
    vec3 rayPos = camera + rayDir * dist;
    vec3 normal = calcNormal(rayPos, artefacts);
    vec3 ref = reflect(rayDir, normal);

    float m = 65.;
    vec3 col = 0.45 + 0.35*sin( vec3(0.05,0.08,0.10)*(m-1.0) );

    // Lighting
    vec3  lig = normalize( vec3(-0.4, 0.7, -0.6) );
    float amb = clamp( 0.5+0.5*normal.y, 0.0, 1.0 );
    float dif = clamp( dot( normal, lig ), 0.0, 1.0 );
    float bac = clamp( dot( normal, normalize(vec3(-lig.x,0.0,-lig.z))), 0.0, 1.0 )*clamp( 1.0-rayPos.y,0.0,1.0);
    float dom = smoothstep( -0.1, 0.1, ref.y );
    float fre = pow( clamp(1.0+dot(normal,rayDir),0.0,1.0), 2.0 );
    float spe = pow(clamp( dot( ref, lig ), 0.0, 1.0 ),16.0);

    vec3 lin = vec3(0.3);
    lin += 1.30*dif*vec3(1.00,0.80,0.55);
    lin += 2.00*spe*vec3(1.00,0.90,0.70);
    lin += 0.40*amb*vec3(0.40,0.60,1.00);
    lin += 0.50*dom*vec3(0.40,0.60,1.00);
    lin += 0.50*bac*vec3(0.25,0.25,0.25);
    lin += 0.25*fre*vec3(1.00,1.00,1.00);
    col = col*lin;

    col = mix( col, vec3(0.8,0.9,1.0), 1.0-exp( -0.0002*dist*dist*dist ) );

    return vec3( clamp(col,0.0,1.0) );
}

vec3 distanceShade(float dist, float minDist, float maxDist) {
    float normalized = (dist - minDist) / (maxDist - minDist);
    if (normalized < 1. / 4.) {
        float inRange = normalized * 4.;
        return vec3(inRange, 0., 0.);
    } else if (normalized < 2. / 4.) {
        float inRange = (normalized - 1. / 4.) * 4.;
        return vec3(1. - inRange, inRange, 0.);
    } else if (normalized < 3. / 4.) {
        float inRange = (normalized - 2. / 4.) * 4.;
        return vec3(0., 1. - inRange, inRange);
    } else {
        float inRange = (normalized - 3. / 4.) * 4.;
        return vec3(0., 0., 1. - inRange);
    }
}

vec4 render(vec2 uv, bool artefacts) {
    vec3 camera = vec3(cos(iTime / 4.), 0.0, sin(iTime / 4.)) * 0.75;
    vec3 target = vec3(0.0);

    // Camera-to-world transformation
    mat3 transform = setCamera(camera, target, 0.0);

    // Origin is now at the center of the screen (given camera position);
    vec3 rayDirection = transform * normalize(vec3(uv, 2.0));

    float dist = castRay(camera, rayDirection, artefacts);

    if (dist > MAX_DIST) {
        return vec4(uv, 0., 1.0);
    } else {
        #ifdef RENDER_DISTANCE
            return vec4(distanceShade(dist, 0.485, 0.8), 1.0);
        #else
            return vec4(shade(camera, rayDirection, dist, artefacts), 1.0);
        #endif
    }
}
// fragColor: 0 to 1, starting at bottom-left corner
void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    // Divide by two since we split the screen
    vec2 splitResolution = vec2(iResolution.x / 2., iResolution.y);
    float minDimension = min(splitResolution.x, splitResolution.y);
    vec2 uv = (fragCoord - splitResolution / 2.) / minDimension * 2.;
    if (fragCoord.x < iResolution.x / 2.) {
        #if defined(MAKE_OBVIOUS) && !defined(RENDER_DISTANCE)
            vec4 wrong = render(uv, true);
            vec4 correct = render(uv, false);
            fragColor = wrong + (wrong - correct) * 5.;
        #else
            fragColor = render(uv, true);
        #endif
    } else {
        fragColor = render(uv - vec2(iResolution.x / minDimension, 0.0), false);
    }
}
-->

In the demo above, instead of adding sin noise (which is too regular) to the distance function of a sphere, I add Perlin noise to the distance function of a sphere. Perlin noise is a commonly used random function that has some smoothness to it. Using numerical optimization, I previously calculated the maximum gradient of 3D Perlin noise to be around 2.793. But in this case, I need to step almost **3x more** than my "speed limit" allows to see obvious rendering artifacts.

So this "speed limit" seems rather unconvincing in practice. What's wrong?

Rare extreme cases
------------------

It all comes down to the likelihood of overstepping past the surface of an object when sampling the distance field. One way to get a sense of that is to use a Monte Carlo simulation. First, I generate 50000 random points on the sin noise function \\( \sin(x)\sin(y)\sin(z) \\) and calculate the gradient magnitude at each point. Then I plot the probability density function of getting any particular value, as well as the cumulative distribution function, see below:

<center><img src="/images/2017/perlin2d_gradient.png" width="500"/></center>

As can be seen, most points will have an average gradient magnitude. The situation is even more extreme with 3D Perlin noise:

<center><img src="/images/2017/perlin3d_gradient.png" width="500"/></center>

Although we can prove that the gradient of 3D Perlin noise can have a magnitude as large at 2.793, it's rare that a point will have gradient magnitude more than 1.5, and even rarer that this will cause a rendering artifact. This makes sense. Perlin noise is generated in cubes, each cube being configured via a unit vector at each corner, which can be represented as two angles. In order to hit the worst case, you would need a particular configuration for 16 different variables AND that extreme point would need to be near the surface of the object AND we would need to have a ray pass by that point under a restricted range of angles to see rendering artifacts. Finally, the rendering artifact needs to be significant. If it's off by only 2-3 values in the RGB spectrum, it's probably not going to be noticeable.

95th percentile tradeoff
------------------------

Armed with this knowledge, we can do the following. Instead of using the maximum gradient magnitude as our "speed limit", we can use the 95th percentile speed limit. That is, pick a value \\( x \\) such that the gradient magnitude is larger than \\( x \\) only 5% of the time. In the case of sin noise, this is 0.88. In the case of 3D Perlin noise, this is 1.32.

This is conservative enough that there are no perceptible rendering artifacts, and I only need to go 20-30% faster than my speed limit for there to be clearly visible rendering artifacts.

Smoothly clamped Perlin noise
-----------------------------

You might have also read about a [modification I made to Perlin noise](/2017/06/22/restricted-perlin-noise.html) in order to avoid having to deal with unlikely extreme values. What does the distribution of that Perlin noise look like?

<center><img src="/images/2017/perlin2d_new_gradient_pdf.png" width="500"/><br /><em>Gradient magnitude PDF and CDF for modified 2D Perlin noise</em></center>

<center><img src="/images/2017/perlin3d_new_gradient_pdf.png" width="500"/><br /><em>Gradient magnitude PDF and CDF for modified 3D Perlin noise</em></center>

With a gradient magnitude that goes up to 5.18 and 6.98 respectively, there are also a large range of unlikely gradients. (This Perlin noise is scaled to \\( [-1, 1] \\), which is why the gradient seems a little large). The 95th percentiles are at 3.12 and 3.18.

So as you can see, efficiently rendering surfaces that are defined by fake distance fields can be quite hard. In these blog posts, I've come up with some analysis one can do, but a future goal would be to find more general optimization techniques.
