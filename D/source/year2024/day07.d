module year2024.day07;

import std.stdio;
import std.conv;
import std.regex;
import std.string;
import std.algorithm;
import std.array;
import std.stdint;
import std.exception;
import std.container;
import core.time;

import input;

struct Input
{
    int64_t target;
    int64_t[] values;
}

Input[] parse_input()
{
    Input[] _in;
    string contents = get_input(2024, 7);
    auto split_contents = contents.strip.split(regex("\r?\n"));
    foreach (line; split_contents)
    {
        auto split_line = line.split(":");
        enforce(split_line.length == 2, "Bad input!");
        _in ~= Input(split_line[0].to!int64_t, split_line[1].split.map!(a => a.to!int64_t).array);
    }
    return _in;
}

bool try_combination(const ref Input inp, int64_t combination)
{
    int64_t total = inp.values[0];
    for (size_t i = 1; i < inp.values.length; ++i)
    {
        if (combination & 1)
        {
            total *= inp.values[i];
        }
        else
        {
            total += inp.values[i];
        }
        combination >>= 1;
    }
    return total == inp.target;
}

int64_t calibrate(const ref Input inp)
{
    // Number of possible combinations:
    //    - Operator slots -> one less than the number of values
    //    - Two possible operators: + or *
    for (int64_t i = 0; i < 2 ^^ (inp.values.length.to!int64_t - 1); ++i)
    {
        // The current combination is represented by a single integer, where the
        // 0 bits represent adding and 1 bits represent multiplication; this way
        // simply incrementing i is sufficient to generate all combinations.
        if (try_combination(inp, i))
        {
            return inp.target;
        }
    }
    return 0;
}

int64_t part_1(Input[] inputs, out Input[] filtered)
{
    int64_t total = 0;
    foreach (inp; inputs)
    {
        int64_t calibration_result = inp.calibrate;
        if (!calibration_result)
        {
            filtered ~= inp;
        }
        else
        {
            total += calibration_result;
        }
    }
    return total;
}

enum Operation
{
    Add,
    Multiply,
    Concat
}

int64_t calibrate_pt2(const ref Input inp)
{
    struct _RunningTotal
    {
        int64_t total;
        size_t i;
    }

    auto queue = heapify!("a.total < b.total")([_RunningTotal(inp.values[0], 1)]);
    
    _RunningTotal do_operation(Operation op)(_RunningTotal total)
    {
        static if (op == Operation.Add)
        {
            total.total += inp.values[total.i];       
        }
        else static if (op == Operation.Multiply)
        {
            total.total *= inp.values[total.i];
        }
        else static if (op == Operation.Concat)
        {
            total.total = (total.total.to!string ~ inp.values[total.i].to!string).to!int64_t;
        }
        ++total.i;
        return total;
    }

    while (!queue.empty)
    {
        auto current = queue.front;
        queue.removeFront;
        static foreach (op; [Operation.Add, Operation.Multiply, Operation.Concat])
        {{  // static foreach's {} don't define a scope, so another pair is needed to prevent next already defined.
            auto next = do_operation!(op)(current);
            if (next.i == inp.values.length && next.total == inp.target)
            {
                return inp.target;
            }
            else if (next.total <= inp.target && next.i < inp.values.length)
            {
                queue.insert(next);
            }
        }}
    }
    return 0;
}

bool try_combination_2(const ref Input inp, int64_t combination)
{
    int64_t total = inp.values[0];
    for (size_t i = 1; i < inp.values.length; ++i)
    {
        switch (combination & 3)
        {
        case 0:
            total += inp.values[i];
            break;
        case 1:
            total *= inp.values[i];
            break;
        case 2:
            total = (total.to!string ~ inp.values[i].to!string).to!int64_t;
            break;
        case 3:
            break;
        default:
            assert(0);
        }
        combination >>= 2;
        if (total > inp.target) return 0;
    }
    return total == inp.target;
}

// Anything which passed part 1 is guaranteed to pass part 2,
// so we skip those ones.
int64_t part_2(Input[] inputs_pt2, int64_t pt1_result)
{
    return pt1_result + inputs_pt2.map!(a => a.calibrate_pt2).sum;
}

bool run_2024_day07()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    Input[] pt2_input;  // Part 1 will fill this in.
    auto pt1_solution = part_1(input, pt2_input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(pt2_input, pt1_solution);
    auto end_time = MonoTime.currTime;

    writefln("Calibration score (part 1): %s", pt1_solution);
    writefln("Calibration score (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}