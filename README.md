# Dullstar's Advent Of Code Solutions
My solution for the Advent of Code challenges in various languages.

I try to make these solutions easy to follow. In some cases, particularly on later days in the year, this may lead to some days that may feel overcommented, but the idea is that someone who's struggling to solve the problem themselves should hopefully be able to look at the solution and understand how I went about solving the problem and why the code does what it does.

For the year 2020 specifically, some additional languages may be available at https://github.com/Dullstar/Advent-Of-Code-2020 (as well as every day from that year being present in at least one language), as this repository hasn't quite caught up yet (it is planned, however, along with improvements to some of those solutions). Since the directory structure has been revamped from scratch, the old repository is being kept instead of renamed to avoid dead links in 2020's solution sharing threads.

## Inputs
The older language templates expect the input files to be stored in `inputs/NNNN/dayNN.txt` where `NNNN` is the year and `NN` is the day. Days 1-9 should be zero prefixed such that the day is 2 digits, e.g. `day02.txt` for day 2. This path is relative to the root of this repository, that is, the same folder as this readme.

The more recent ones allow arbitrary input folders, though the `NNNN/dayNN.txt` formatting within it is still required. Some also additionally allow specifying a folder for test inputs, but test inputs aren't guaranteed to run, as sometimes a problem has multiple test inputs, and when that happens the Part 1 test inputs aren't always valid for Part 2 and vice versa.