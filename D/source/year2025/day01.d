module year2025.day01;

import core.time;
import std.stdio;
import std.conv;
import std.string;
import std.exception;
import std.regex;
import std.math;

import input;
import utility;

enum int DIAL_SIZE = 100;

int[] parse_input()
{
    auto contents = get_input(2025, 1).split(regex("\r?\n"));
    int[] instructions;
    foreach (line; contents)
    {
        if (line.length == 0) continue;
        enforce(line.length >= 2, "Invalid input!");
        int dir;
        if (line[0] == 'L') dir = -1;
        else if (line[0] == 'R') dir = 1;
        else throw new Exception("Invalid input!");
        instructions ~= dir * line[1..$].to!int;
        
    }
    return instructions;
}

int part_1(int[] instructions)
{
    int dial_pos = 50;
    int count = 0;
    foreach(rotation; instructions)
    {
        dial_pos += rotation;
        dial_pos = wrap(dial_pos, DIAL_SIZE);
        count += (dial_pos == 0);
    }
    return count;
}

// It's not inefficient -- it's ~~cycle accurate~~
// Seriously, though, it's fast *enough*, and that means we can use it to generate test cases for something smarter.
int part_2(int[] instructions)
{
    int dial_pos = 50;
    int count = 0;
    foreach (rotation; instructions)
    {
        int increment = (rotation < 0) ? -1 : 1;
        for (int i = 0; i < abs(rotation); ++i)
        {
            dial_pos += increment;
            if (dial_pos == 100)
            {
                dial_pos = 0;
                count += 1;
            }
            else if (dial_pos == 0)
            {
                count += 1;
            }
            else if (dial_pos == -1)
            {
                dial_pos = 99;
            }
        }
    }
    return count;
}

bool run_2025_day01()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input);
    auto end_time = MonoTime.currTime;
    writefln("Password (part 1): %s", pt1_solution);
    writefln("Password (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}

/* Failed attempt stashed for later use
int part_2(int[] instructions)
{   
    int dial_pos = 50;
    int count = 0;
    int zero_passthroughs = 0;
    foreach(rotation; instructions)
    {
        writefln("Rotate %d -> %d", rotation, wrap(dial_pos + rotation, DIAL_SIZE));
        if (rotation < 0)
        {
            if (dial_pos == 0) dial_pos = DIAL_SIZE;  // so we don't think we can only go zero places
            alias distance_to_zero = dial_pos;  // for clarity
            int temp = ((-rotation) - distance_to_zero) / DIAL_SIZE + ((-rotation) > distance_to_zero);
            zero_passthroughs += temp;
            writefln("    Passed %d times.", temp);
            writefln("    Distance to zero was: %d", distance_to_zero);
        }
        else
        {
            int distance_to_zero = DIAL_SIZE - dial_pos;
            int temp = (rotation - distance_to_zero) / DIAL_SIZE + (rotation > distance_to_zero);
            zero_passthroughs += temp;
            writefln("    Passed %d times", temp);
        }
        writeln;
        dial_pos += rotation;
        dial_pos = wrap(dial_pos, DIAL_SIZE);
        count += (dial_pos == 0);
    }
    return count + zero_passthroughs;  // 6336 too high
}
*/