module year2023.day06;

import std.string;
import std.stdio;
import std.exception;
import std.conv;
import std.algorithm;
import std.stdint;
import core.time;

import input;

struct Race
{
    int64_t time;
    int64_t distance;
}

Race[] parse_input()
{
    auto file = File(get_input_path(2023, 6), "r");
    string raw_line;
    string[] time_strings;
    string[] distance_strings;
    while ((raw_line = file.readln) !is null) {
        auto line = raw_line.split;
        enforce(line.length >= 2, "Bad input");
        switch (line[0]) {
        case "Time:":
            time_strings = line[1..$];
            break;
        case "Distance:":
            distance_strings = line[1..$];
            break;
        default:
            enforce(false, "Bad input");
        }
    }
    Race[] races;
    enforce(time_strings.length == distance_strings.length, "Expected the same number of times and distances.");
    races.reserve(time_strings.length);
    foreach(i, time_str; time_strings) {
        races ~= Race(time_str.to!int64_t, distance_strings[i].to!int64_t);
    }
    return races;
}

int64_t part_1(const ref Race[] races)
{
    int64_t[] wins_per_race;
    foreach(race; races) {
        int64_t wins = 0;
        foreach(wind_up; 1..race.time) {
            int64_t our_distance = wind_up * (race.time - wind_up);
            if (our_distance > race.distance) wins += 1;
        }
        wins_per_race ~= wins;
    }
    return wins_per_race.fold!((a, b) => a * b)(1.to!int64_t);
}

int64_t part_2(const ref Race[] races)
{
    // Just use the already-parsed input to reconstruct what it wants
    string timestring;
    string diststring;
    foreach (race; races) {
        timestring ~= race.time.to!string;
        diststring ~= race.distance.to!string;
    }
    auto s = [Race(timestring.to!int64_t, diststring.to!int64_t)];
    return part_1(s);
}

bool run_2023_day06()
{
    auto start_time = MonoTime.currTime;
    auto races = parse_input;

    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(races);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(races);
    auto end_time = MonoTime.currTime;

    writefln("Product of race wins (part 1): %s", pt1_solution);
    writefln("Race wins (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}