---
title: The Chameleon Style of Programming
disqus: y
---
<center><img src="/images/2014/01/CCChameleon.jpg" width="250" /></center>

<p>One issue programmers have to deal with often is style. No, not dressing style. Coding style. The manner in which each person prefers formatting code, which can vary wildly between people. Is it better to use tabs vs spaces for indentation? Opening curly braces at the end of a line or at the beginning of a new one? 80 characters limit per line, 100, 120, or none at all? Capitalization? Whitespaces? </p>
<p>For the average folk, these may seem like mundane difference but in the programming universe, these can easily spark the flames of a religious war.<br />
Etc etc.</p>
<p>To illustrate how much the same code can differ by the hands of different people :</p>
```java
int sum_arrays(int [] a,
               int [] b) {
  int sum = 0; /* Obvious comment here */
  for ( int i=0; i<a.size(); ++i ) {
    sum += a[i] * some_member_weight1 + b[i] * some_member_weight2;
  }
  return sum;
}
```
<p>v.s.</p>
```java
int SumArray( int[] a, int [] b )
{
    // Obvious comment here
    int sum = 0;
    for (int i = 0; i < a.size(); i++)
    {
        sum = sum + a[i] * _someMemberWeight1
                  + b[i] * _someMemberWeight2;
    }
    return sum;
}
```
<p>Exercise : Spot the differences (I counted 10).</p>
<p>Which look best? Personally I prefer 4 spaces/tab and { on new lines and 80 chars/line for aeration and readability, and some people have cringed just by reading the first half of this sentence. But at the end of the day, we're all humans gifted with the power of adaptation (or simply made of neurons converging to inevitable habituation). Spend enough time on a codebase, change text editor settings and eyes will be used to it within a day.</p>
<p>However, there is one kind of code formatting that looks worse than any other formatting : inconsistent formatting. This can occur when multiple people edit the same codebase over a long period of time and eyes just can't habituate to anything. Rather than just annoying newcomers, everyone is annoyed.</p>
<p>The simple solution to this problem? I propose the <b>chameleon style</b>. It is dead simple : like a chameleon, just use whatever style is in the surrounding environment? The rest of the file uses tab characters and not space characters for indentation? Do the same?</p>
<p>It's nothing good programmers don't already do, but I call dibs on nailing the term first.</p>
<p>Exception : The local environment is inconsistent with the global environment. For example, it a project sticks to 80 chars per line except that one module where the developer averages 140, might want to use 80 chars so that the outlying module will converge back into the global environment over time.</p>
