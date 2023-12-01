module year2023.day01;

import std.array;
import std.string;
import std.conv;
import std.stdio;
import std.regex;
import std.algorithm;
import std.exception;
import core.time;
import core.stdc.string;

import input;
import day01_cursed = year2023.day01_cursed;

string[] parse_input()
{
    string contents = get_input(2023, 1);
    // Unfortunately, D doesn't seem to give us the convenience of not caring about \r\n vs. \n
    auto split_contents = contents.split(regex("\r?\n"));
    return split_contents.filter!(s => s.length > 0).array;
}

int get_calibration_values_sum(string[] values, bool pt_2 = false) 
{
    int total = 0;
    foreach (value; values) {
        if (pt_2) total += process_value_pt2(value);
        else total += value.process_value;
    }
    return total;
}

int process_value(string value)
{
        char[2] digits = ['a', 'a'];
        for (int i = 0; i < value.length; ++i) {
            if (isNumeric(value[i].to!string)) {
                digits[0] = value[i];
                break;
            }
        }
        for (int i = value.length.to!int - 1; i >= 0; --i) {
            if (isNumeric(value[i].to!string)) {
                digits[1] = value[i];
                break;
            }
        }
        try {
            return digits.to!int;
        }
        catch (ConvException) {
            return 0;  // This is here to make it so the full day's code doesn't crash if given part 2's test input.
        }
}

int process_value_pt2(string value)
{
    char[2] digits = ['a', 'a'];
    for (int i = 0; i < value.length; ++i) {
        digits[0] = check_char(value, i);
        if (digits[0] != 'a') break;
    }
    for (int i = value.length.to!int - 1; i >= 0; --i) {
        digits[1] = check_char(value, i);
        if (digits[1] != 'a') break;
    }
    return digits.to!int;
}

// a return of 'a' signals failure.

char check_char(string value, size_t index)
{
    if (value[index].to!string.isNumeric) return value[index];
    string[9] numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"];
    char[9] rets = ['1', '2', '3', '4', '5', '6', '7', '8', '9'];
    foreach (i, num; numbers) {
        if (strncmp(num.toStringz, value[index..$].toStringz, num.length) == 0) {
            return rets[i];
        }
    }
    return 'a';
}

bool run_2023_day01()
{
    auto start_time = MonoTime.currTime;
    auto values = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = get_calibration_values_sum(values);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = get_calibration_values_sum(values, true);
    auto end_time = MonoTime.currTime;
    // I've placed this AFTER end_time because this technically isn't doing anything new.
    auto pt2_solution_cursed = day01_cursed.get_calibration_values_sum(values);
    auto end_time2 = MonoTime.currTime;

    // Note that in D, unlike C, %s deduces an appropriate default formatting method based on the type.
    writefln("Sum of calibration values (part 1): %s", pt1_solution);
    writefln("Sum of calibration values (part 1): %s", pt2_solution);

    enforce(pt2_solution == pt2_solution_cursed);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    writefln("    Alternate Part 2: %s ms", float((end_time2 - end_time).total!"usecs") / 1000);
    writeln("        Note: While the alternate Part 2 solution was faster in testing,");
    writeln("        it achieves that at the expense of being hyperspecific to this problem.");
    writeln("        For that reason, I've chosen to showcase the more general solution.");

    return true;
}