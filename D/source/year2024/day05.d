module year2024.day05;

import std.stdio;
import std.conv;
import std.regex;
import std.string;
import std.algorithm;
import std.array;
import std.exception;
import core.time;

import input;

struct Input
{
    bool[int][int] deps;
    int[][] sequences;
}

Input parse_input()
{
    Input _in;
    string contents = get_input(2024, 5);
    auto split_contents = contents.strip.split(regex("\r?\n\r?\n"));
    enforce(split_contents.length == 2, "Bad input: too many subsections");
    foreach (line; split_contents[0].split(regex("\r?\n")))
    {
        auto line_contents = line.split("|");
        enforce(line_contents.length == 2, format!("Bad input: bad line: %s")(line_contents));
        int a = line_contents[0].to!int;
        int b = line_contents[1].to!int;
        bool[int]* ptr = a in _in.deps;
        if (ptr is null)
        {
            _in.deps[a] = [b: true];
        }
        else
        {
            (*ptr)[b] = true;
        }
    }
    foreach (line; split_contents[1].split(regex("\r?\n")))
    {
        _in.sequences ~= line.split(",").map!(a => a.to!int).array;
    }
    return _in;
}

bool is_sequence_correctly_ordered(const ref int[] seq, const ref bool[int][int] deps)
{
    for (size_t i = 1; i < seq.length; ++i)
    {
        auto not_allowed = deps.get(seq[i], null);
        if (not_allowed is null) continue;
        for (size_t j = 0; j < i; ++j)
        {
            if (not_allowed.get(seq[j], false))
            {
                return false;
            }
        }
    }
    return true;
}

int get_sequence_middle_number(const ref int[] seq)
{
    // Honestly this should probably be enforced by parse_input.
    enforce(seq.length > 0, "Zero length sequences aren't allowed!");
    // technically probably doens't work on even size, but no point checking,
    // it won't crash and valid input probably just doesn't have it;
    // otherwise it would have said what to do about that.
    return seq[seq.length / 2];  // e.g. [1, 4, 6] -> len 3, so 3/2 = int(1.5) = 1, seq[1] = 4
}

int part_1(Input input, out bool[] pt2_helper)
in (pt2_helper.length == 0)  // pt2_helper is to be filled in here
{
    int sum = 0;
    foreach (sequence; input.sequences)
    {
        bool ordered = is_sequence_correctly_ordered(sequence, input.deps);
        if (ordered)
        {
            sum += get_sequence_middle_number(sequence);
        }
        pt2_helper ~= ordered;
    }
    return sum;
}

int get_first_bad_entry_index(const ref int[] seq, const ref bool[int][int] deps)
{
    for (int i = 1; i < seq.length; ++i)
    {
        auto not_allowed = deps.get(seq[i], null);
        if (not_allowed is null) continue;
        for (int j = 0; j < i; ++j)
        {
            if (not_allowed.get(seq[j], false))
            {
                return i;
            }
        }
    }
    return -1;
}

int fix_sequence(int[] sequence, const ref bool[int][int] deps)
{
    while (true) {
        int bad_entry = get_first_bad_entry_index(sequence, deps);
        if (bad_entry >= 0)
        {
            int temp = sequence[bad_entry - 1];
            sequence[bad_entry - 1] = sequence[bad_entry];
            sequence[bad_entry] = temp;
            continue;
        }
        return get_sequence_middle_number(sequence);
    }
    //enforce(0, "Sequence %s is bad, and it should feel bad.");
    //assert(0);  // makes the compiler happy (enforce renders this unreachable)
}

int part_2(Input input, bool[] passed)
{
    int sum = 0;
    foreach(i, sequence; input.sequences)
    {
        if (!passed[i])
        {
            sum += fix_sequence(sequence, input.deps);
        }
    }
    return sum;
}

bool run_2024_day05()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    bool[] passed;  // part 1 will fill this out so part 2 can use it.
    auto pt1_solution = part_1(input, passed);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input, passed);
    auto end_time = MonoTime.currTime;

    writefln("XMAS puzzle hits (part 1): %s", pt1_solution);
    writefln("X-MAS puzzle hits (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}
