module year2023.day06;

import std.string;
import std.stdio;
import std.exception;
import std.conv;
import std.algorithm;
import std.stdint;
import std.math;
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

int64_t get_race_wins_product_brute_force(const ref Race[] races)
{
    int64_t total = 1;
    foreach(race; races) {
        int64_t wins = 0;
        foreach(wind_up; 1..race.time) {
            int64_t our_distance = wind_up * (race.time - wind_up);
            if (our_distance > race.distance) wins += 1;
        }
        total *= wins;
    }
    return total;
}

// Calculates the roots of the quadratic formula and then returns the number of ints between them.
// Because of the problem's constraints we can safely assume that the roots are at least 1 and at most (time - 1).
// The a variable is always -1 in this context, so this function is simplified with that in mind.
// For anyone reading this for help, I've erred on the side of overcommenting this.
//
// Where did the quadratic come from?
// Let w = wind up time, t = available time, r = record distance, and d = our distance
// d = speed * remaining_time
// The problem gives us that our speed = w, and after we wind up our remaining_time = (t - w)
// Substitute to get d = w * (t - w). We want d > r, so that means w * (t - w) > r.
// Multiply (distributive property) for wt - w^2 > r, rearrange to get -w^2 + wt - r > 0
// which is a quadratic inequality ax^2 + bx + c > 0 with a = -1, b = t, and c = -r
int64_t quadratic_range_size(int64_t _b, int64_t _c)
{

    double b = _b.to!double;
    double c = _c.to!double; 
    // Quadratic formula, simplified for a = -1
    double n1 = (-b + sqrt(pow(b, 2) + (4 * c))) / -2;
    double n2 = (-b - sqrt(pow(b, 2) + (4 * c))) / -2;
    // Normally, we'd need to handle the inequality, but given our possible inputs,
    // we know it'll always be min(n1, n2) < wind_up_time < max(n1, n2) to win.
    // It's possible that n1 or n2 may fall in a consistent ordering, but I didn't check.
    int64_t start = trunc(min(n1, n2)).to!int64_t + 1;  // why not ceil? We want e.g. 5.0 to become 6, not 5, but ceil would give 5.
    // end isn't included, so start = 2; end = 5; would represent the ints 2, 3, 4. It works out slightly nicer that way.
    int64_t end = ceil(max(n1, n2)).to!int; 
    return end - start;
}

int64_t get_race_wins_product_math(const ref Race[] races) {
    return races.fold!((int64_t a, Race b) => a * quadratic_range_size(b.time, -b.distance))(1.to!int64_t);
}

Race[] part_2_adjust(const ref Race[] races)
{
    // Just use the already-parsed input to reconstruct what it wants
    string timestring;
    string diststring;
    foreach (race; races) {
        timestring ~= race.time.to!string;
        diststring ~= race.distance.to!string;
    }
    return [Race(timestring.to!int64_t, diststring.to!int64_t)];
}

bool run_2023_day06()
{
    auto start_time = MonoTime.currTime;
    auto races = parse_input;
    auto races_pt2 = races.part_2_adjust;

    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = get_race_wins_product_brute_force(races);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = get_race_wins_product_brute_force(races_pt2);
    auto end_time = MonoTime.currTime;

    writefln("Product of race wins (brute force) (part 1): %s", pt1_solution);
    writefln("Race wins (brute force) (part 2): %s", pt2_solution);

    auto pt1_start_math = MonoTime.currTime;
    auto pt1_solution_math = get_race_wins_product_math(races);
    auto pt2_start_math = MonoTime.currTime;
    auto pt2_solution_math = get_race_wins_product_math(races_pt2);
    auto end_time_math = MonoTime.currTime;

    writefln("Product of race wins (using math) (part 1): %s", pt1_solution_math);
    writefln("Race wins (using math) (part 2): %s", pt2_solution_math);

    writeln("Elapsed Time (brute force):");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    writeln("Elapsed Time (math):");
    // Parsing is the same line from above since the original parse can just be reused.
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start_math - pt1_start_math).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time_math - pt2_start_math).total!"usecs") / 1000);
    // Get the total for math, but then add the parse time back.
    writefln("    Total: %s ms", 
        float(((pt1_start - start_time) + (end_time_math - pt1_start_math)).total!"usecs") / 1000
    );

    return true;
}