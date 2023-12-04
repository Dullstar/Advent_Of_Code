module year2023.day04;

import std.string;
import std.array;
import std.stdio;
import std.algorithm;
import std.math;
import std.conv;
import input;
import core.time;

struct ScoreResult
{
    int matches;
    int score;
}

struct Card
{
    int[] winning;
    int[] numbers;

    ScoreResult score() const
    {
        int matches = 0;
        foreach (num; numbers) {
            // The winning number lists are pretty small, so I suspect there's a possibility
            // a more sophisticated search would have little to no benefit.
            foreach (winner; winning) {
                matches += (winner == num);
            }
        }
        // I guess we could also write this as (matches > 0) * pow(...)
        return ScoreResult(matches, (matches > 0) ? pow(2, (matches - 1)) : 0);
    }
}

Card[] parse_input()
{
    auto file = File(get_input_path(2023, 4), "r");
    string s;
    Card[] cards;
    while ((s = file.readln) !is null) {
        s = s.strip;
        auto line = s.split(":");
        auto card = line[1].split("|");
        auto winning = card[0].split.map!(a => a.to!int).array;
        auto numbers = card[1].split.map!(a => a.to!int).array;
        cards ~= Card(winning, numbers);
    }
    return cards;
}

// This was pulled out of Part 1's function so that Part 2 can re-use
// the number of matches that we had to calculate ANYWAY in part 1 in order to get the scores
// instead of doing it again in Part 2.
ScoreResult[] get_card_scores(const ref Card[] cards)
{
    return cards.map!(a => a.score).array;
}

int calculate_card_pile_score_pt1(const ref ScoreResult[] card_scores)
{
    return card_scores.fold!((int a, ScoreResult b) => a + b.score)(0);
}

int calculate_card_pile_amount_pt2(const ref ScoreResult[] card_scores)
{
    int[] copies;
    copies.length = card_scores.length;
    copies[] = 1;
    foreach(i, card; card_scores) {
        foreach (j; 0..card.matches) {
            if ((i + j + 1) < copies.length) {
                copies[i + j + 1] += copies[i];
            }
        }
    }
    return sum(copies);
}

bool run_2023_day04()
{
    auto start_time = MonoTime.currTime;
    auto cards = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto card_scores = get_card_scores(cards);
    auto pt1_solution = calculate_card_pile_score_pt1(card_scores);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = calculate_card_pile_amount_pt2(card_scores);
    auto end_time = MonoTime.currTime;

    writefln("Sum of card scores (part 1): %s", pt1_solution);
    writefln("Number of cards (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}