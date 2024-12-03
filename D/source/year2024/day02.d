module year2024.day02;

import std.string;
import std.stdio;
import std.array;
import std.regex;
import std.conv;
import std.algorithm;
import std.exception;
import std.math;
import std.typecons;
import core.time;

import input;

int[][] parse_input()
{
    string contents = get_input(2024, 2);
    auto split_contents = contents.strip.split(regex("\r?\n"));
    int[][] output;
    foreach(line; split_contents) 
    {
        output ~= line.split.map!(a => a.to!int).array;
    }
    return output;
}

bool delta_in_range(int delta)
{
    return abs(delta) >= 1 && abs(delta) <= 3;
}

bool delta_sign_matches(int delta1, int delta2)
{
    // Rejecting both == 0 is intended behavior, though it doesn't matter
    // since both == 0 also fails the range check.
    return (delta1 < 0 && delta2 < 0) || (delta1 > 0 && delta2 > 0);
}

bool is_report_safe(int[] report)
{
    enforce(report.length >= 2, "Bad length!");
    int delta = report[1] - report[0];
    if (!delta_in_range(delta)) return false;
    for (size_t i = 2; i < report.length; ++i)
    {
        int prev_delta = delta;
        delta = report[i] - report[i - 1];
        if (!delta_in_range(delta)) return false;
        if (!delta_sign_matches(delta, prev_delta)) return false;
    }
    return true;
}

int count_safe_reports(int[][] reports)
{
    return reports.map!(a => is_report_safe(a).to!int).sum;
}

bool is_report_safe_with_dampener_brute_force(int[] report, bool already_skipped=false, bool suppress_out=false)
{
    if (!is_report_safe(report))
    {
        for (int i = 0; i < report.length; ++i)
        {
            if (is_report_safe(report[0..i] ~ report[i+1..$])) return true;
        }
        return false;
    }
    return true;
}

bool delta_sign_matches(int delta1, Nullable!int delta2)
{
    if (delta2.isNull) return true;
    return (delta1 < 0 && delta2.get < 0) || (delta1 > 0 && delta2.get > 0);
}

// It passes the test inupt and my input, but during testing enough edge cases appeared
// that I'm not confident that it would pass on arbitrary valid inputs.
// But it DOES run faster than the brute force.
bool is_report_safe_with_dampener(int[] report)
{
    bool verify(int delta, Nullable!int prev_delta)
    {
        return delta_sign_matches(delta, prev_delta) && delta_in_range(delta);
    }
    int naughty = -1;
    Nullable!int prev_delta;
    Nullable!int prev_prev_delta;
    for (int i = 0; i < report.length.to!int - 1; ++i)
    {
        int delta = report[i + 1] - report[i];
        if (!verify(delta, prev_delta))
        {
            // prevents trying to remove the first element from getting skipped
            // because of the "shallower" approach
            if (naughty == 1)
            {
                prev_delta.nullify;
                prev_prev_delta.nullify;
                i = 0; // will set us to i = 1 when the loop continues
                naughty = 2;  // don't take this branch again.
                continue;
            }
            else if (naughty >= 0)
            {
                return false;
            }
            naughty = i;
            if (i + 2 >= report.length.to!int)
            {
                // Last value is the bad one.
                return true;
            }
            delta = report[i + 2] - report[i];
            if (verify(delta, prev_delta))
            {
                ++i;  // skip!
            }
            if (i - 1 < 0)
            {
                continue;
            }
            prev_delta = prev_prev_delta;
            delta = report[i + 1] - report[i - 1];
            if (!verify(delta, prev_delta))
            {
                // seems we need to also check this here; neither location alone
                // handles all identified edge cases.
                if (naughty == 1)
                {
                    prev_delta.nullify;
                    prev_prev_delta.nullify;
                    i = 0;
                    naughty = 2;
                    continue;
                }
                return false;
            }
        }
        prev_prev_delta = prev_delta;
        prev_delta = delta;
    }
    return true;
}


int count_safe_reports_with_dampener_brute_force(int[][] reports)
{
    return reports.map!(a => is_report_safe_with_dampener_brute_force(a).to!int).sum;
}

int count_safe_reports_with_dampener(int[][] reports)
{
    return reports.map!(a => is_report_safe_with_dampener(a).to!int).sum;
}

// Tries both methods and reports any mismatch.
// Brute force should always have the correct answer.
void compare_dampener_report(int[] report)
{
    bool expected = is_report_safe_with_dampener_brute_force(report);
    bool got = is_report_safe_with_dampener(report);
    if (expected != got)
    {
        writefln("Failure with sequence %s:\nExpected %s, got %s\n", report, expected, got);
    }
}

void compare_dampener_reports(int[][] reports)
{
    foreach (report; reports)
    {
        compare_dampener_report(report);
    }
}

bool run_2024_day02()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = count_safe_reports(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = count_safe_reports_with_dampener_brute_force(input);
    auto end_time = MonoTime.currTime;
    auto pt2_solution_alternate = count_safe_reports_with_dampener(input);
    auto alternate_time = MonoTime.currTime;
    
    if (pt2_solution != pt2_solution_alternate)
    {
        writeln("Oh no, I must have missed an edge case somewhere.");
        writeln("The brute force method should be correct, so that's the result that's reported.");
        writeln("Here's where the methods disagreed:");
        compare_dampener_reports(input);
        writeln("These comparisons are not included in the timing.\n");
    }

    writefln("Safe readings (part 1): %s", pt1_solution);
    writefln("Safe readings with dampener (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writeln("    Part 2:");
    writefln("        Brute force: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("        Alternate, risky: %s ms", float((alternate_time - end_time).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((alternate_time - start_time).total!"usecs") / 1000);

    return true;
}