module year2023.day15;

import std.conv;
import std.stdio;
import core.time;
import std.algorithm;
import std.exception;
import std.string;
import std.regex;
import std.array;

import input;

string[] parse_input()
{
    return get_input(2023, 15).strip.split(",");
}

ubyte HASH(string str)
{
    ubyte value;  // I could % 256 or I could let the type system do it for me!
    foreach(ubyte c; str) {
        value += c;
        value *= 17;
    }
    return value;
}

uint part_1(string[] to_HASH)
{
    return to_HASH.map!(a=>a.HASH).sum;
}

struct Box
{
    uint[string] lenses;
    size_t[string] first_encounters;
}

Box[256] process_steps(string[] steps)
{
    Box[256] boxes;
    auto re = regex(r"([a-zA-Z]+)([=-])(\d*)");
    foreach(i, step; steps) {
        auto match = step.matchFirst(re);
        enforce(!match.empty, format("Error: couldn't interpret string: %s", step));
        ubyte box = HASH(match[1]);
        switch (match[2]) {
        case "-":
            boxes[box].lenses.remove(match[1]);
            boxes[box].first_encounters.remove(match[1]);
            break;
        case "=":
            if (!(match[1] in boxes[box].lenses)) boxes[box].first_encounters[match[1]] = i;
            boxes[box].lenses[match[1]] = match[3].to!uint;
            break;
        default: 
            assert(0);
        }
    }
    return boxes;
}
uint part_2(string[] steps)
{
    auto boxes = steps.process_steps;
    uint total = 0;
    foreach(i, ref box; boxes) {
        auto lens_order = box.lenses.keys.sort!((a,b)=>box.first_encounters[a] < box.first_encounters[b]).array;
        foreach(j, label; lens_order) {
            total += (i + 1) * (j + 1) * box.lenses[label];
        }
    }
    return total;
}

bool run_2023_day15()
{
    auto start_time = MonoTime.currTime;
    auto steps = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(steps);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(steps);
    auto end_time = MonoTime.currTime;

    writefln("HASH algorithm output (part 1): %s", pt1_solution);
    writefln("Part 2 (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}
