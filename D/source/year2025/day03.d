module year2025.day03;

import core.time;
import std.stdio;
import std.string;
import std.conv;
import std.regex;
import std.exception;
import std.stdint;

import input;

alias Bank = int[];

Bank[] parse_input()
{
    Bank[] inputs;
    auto contents = get_input(2025, 3).strip.split(regex("\r?\n"));
    foreach(line; contents)
    {
        Bank digits;
        foreach(char c; line)
        {
            digits ~= (c^0x30).to!int;  // char->int just makes it wider, so we need to manually ascii digit -> int
        }
        enforce(digits.length >= 12, "Invalid input!");
        inputs ~= digits;
    }
    writeln;
    return inputs;
}

int get_largest_joltage_pt1(Bank bank)
{
    struct _Record
    {
        size_t pos;
        int value = -1;
    }

    _Record first;
    _Record second;

    for (size_t i = 0; i < bank.length - 1; ++i)  // the first digit can't be the last digit
    {
        if (bank[i] > first.value)
        {
            first = _Record(i, bank[i]);
            if (first.value == 9) break;  // early exit since 9 is the largest possible value in the bank
        }
    }
    for (size_t i = first.pos + 1; i < bank.length; ++i)
    {
        if (bank[i] > second.value)
        {
            second = _Record(i, bank[i]);
            if (second.value == 9) break;
        }
    }
    // could probably do this more efficiently, but good enough.
    return (bank[first.pos].to!string ~ bank[second.pos].to!string).to!int;
}

int part_1(Bank[] banks)
{
    int sum = 0;
    foreach(bank; banks)
    {
        sum += get_largest_joltage_pt1(bank);
    }
    return sum;
}

// We're finding the largest digit that leaves at least enough space left over to fill in the remaining digits.
// remaining: digits remaining to find AFTER the current one; so to find 12 digits, set remaining to 11.
string find_digits_part2(Bank bank, size_t start_pos, size_t remaining)
in (start_pos < bank.length)
{
    int max = -1;
    size_t max_pos;
    for (size_t i = start_pos; i < bank.length - remaining; ++i)
    {
        if (bank[i] > max)
        {
            max = bank[i];
            max_pos = i;
            if (max == 9) break;
        }
    }
    if (remaining == 0)
    {
        return max.to!string;
    }
    return max.to!string ~ find_digits_part2(bank, max_pos + 1, remaining - 1);
}

int64_t get_largest_joltage_pt2(Bank bank)
{
    pragma(inline, true);
    return find_digits_part2(bank, 0, 11).to!int64_t;
}

int64_t part_2(Bank[] banks)
{
    int64_t sum = 0;
    foreach(bank; banks)
    {
        sum += get_largest_joltage_pt2(bank);
    }
    return sum;
}

bool run_2025_day03()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input);
    auto end_time = MonoTime.currTime;
    writefln("Total output joltage (part 1): %s", pt1_solution);
    writefln("Total output joltage (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}