module year2025.day06;

import core.time;
import std.stdio;
import std.regex;
import std.conv;
import std.string;
import std.exception;
import std.stdint;
import std.algorithm;
import std.array;

import input;
import utility;

enum Op: char
{
    Add = '+',
    Mul = '*',
}

struct Input
{
    int64_t[][] numbers;
    Op[] operators;
    int64_t[][] numbers_pt2;
}

Grid2D!char construct_grid(string[] input_lines)
{
    char[] layout;
    Point!int size = Point!int(input_lines[0].length.to!int, input_lines.length.to!int);
    foreach (line; input_lines)
    {
        layout ~= line.to!(char[]);
    }
    return new Grid2D!char(size, layout);
}

int64_t[][] parse_grid(Grid2D!char grid)
{
    int64_t[] current;
    int64_t[][] numbers;
    // Technically, we should be reading the columns right-to-left, but
    // there are only two possible operators, and they are both commutative,
    // so reading them from left-to-right anyway does not change the answer,
    // and the operators were parsed left-to-right for part 1, so if we parse
    // these left-to-right too, we don't need to do anything to account for it.
    for (int x = 0; x < grid.size.x; ++x)
    {
        bool have_number = false;
        int64_t number;
        inner: for (int y = 0; y < grid.size.y; ++y)
        {
            char c = grid[x, y];
            switch(c)
            {
            case '0': .. case '9':
                have_number = true;
                number = (number * 10) + (c ^ 0x30);
                break;
            default:
                if (have_number) break inner;
                break;
            }

        }
        if (have_number)
        {
            current ~= number;
        }
        else
        {
            numbers ~= current;
            current = [];
        }
    }
    if (current.length != 0) numbers ~= current;
    return numbers;
}

Input parse_input()
{
    Input input;
    auto contents = get_input(2025, 6).strip.split(regex("\r?\n"));
    size_t len = 0;
    foreach (line_num, line; contents[0..$-1])
    {
        if (line_num == 0)
        {
            auto numbers_horiz = line.split();
            len = numbers_horiz.length;
            foreach (num; numbers_horiz)
            {
                input.numbers ~= [num.to!int64_t];
            }
        }
        else
        {
            auto numbers_horiz = line.split();
            enforce(numbers_horiz.length == len, "Length mismatch in input!");
            foreach (i, num; numbers_horiz)
            {
                input.numbers[i] ~= num.to!int64_t;
            }
        }
    }
    foreach (c; contents[$-1])
    {
        switch (c)
        {
        case '+':
            input.operators ~= Op.Add;
            break;
        case '*':
            input.operators ~= Op.Mul;
            break;
        default:
            break;
        }
    }
    enforce(input.numbers.length > 0, "Invalid input!");
    enforce(input.numbers.length == input.operators.length, "Length mismatch in input!");

    auto grid = construct_grid(contents[0..$-1]);
    input.numbers_pt2 = parse_grid(grid);
    enforce(input.numbers_pt2.length == input.operators.length, "Length mismatch for part 2!");

    return input;
}

int64_t solve(const int64_t[][] numbers, const Op[] operators)
{
    int64_t grand_total;
    foreach (i, num_list; numbers)
    {
        final switch(operators[i])
        {
        case Op.Add:
            grand_total += num_list.sum;
            break;
        case Op.Mul:
            grand_total += num_list.fold!((a, b) => a * b)(1.to!int64_t);
            break;
        }
    }
    return grand_total;
}

bool run_2025_day06()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = solve(input.numbers, input.operators);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = solve(input.numbers_pt2, input.operators);
    auto end_time = MonoTime.currTime;
    writefln("Grand total (part 1): %s", pt1_solution);
    writefln("Grand total (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}