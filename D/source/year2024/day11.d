module year2024.day11;

import std.algorithm;
import std.array;
import std.stdio;
import std.conv;
import std.string;
import std.stdint;
import core.time;

import input;
import dict;

int64_t[] parse_input()
{
    return get_input(2024, 11).strip.split.map!(a => a.to!int64_t).array;
}

int64_t[] change_stone_pt1(int64_t stone)
{
    if (stone == 0) return [1];
    string stone_str = stone.to!string;
    if (stone_str.length & 1)
    {
        return [stone * 2024];
    }
    return [stone_str[0..stone_str.length / 2].to!int64_t, stone_str[(stone_str.length / 2)..$].to!int64_t];
}

int64_t part_1_blinks(int64_t stone, size_t blinks_left, size_t blinks_max, ref Dict!(int64_t, int64_t[]) cache)
{
    if (blinks_left == 0) return 1;
    auto cached = cache[stone];
    if (cached.isNull)
    {
        cache[stone] = [];
        cache[stone].length = blinks_max;
        cache[stone][] = -1;
        cached = cache[stone];
    }
    auto quantity = cached.get[blinks_left - 1];
    if (quantity == -1)
    {
        int64_t total = 0;
        foreach (new_stone; stone.change_stone_pt1)
        {
            total += part_1_blinks(new_stone, blinks_left - 1, blinks_max, cache);
        }
        cache[stone][blinks_left - 1] = total;
        return total;
    }
    return quantity;
}

int64_t blinks(int64_t[] stones, int64_t blinks)
{
    Dict!(int64_t, int64_t[]) cache;
    int64_t total = 0;
    foreach(stone; stones)
    {
        total += part_1_blinks(stone, blinks, blinks, cache);
    }
    return total;
}

bool run_2024_day11()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = blinks(input, 25);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = blinks(input, 75);
    auto end_time = MonoTime.currTime;
    writefln("Stones after 25 blinks (part 1): %s", pt1_solution);
    writefln("Stones after 75 blinks (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}
