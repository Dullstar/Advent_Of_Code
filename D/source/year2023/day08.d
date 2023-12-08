module year2023.day08;

import std.stdio;
import std.string;
import std.array;
import std.exception;
import std.conv;
import std.regex;
import std.stdint;
import core.time;

import input;

struct Node
{
    string left;
    string right;
}

struct Instructions
{
    string directions;
    Node[string] layout;
}

Instructions parse_input()
{
    string contents = get_input(2023, 8);
    auto sections = contents.split(regex("\r?\n\r?\n"));
    auto line_regex = regex(r"(...) = \((...), (...)\)");
    enforce(sections.length == 2, "Bad input!");
    auto instructions = Instructions(sections[0]);
    auto matches = sections[1].matchAll(line_regex);
    foreach (match; matches) {
        instructions.layout[match[1]] = Node(match[2], match[3]);
    }
    return instructions;
}

int part_1(const ref Instructions instructions) {
    string current = "AAA";
    int i = 0;
    while (true) {
        foreach(turn; instructions.directions) {
            // writefln("Step %s: %s, %s", i + 1, current, turn);
            i += 1;
            switch (turn) {
            case 'L':
                current = instructions.layout[current].left;
                break;
            case 'R':
                current = instructions.layout[current].right;
                break;
            default:
                writefln("Warning: unexpected character found in input: %s", turn);
                break;
            }
            if (current == "ZZZ") return i;
        }
    }
}

string[] get_starting_nodes(const ref Instructions instructions)
{
    string[] starting_nodes;
    foreach(node; instructions.layout.keys) {
        if (node[2] == 'A') starting_nodes ~= node;
    }
    return starting_nodes;
}

bool check_nodes(const ref string[] nodes, const ref Instructions instructions)
{
    foreach(const ref node; nodes) {
        if (node[2] != 'Z') return false;
    }
    return true;
}

// Okay, so it's ACTUALLY a Least Common Multiple.
// But the bus problem inspired it, so it's a bus now.
// I imagine a prime factorization might be more efficient, but I
// REALLY don't want to write that tonight.
int64_t mega_bus(int[] inputs)
{
    int64_t merge_bus(int64_t a, int64_t b)
    {
        int64_t A = a;
        int64_t B = b;
        b = (a / b) * b;  // well, it helps cut down on the repeated addition a little.
        while(a != b) {
            if (a < b) a += A;
            if (b < a) b += B;
        }
        return a;
    }
    int64_t bus = inputs[0];
    foreach(bus2; inputs[1..$]) {
        bus = merge_bus(bus, bus2);
    }
    return bus;
}

int64_t part_2(const ref Instructions instructions)
{
    string[] current_nodes = get_starting_nodes(instructions);
    int[] run_times;
    foreach(ref node; current_nodes) {
        int i = 0;
        individual: while(true) {
            int turn_index = i % instructions.directions.length.to!int;
            i += 1;
            switch (instructions.directions[turn_index]) {
            case 'L':
                node = instructions.layout[node].left;
                break;
            case 'R':
                node = instructions.layout[node].right;
                break;
            default:
                writefln("Warning: unexpected character found in input: %s", 
                    instructions.directions[turn_index]);
                break;
            }
            if (node[2] == 'Z') {
                run_times ~= i;
                break individual;  // label isn't really necessary, but for clarity
            }
        }
    }
    writeln(run_times);
    auto start = MonoTime.currTime;
    auto result = mega_bus(run_times);
    auto end = MonoTime.currTime;
    writefln("Mega Bus is slow: %s ms", float((end - start).total!"usecs") / 1000);
    return result;
}

bool run_2023_day08()
{
    auto start_time = MonoTime.currTime;
    auto instructions = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(instructions);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(instructions);
    auto end_time = MonoTime.currTime;

    writefln("We're gonna be on this camel for a while (part 1): %s", pt1_solution);
    writefln("The mega ghost bus is gonna take even longer (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}