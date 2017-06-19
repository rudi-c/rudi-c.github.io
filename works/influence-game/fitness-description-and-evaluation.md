---
title: Fitness evaluation and evolution
---
<p><i>If you arrived directly on this page from a link, visit the <a href="/works/influence-game/">introduction and table of contents</a>.</i><br/><br/></p>
<p>This section describes :</p>
<ul>
<li>The usage of a Swiss tournament to assess fitness.</li>
<li>The evolutionary algorithms used to improve ANNs.</li>
<li>The design of a variant of Swiss tournaments to address some issues.</li>
</ul>
<p><strong><font style="font-size:14px">Single column Swiss tournament (SCST)</font></strong></p>
<p>The initial set of teams each have a distinct ANN with weights randomly uniformly generated be between -1 and 1. This set of teams will form the first generation. We begin with only one set and call such sets <strong>columns</strong> for reasons that will become more apparent later on.</p>
<p>In order to train the ANNs, a way to evaluate the performance of a team is required. The Influence Game is a competitive scenario: in order for a team to win, another team has to lose, in contrast to other tasks such as learning how to walk. The main trait required from an ANN is its ability to win against other ANNs. The margin of victory (difference in the number of points) also contains useful information - however, it is used only as a tiebreaker for the number of wins. Indeed, a team could develop a strategy that only wins by a small margin, but does so consistently.</p>
<p>The trivial way to compare a set of ANNs is to have a full tournament consisting in having a match between every pair of ANNs. However, as noted by Fehérvári and Wilfried<sup>1</sup>, that method is too slow to be computationally viable. A full tournament requires n(n-1)/2 rounds. We therefore decide to adopt the method of Swiss tournament, which requires only [log2(n)/2]*n/2 matches. Indeed, on our testing machine featuring a AMD x6 1100t 3300MHz 6-core processor can carry about around 180 matches per second. Given that we are generally interested in evolving sets of more than 64 ANNs for hundreds of generations, it would take weeks to run each experiment.</p>
<p>In this implementation, ANNs are ranked by their number of wins (matches won), then by their number of points. For each round, starting with the top ranked ANN, we attempt to find a valid matchup with another ANN of similar rank. A matchup is valid if it has not occurred previously in the tournament. In pseudo-code, The procedure for ranking a set of ordered ANNs would be :</p>

```
procedure MatchANN(set-of-ANNs, current-index)
    if current-index = set-of-ANNs.size
        // Base case
        end
    else if set-of-ANNs[current-index] is already matched
        // Move to next
        matchANN(set-of-ANNs, current-index + 1)
    else
        for each ANN n with index higher than current-index
            if n has not been matched in this round
            and if set-of-ANNs[current-index] not matched with n previously
                match(set-of-ANNs[current-index], n)
                // Move to next
                matchANN(set-of-ANNs, current-index + 1)

procedure SwissTournament(initial-set, number-of-rounds)
    let current-set = initial-set
    for each round in number-of-round
        MatchANNs(current-set, ceil(log2(initial-set.size)))
        Carry out all matches
        current-set = RankAndSort(current-set)
```

<p>The full procedure includes some technicalities that allow backtracking in cases where not every team is paired for a match. A special case in the tournament is the first round, when all teams have the same score. There we use <a href="http://senseis.xmp.net/?GroupPairing">fold pairing</a>, which prevents teams the best teams from the previous generation from playing against each other too soon. </p>
<p>Given <em>n</em> teams, a Swiss Tournament typically requires <em>k = ceil(log2(n))</em> rounds in order to determine an absolute winner. This is because teams with no losses are paired up against each other, thus the number of teams with no losses decreases by half every round. <em>k</em> is not sufficient to make a pairwise distinction between all teams; there will be multiple teams with the same number of wins. In our application, this is acceptable as we only need to be able to determine which teams are in the first quartile.</p>
<p>Furthermore, our implementation of Swiss tournament assumes the following for simplification purposes :</p>
<ol>
<li>No ties (a team either wins or loses)</li>
<li>No drops (every team plays until the end of the tournament)</li>
<li>No byes (even number of teams ensure every team is paired up)</li>
</ol>
<p><em>example, with initial teams labelled from 1 to 8:</em></p>

