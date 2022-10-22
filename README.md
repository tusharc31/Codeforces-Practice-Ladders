# Codeforces-Practice-Ladders

A python script to suggest practice problem in a ladder-wise fashion, inspired by [A2OJ Ladders](https://a2oj.com/Ladders.html). The code selects problems in the specified rating range from [Codeforces Educational Rounds](https://codeforces.com/blog/entry/21496) held to date and returns the most relevant unsolved problem from this range. The output includes the problem suggested (name and link) and indicates your current progress on the ladder.

Before running the script, make sure to set your `handle` and adjust the `min_rating` and `max_rating`.

Sample output:
```
Suggested Problem: Pairs
Link: https://codeforces.com/contest/1463/problem/D
Current Progress: 48/138 Problems
```

---

## Personalised problem suggestion

- For a user, the problems solved by the user is extracted.<br>For all of these problems, each of it's tag's frequency is incremented.
- For the 5 most recently solved problems the frequency is increased greatly, so as to get new genres of questions each time.
- Then the score is calculated in such a way that lower frequency tags get higher score.
- Then, the problem gets a score as the sum of score of it's tags, and finally a random problem is selected among all problems with weights as their scores.