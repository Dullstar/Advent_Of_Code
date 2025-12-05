module year2025.day05;

import core.time;
import std.stdio;
import std.regex;
import std.conv;
import std.string;
import std.exception;
import std.stdint;
import std.algorithm;
import std.array;
import std.typecons;

import input;
import utility;

struct Range
{
    this(int64_t a, int64_t b)
    {
        if (a < b)
        {
            min = a;
            max = b;
        }
        else
        {
            min = b;
            max = a;
        }
    }
    int64_t min;
    int64_t max;
}

struct Input
{
    Range[] fresh;
    int64_t[] ingredients;
}

// technically we could just use std.format.formattedRead, but we're already using regex
// to split on line endings that could either be \n or \r\n, so we may as well use regex
// to parse too. (and yes, we DO have to account for \r\n, D doesn't do that for us).
//
// (Usually, the inputs won't contain \r\n, but if they're copy/pasted, such as with example inputs,
// then without it, it'll work on e.g. Linux, but won't work on Windows)
Input parse_input()
{
    auto parts = get_input(2025, 5).strip.split(regex("\r?\n\r?\n"));
    enforce(parts.length == 2, "Invalid input!");
    Input input;
    input.fresh =
        parts[0].strip.split(regex("\r?\n"))
        .map!(a => a.matchFirst(regex(`(\d+)-(\d+)`)))
        .map!(a => Range(a[1].to!int64_t, a[2].to!int64_t)).array;
    input.ingredients =
        parts[1].strip.split(regex("\r?\n"))
        .map!(a => a.to!int64_t).array;
    return input;
}

bool in_range(int64_t input, Range range)
{
    return input >= range.min && input <= range.max;
}

int64_t part_1(Input input)
{
    int64_t fresh = 0;
    foreach(ingredient; input.ingredients)
    {
        foreach(range; input.fresh)
        {
            if (ingredient.in_range(range))
            {
                fresh += 1;
                break;
            }
        }    
    }
    return fresh;
}

int64_t calculate_range_size(Range range)
{
    // +1 is because e.g. Range(3, 5) includes 3, 4, and 5, but 5-3=2, so we need to add 1.
    return range.max - range.min + 1;
}

int64_t part_2(Input input)
{
    input.fresh.sort!((a, b) => (a.min < b.min));

    Range merged_range = input.fresh[0];
    int64_t fresh_ids = 0;
    foreach(range; input.fresh[1..$])
    {
        if (range.min <= merged_range.max)
        {
            if (range.max > merged_range.max) merged_range.max = range.max;
        }
        else
        {
            // range falls entirely outside the current merged range, so we now calculate the size
            // of the old range, and set up the next iteration of the loop so we don't miss the range
            // we just found.
            fresh_ids += merged_range.calculate_range_size;
            merged_range = range;
        }
    }
    // We will consistently fail to calculate the last range within the loop,
    // since that step triggers when it hits a range that falls entirely outside the current one,
    // and the calculation only includes the previous range in that case -- so we need to clean up
    // whatever's left.
    fresh_ids += merged_range.calculate_range_size;
    return fresh_ids;
}

bool run_2025_day05()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input);
    auto end_time = MonoTime.currTime;
    writefln("Fresh ingredients (part 1): %s", pt1_solution);
    writefln("Fresh ids (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}