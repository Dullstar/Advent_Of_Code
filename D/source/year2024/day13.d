module year2024.day13;

import std.algorithm;
import std.stdio;
import std.conv;
import std.exception;
import std.container;
import std.regex;
import std.string;
import std.stdint;
import core.time;

import input;
import utility;

struct ClawMachine
{
    Point!int64_t a;
    Point!int64_t b;
    Point!int64_t prize;
}

ClawMachine[] parse_input()
{
    auto contents = get_input(2024, 13).split(regex("\r?\n\r?\n"));
    ClawMachine[] machines;
    foreach (line; contents)
    {
        auto machine = line.strip.split(regex("\r?\n"));
        enforce(machine.length == 3, "Bad input!");
        auto re = regex(r"X[+=]([0-9]+), Y[+=]([0-9]+)");
        ClawMachine claw;
        static foreach(i; [0, 1, 2])
        {{
            auto match = machine[i].matchFirst(re);
            enforce(!match.empty, "Bad input!");
            auto pt = Point!int64_t(match[1].to!int64_t, match[2].to!int64_t);
            static if (i == 0) claw.a = pt;
            else static if(i == 1) claw.b = pt;
            else static if (i == 2) claw.prize = pt;
        }}
        machines ~= claw;
    }
    return machines;
}

enum COST_A = 3;
enum COST_B = 1;

// Note: Assumes that the statement regarding 100 pushes/button in Part 1 was a hint,
// and not a constraint.
int64_t play(ClawMachine claw)
{
    int64_t pushes_a_num = (claw.b.y * claw.prize.x) - (claw.b.x * claw.prize.y);
    int64_t pushes_a_den = (claw.b.y * claw.a.x) - (claw.b.x * claw.a.y);
    if (pushes_a_num % pushes_a_den != 0) return 0;
    int64_t pushes_a = pushes_a_num / pushes_a_den;
    int64_t pushes_b_num = (claw.prize.y - claw.a.y * pushes_a);
    if (pushes_b_num % claw.b.y != 0) return 0;
    int64_t pushes_b = pushes_b_num / claw.b.y;
    return pushes_a * COST_A + pushes_b * COST_B;
}

int64_t part_1(ClawMachine[] claws)
{
    return claws.map!(claw => play(claw)).sum;
}

enum LARGE = 10_000_000_000_000;


int64_t part_2(ClawMachine[] claws)
{
    return claws.map!(claw => play(ClawMachine(claw.a, claw.b, claw.prize + Point!int64_t(LARGE, LARGE)))).sum;
}

bool run_2024_day13()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input);
    auto end_time = MonoTime.currTime;
    writefln("Tokens spent (part 1): %s", pt1_solution);
    writefln("Tokens spent (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}
