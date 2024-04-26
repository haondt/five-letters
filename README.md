# five-letters

A solution to Matt Parkers [5-word-problem](https://www.youtube.com/watch?v=_-AfhLQfb6w).

# Result

currently this solution completes in 4m26s:

```shell
$ time python3 search.py
building initial word list...
5977
selecting second word...
640023
np selecting third word...
1272060
selecting fourth and fifth words...
final answer: 538
python3 search.py  208.01s user 23.02s system 86% cpu 4:26.47 total
```

# Usage

get `words_alpha.txt` from https://github.com/dwyl/english-words, and run

```shell
python3 search.py
```