<center><table border="1" style="text-align: center;">
<tr>
<td colspan="4">Round 1</td>
</tr>
<tr>
<td>Positive Team</td>
<td>Score</td>
<td>Negative Team</td>
<td>Score</td>
</tr>
<tr>
<td>1</td>
<td>0</td>
<td>8</td>
<td>0</td>
</tr>
<tr>
<td>2</td>
<td>0</td>
<td>7</td>
<td>0</td>
</tr>
<tr>
<td>3</td>
<td>0</td>
<td>6</td>
<td>0</td>
</tr>
<tr>
<td>4</td>
<td>0</td>
<td>5</td>
<td>0</td>
</tr>
<tr>
<td colspan="4">Suppose 1, 2, 5, 6 win</td>
</tr>
<tr>
<td colspan="4">Round 2</td>
</tr>
<tr>
<td>Positive Team</td>
<td>Score</td>
<td>Negative Team</td>
<td>Score</td>
</tr>
<tr>
<td>1</td>
<td>1</td>
<td>2</td>
<td>1</td>
</tr>
<tr>
<td>5</td>
<td>1</td>
<td>6</td>
<td>1</td>
</tr>
<tr>
<td>3</td>
<td>0</td>
<td>4</td>
<td>0</td>
</tr>
<tr>
<td>7</td>
<td>0</td>
<td>8</td>
<td>0</td>
</tr>
<tr>
<td colspan="4">Suppose 2, 3, 5, 8 win</td>
</tr>
<tr>
<td colspan="4">Round 3</td>
</tr>
<tr>
<td>Positive Team</td>
<td>Score</td>
<td>Negative Team</td>
<td>Score</td>
</tr>
<tr>
<td>2</td>
<td>2</td>
<td>5</td>
<td>2</td>
</tr>
<tr>
<td>1</td>
<td>1</td>
<td>3</td>
<td>1</td>
</tr>
<tr>
<td>6</td>
<td>1</td>
<td>8</td>
<td>1</td>
</tr>
<tr>
<td>4</td>
<td>0</td>
<td>7</td>
<td>0</td>
</tr>
<tr>
<td colspan="4">Suppose 2, 3, 4, 6 win</td>
</tr>
</table>
<p>The final rankings, a "column" of teams.</p>
<table border="1" style="text-align: center;">
<tr>
<td colspan="4">Final Results</td>
</tr>
<tr>
<td>Ranking</td>
<td>Team</td>
<td>Score</td>
</tr>
<tr>
<td>1</td>
<td>2</td>
<td>3</td>
</tr>
<tr>
<td>2</td>
<td>5</td>
<td>2</td>
</tr>
<tr>
<td>3</td>
<td>3</td>
<td>2</td>
</tr>
<tr>
<td>4</td>
<td>6</td>
<td>2</td>
</tr>
<tr>
<td>5</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>6</td>
<td>8</td>
<td>1</td>
</tr>
<tr>
<td>7</td>
<td>4</td>
<td>1</td>
</tr>
<tr>
<td>8</td>
<td>7</td>
<td>0</td>
</tr>
</table></center>

<p><strong><font style="font-size:14px">Evolutionary Algorithm</font></strong></p>
<p>After a tournament is over and every teams have been ranked, the next step is to create a new generation of teams. To do, we create a DNA sequence identifying the properties of each team, by mapping all the weights of its neural network into a one-dimensional array. Each weight will represent a single <b>gene</b>.</p>
<p>We then apply the following evolutionary methods :</p>
<ul>
<li>The top 25% best performing ANNs (<strong>elites</strong>) are carried over to the next generation</li>
<li>Every elite is paired with another elite and produces two offspring by uniform crossover</li>
<li>Twice the number of elites are created through mutation. The mutation consists in :
<ul>
<li>Selecting a random elite and creating an identical offspring</li>
<li>Every gene in the offspring has a 10% chance of being rerolled between [-1 and 1]</li>
<li>Every gene in the offspring has a 30% chance of being multiplied by up to 30%, with a larger chance of a small change</li>
</ul>
</li>
</ul>
<p>The procedure of ranking ANNs through a Swiss tournament and evolving them is repeated every generation.</p>
<p>In order to measure the improvement (or decrease) in performance of the teams, we keep track of the elites of each generation (top 25%) in an array. Those elites are stored in a separate array cell corresponding to their generation. It is possible that a given team is present as an elite throughout multiple generations. In that case, the team is kept only in the cell corresponding to the last generation in which it was an elite, which we define as the team's <b>associated generation</b>.</p>
<p>After the simulation has reached the last generation, we are left with an array containing a list of up to (teams/generation) * number of generations * .25 teams. However, since a given team competes for 2-3 generations on average, the actual number will usually be around 40% of the maximum. A large-scale Swiss tournament is then performed with every team in that list. If the number of teams is odd, we simply remove an ANN from the first generation to ensure that there are no byes.</p>
<p>In other words, we are comparing the top teams of each generation. Once the final ranking tournament is over, we proceed to plot every team in a graph of their ranking vs their associated generation.</p>
<p><center><img src="/images/2012/09/AC-ranking-plot.png"></center></p>
<p>The graph below represents a possible outcome for a simulation of 500 generations, 256 teams/generations. 13345 distinct teams have been ranked in the final tournament. The top 4 teams of each generation are highlighted in blue as they represent the very best of the generation. Other teams may be promising but unpolished variants. We can observe that teams improve in performance over the generations, with a decreasing rate of improvement.</p>
<p><i>Side note : The image was rendered with built-in Racket libraries for plotting data points and graphs. As I was looking for better ways to plot graphs than excel, my CS professor, Prabhakar Ragde, suggested that I use the programming we were learning. Though there's a slightly steeper learning curve than using some dedicated software, it is very convenient as the programming language itself allows me to pre-process data points in a clean and efficient manner. I am also very impressed by the quality of the graphs it can produce.</i></p>
<p><strong><font style="font-size:14px">Issues with the methodology</font></strong></p>
<p>While the teams get progressively better over time, able to rank better than teams from earlier generations, the strategy they develop is not the sort of results we would desire. Excluding some rare mutation that could create a team with a competitive novel strategy, the population will quickly converge to a set of similar team. Due to elite selection, the gene pool diversity will decrease quickly. The teams will then adopt a behavior suited specifically to playing against itself, which is not an interesting desired behavior.</p>

