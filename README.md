# Codeforces-Practice-Ladders

A python script to suggest practice problem in a ladder-wise fashion, inspired by [A2OJ Ladders](https://a2oj.com/Ladders.html). The code selects problems in the specified rating range from [Codeforces Educational Rounds](https://codeforces.com/blog/entry/21496) held to date and returns the most relevant unsolved problem from this range. The output includes the problem suggested (name and link) and indicates your current progress on the ladder.

Before running the script, make sure to set your `handle` and adjust the `min_rating` and `max_rating`.

Sample output:
```
Suggested Problem: Pairs
Link: https://codeforces.com/contest/1463/problem/D
Current Progress: 48/138 Problems
```