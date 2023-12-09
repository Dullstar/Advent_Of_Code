module year2023.day09;

import std.stdio;
import std.string;
import std.algorithm;
import std.exception;
import std.conv;
import std.array;
import core.time;

import input;


int[][] parse_input()
{
    auto file = File(get_input_path(2023, 9), "r");
    string line;
    int[][] OASIS_report;
    while ((line = file.readln) !is null) {
        OASIS_report ~= line.strip.split.map!(a => a.to!int).array;
    }
    return OASIS_report;
}

bool is_zeroes(const ref int[] sequence) {
    foreach(n; sequence) {
        if (n != 0) return false;
    }
    return true;
}

int predict_next_value(const ref int[] sequence) {
    if (sequence.is_zeroes) return 0;
    enforce(sequence.length > 1, format("Sequence %s isn't long enough.", sequence));
    int[] new_sequence;
    new_sequence.reserve(sequence.length - 1);
    for (size_t i = 1; i < sequence.length; ++i) {
        new_sequence ~= sequence[i] - sequence[i - 1];
    }
    assert (new_sequence.length == sequence.length - 1);
    return predict_next_value(new_sequence) + sequence[$-1];
}

int part_1(int[][] OASIS_report) {
    return OASIS_report.map!(a => a.predict_next_value).sum;
}

int part_2(int[][] OASIS_report) {
    return OASIS_report.map!(a => a.reverse.array).array.part_1;
}

bool run_2023_day09()
{
    auto start_time = MonoTime.currTime;
    auto OASIS_report = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(OASIS_report);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(OASIS_report);
    auto end_time = MonoTime.currTime;

    writefln("Sum of extrapolated next values (part 1): %s", pt1_solution);
    writefln("Sum of extrapolated previous values (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}