<center><iframe width="420" height="315" src="//www.youtube.com/embed/pcwBLDQiA08" frameborder="0" allowfullscreen></iframe></center>

<p>The video above shows a sample match between two of the top performing teams from the previous graph. The positive team (red) wins by 3007 points. We can observe that players adopt the strategy of moving to the left upon approaching opponents. This is a passive behavior <a href="http://www.youtube.com/watch?v=lmPJeKRs8gE">similar to walking on the right side of a corridor</a> to avoid collision. Almost all of the later-generation teams adopt this behavior, so the teams are not competing on strategy so much as moving into place and doing a slightly better job avoiding being removed from the field. We would think that the artificial neural networks could produce more active, elaborate behavior.</p>
<p>Thus, in our experiment, a naive Swiss tournament is not the proper methodology to compare different teams.</p>
<p><strong><font style="font-size:14px">Multi column Swiss tournament (MCST)</font></strong></p>
<p>The method we use to avoid having ANNs converge too quickly into a local minimum is to separate them in multiple columns. We initially create N sets (<b>columns</b>) of K random artificial neural networks. Teams in one column compete against teams in other columns, but there is no competition among teams of the same column. The procedure for ranking teams is similar to a Swiss tournament. We begin by choosing 2 columns among the N available, say A and B, to be paired against one another - column pairing. Then, we do <b>column-wise pairing</b>; we attempt to pair the best team of column A with the best team of column B if they have not been matched together in a previous round. After each round, the teams are sorted within their own column by their performance and we match them up again. Since both columns have K teams, there will be no byes.</p>
<p>The performance of a team is thus determined by its total number of wins across all column pair-ups. To ensure that the results are invariant under the ordering of column pair-ups, we tally the number of wins only at the end. When two columns are paired up, the teams do not start with a ranking for the purpose of the pair-up. In pseudo-code :</p>

```
procedure MatchANN(set-of-ANNs1, set-of-ANNs2, current-index)
    if current-index = set-of-ANNs1.size
        // Base case
        end
    else
        for each ANN n in set-of-ANNs2
            if n has not been matched in this round
            and if set-of-ANNs1[current-index] not matched with n previously
                match(set-of-ANNs[current-index], n)
                // Move to next ANN in first set
                matchANN(set-of-ANNs, current-index + 1)

procedure MultiSwissTournament(initial-columns, number-of-rounds)
    for i = 0 to initial-columns.size - 1
        for j = i + 1 to initial-columns.size - 1
            let current-set1 = initial-columns[i]
            let current-set2 = initial-columns[j]
            for each round in number-of-round
                MatchANNs(current-set1, current-set2, arbitrary-number)
                Carry out all matches
                current-set1 = Rank(current-set1)
                current-set2 = Rank(current-set2)
            Set aside score for column i
            Set aside score for column j
```

