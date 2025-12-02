module year2025.day02;

import core.time;
import std.stdio;
import std.string;
import std.array;
import std.exception;
import std.conv;
import std.algorithm;
import std.stdint;

import input;

struct ID_Range
{
    int64_t min;
    int64_t max;
}

// Realistically, we can probably approach this with some type of pattern matching, once we figure out which digits
// we can actually change that would produce an (in)valid result.

ID_Range[] parse_input()
{
    ID_Range[] ranges;
    auto contents = get_input(2025, 2).strip.split(',');
    foreach (range_str; contents)
    {
        auto range = range_str.split('-').map!(a => a.to!int64_t).array;
        enforce((range.length == 2) && (range[0] < range[1]), "Invalid input!");
        ranges ~= ID_Range(range[0], range[1]);
    }
    return ranges;
}

// Normally, it would probably make more sense to check if IDs are valid,
// but we're looking to find the ones that are invalid, so it's more convenient to just
// write it that way from the start.
bool is_id_invalid_part_1(int64_t id_int)
{
    string id = id_int.to!string;
    // we should ideally rule out all of these cases ahead of time, in which case
    // this if should become an assert
    if (id.length & 1) return false;
    size_t offset = id.length / 2;
    for (size_t i = 0; i < offset; ++i)
    {
        if (id[i] != id[offset + i]) return false;
    }
    return true;
}

int64_t check_range_part_1(ID_Range range)
{
    // Simple optimization: if all the ids have an odd length, then they can't be invalid.
    size_t len = range.min.to!string.length;
    if ((len & 1) && len == range.max.to!string.length) return 0;

    // I'm SURE there's a lot of optimizations we can make here, but let's just start by vomiting out the brute force solution.
    int64_t sum = 0;
    for (int64_t id = range.min; id <= range.max; ++id)
    {
        if (is_id_invalid_part_1(id))
        {
            // writefln("\tDetected invalid ID: %s", id);
            sum += id;
        }
    }
    return sum;
}

int64_t part_1(ID_Range[] ids)
{
    int64_t sum = 0;
    foreach (id_range; ids)
    {
        // writefln("Checking range %s to %s", id_range.min, id_range.max);
        sum += check_range_part_1(id_range);
    }
    return sum;
}

bool is_id_invalid_part_2(int64_t id_int)
{
    // Should be able to share some of the work as long as we properly detect when it changes...
    string id = id_int.to!string;
    segment_length: for (size_t i = 2; i <= id.length; ++i)
    {
        if (id.length % i != 0) continue;
        size_t inc = id.length / i;
        // writefln(" - %s (len=%s) should divide into %s segments of %s", id, id.length, i, inc);
        for (size_t j = 0; j < inc; ++j)
        {
            char want = id[j];
            // writefln("    - id[j=%s]=%s", j, id[j]);
            for (size_t k = j + inc; k < id.length; k += inc)
            {
                // writefln("    - id[k=%s]=%s", k, id[k]);
                if (want != id[k]) continue segment_length;
            }
        }
        return true;
    }
    return false;
}

int64_t check_range_part_2(ID_Range range)
{
    int64_t sum = 0;
    for (int64_t id = range.min; id <= range.max; ++id)
    {
        if (is_id_invalid_part_2(id))
        {
            // writefln("\tDetected invalid ID: %s", id);
            sum += id;
        }
    }
    return sum;
}

int64_t part_2(ID_Range[] ids)
{
    int64_t sum = 0;
    foreach (id_range; ids)
    {
        // writefln("\n\n ---Checking range %s to %s---", id_range.min, id_range.max);
        sum += check_range_part_2(id_range);
    }
    return sum;
}

bool run_2025_day02()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input);
    auto end_time = MonoTime.currTime;
    writefln("Invalid ID sum (part 1): %s", pt1_solution);
    writefln("Password (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}