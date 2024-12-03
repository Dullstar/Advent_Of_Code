module year2024.day03;

import std.regex;
import std.stdio;
import std.stdint;
import std.conv;
import std.algorithm;
import core.time;

import input;

enum Opcode
{
    Multiply,
    Do,
    DoNot,
    Invalid
}

struct Instruction
{
    this(string raw)
    {
        switch (raw)
        {
        case "do()":
            opcode = Opcode.Do;
            break;
        case "don't()":
            opcode = Opcode.DoNot;
            break;
        default:
            auto match = matchFirst(raw, r"mul\(([0-9]{1,3}),([0-9]{1,3})\)");
            if (match.empty)
            {
                opcode = Opcode.Invalid;
            }
            else
            {
                opcode = Opcode.Multiply;
                a = match[1].to!int64_t;
                b = match[2].to!int64_t;
            }
        }
    }
    Opcode opcode;
    int64_t a;
    int64_t b;
}

Instruction[] parse_input()
{
    string contents = get_input(2024, 3);
    Instruction[] instr;
    foreach(match; matchAll(contents, regex(r"don?'?t?\(\)|mul\([0-9]{1,3},[0-9]{1,3}\)")))
    {
        instr ~= Instruction(match[0]);
    }
    return instr;
}

int64_t do_multiplications(Instruction[] instructions)
{
    int64_t sum = 0;
    foreach (instr; instructions)
    {
        if (instr.opcode == Opcode.Multiply) 
        {
            sum += instr.a * instr.b;
        }
    }
    return sum;
    // This equivalent one-liner apparently has some (slight) overhead.
    // I can't imagine a situation where it would make the difference between good/bad performance,
    // but the for loop is slightly faster on my machine.
    // return instructions.filter!(a => a.opcode == Opcode.Multiply).map!(a => a.a * a.b).sum;
}

int64_t conditional_multiplications(Instruction[] instructions)
{
    int64_t sum = 0;
    bool multiply = true;
    foreach (instr; instructions)
    {
        final switch (instr.opcode)
        {
        case Opcode.Multiply:
            if (multiply)
            {
                sum += instr.a * instr.b;
            }
            break;
        case Opcode.Do:
            multiply = true;
            break;
        case Opcode.DoNot:
            multiply = false;
            break;
        case Opcode.Invalid:
            assert(0);
        }
    }
    return sum;
}

bool run_2024_day03()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = do_multiplications(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = conditional_multiplications(input);
    auto end_time = MonoTime.currTime;

    writefln("Sum of multiplication instructions (part 1): %s", pt1_solution);
    writefln("Sum of multiplication instructions (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}