<p><em>example, with initial teams labelled from A1 to A4 for column A, B1 to B4 for column B</em></p>
<center><table border="1" style="text-align: center;">
<tr>
<td colspan="4">Round 1</td>
</tr>
<tr>
<td>Column A</td>
<td>Score</td>
<td>Column B</td>
<td>Score</td>
</tr>
<tr>
<td>A1</td>
<td>0</td>
<td>B1</td>
<td>0</td>
</tr>
<tr>
<td>A2</td>
<td>0</td>
<td>B2</td>
<td>0</td>
</tr>
<tr>
<td>A3</td>
<td>0</td>
<td>B3</td>
<td>0</td>
</tr>
<tr>
<td>A4</td>
<td>0</td>
<td>B4</td>
<td>0</td>
</tr>
<tr>
<td colspan="4">Suppose A1, B2, B3, B4 win</td>
</tr>
<tr>
<td colspan="4">Round 2</td>
</tr>
<tr>
<td>Column A</td>
<td>Score</td>
<td>Column B</td>
<td>Score</td>
</tr>
<tr>
<td>A1</td>
<td>1</td>
<td>B2</td>
<td>1</td>
</tr>
<tr>
<td>A2</td>
<td>0</td>
<td>B3</td>
<td>1</td>
</tr>
<tr>
<td>A3</td>
<td>0</td>
<td>B4</td>
<td>1</td>
</tr>
<tr>
<td>A4</td>
<td>0</td>
<td>B1</td>
<td>0</td>
</tr>
<tr>
<td colspan="4">Suppose A1, A2, B4, B1 win</td>
</tr>
<tr>
<td colspan="4">Round 3</td>
</tr>
<tr>
<td>Column A</td>
<td>Score</td>
<td>Column B</td>
<td>Score</td>
</tr>
<tr>
<td>A1</td>
<td>2</td>
<td>B4</td>
<td>2</td>
</tr>
<tr>
<td>A2</td>
<td>1</td>
<td>B2</td>
<td>1</td>
</tr>
<tr>
<td>A3</td>
<td>0</td>
<td>B3</td>
<td>1</td>
</tr>
<tr>
<td>A4</td>
<td>0</td>
<td>B1</td>
<td>1</td>
</tr>
<tr>
<td colspan="4">Suppose A1, A2, B3, B1 win</td>
</tr>
</table>
<p>The final rankings, a "column" of teams.</p>
<table border="1" style="text-align: center;">
<tr>
<td colspan="5">Final Results</td>
</tr>
<tr>
<td>Ranking</td>
<td>Column A</td>
<td>Score</td>
<td>Column B</td>
<td>Score</td>
</tr>
<tr>
<td>1</td>
<td>A1</td>
<td>3</td>
<td>B1</td>
<td>2</td>
</tr>
<tr>
<td>2</td>
<td>A2</td>
<td>2</td>
<td>B3</td>
<td>2</td>
</tr>
<tr>
<td>3</td>
<td>A3</td>
<td>0</td>
<td>B4</td>
<td>2</td>
</tr>
<tr>
<td>4</td>
<td>A4</td>
<td>0</td>
<td>B2</td>
<td>1</td>
</tr>
</table></center>

<p>First, notice that in the case of MCST, the number of rounds in a column pair-up can be arbitrary. Over all pair-ups, a given team will end up playing more matches than it would in a SCST to begin with. Secondly, there is no guarantee that the MCST will efficiently differentiate the best teams (see Team B in previous example) although in general, that is acceptable as we keep an entire quartile to carry over to the next generation.</p>
<p>Given this method, the best teams will be versatile enough to beat a number of different strategies from other columns. They will evolve and adapt to defeat other strategies, as opposed to its own.</p>
<p>Again, at every generation, we record the top 25% of teams in every column. After <em>n</em> generations, we have up to <em>n * number of teams per generation * .25</em> per column, which we merge into one large column for the final tournament that determines the ranking of teams in relation to their associated generation.</p>
<p>As in the case of SCST, the number of teams in the final columns is around 40% of the theoretical maximum since teams survive for 2-3 generations on average. Note, however, that with MCST, the number of teams in each column will not necessarily be the same for all columns. It is possible, for example, that column A evolves more slowly than column B such that an average team in A survives for 1 more generation than the average team in B. That creates a difficulty for the final tournament since it requires an equal number of teams in each column to be allow column pairings.</p>
<p>We decide to remove teams randomly from each column until each column has the same number of teams. Let <em>k = min{teams in column 1, teams in column 2, ..., teams in column n}</em>. A random team is selected and removed from each column until there are k teams in that column. We choose this method of removal to maintain the expected number of total wins by all teams in each column. If we were to remove teams from earlier generations or teams from later generations, it may give an advantage or disadvantage, respectively, to columns with more than k teams. Randomness guarantees a certain degree of uniformity in the removal process.</p>
<p>Next, we present a <a href="observations-and-discussion.html">sample test case with ANNs evolved using the MCST ranking system</a> and analyse the findings.</p>
