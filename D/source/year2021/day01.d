module year2021.day01;

import std.stdio;
import std.conv;
import std.string;
import core.time;

import input;

// def parse_input(filename: str) -> list[int]:
//     with open(filename, "r") as file:
//         return [int(line) for line in file]

int[] parse_input() 
{
    auto file = File(get_input_path(2021, 1), "r");
    string s;
    int[] res;
    while ((s = file.readln) !is null) {
        res ~= s.strip.to!int;
    }
    return res;
}

int get_depth_increases(const ref int[] readings) nothrow @safe
{
    int total = 0;
    for (int i = 1; i < readings.length; ++i) {
        if (readings[i] > readings[i - 1]) {
            total += 1;
        }
    }
    return total;
}

// def get_depth_increases(readings: list[int]) -> int:
//     total = 0
//     for i in range(1, len(readings)):
//         if readings[i] > readings[i - 1]:
//             total += 1
//     return total


// def sliding_window_increases(readings: list[int]) -> int:
//     return get_depth_increases([readings[i] + readings[i + 1] + readings[i + 2] for i in range(len(readings) - 2)])

int sliding_window_increases(const ref int[] readings) nothrow @safe 
{
    int[] new_readings;
    assert(readings.length >= 2);
    for (int i = 0; i < readings.length - 2; ++i) {
        new_readings ~= readings[i] + readings[i + 1] + readings[i + 2];
    }
    return get_depth_increases(new_readings);
}

// def main(input_filename: str):
//     start_time = time.time()
//     readings = parse_input(input_filename)
//     part1_start = time.time()
//     print(f"Part 1: {get_depth_increases(readings)} depth increases")
//     part2_start = time.time()
//     print(f"Part 2: {sliding_window_increases(readings)} depth increases (sliding window)")
//     end_time = time.time()

//     print("Elapsed Time:")
//     print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
//     print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
//     print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
//     print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")

bool run_2021_day01()
{
    auto start_time = MonoTime.currTime;
    auto readings = parse_input();
    auto pt1_start = MonoTime.currTime;
    auto pt1_result = get_depth_increases(readings);
    auto pt2_start = MonoTime.currTime;
    auto pt2_result = sliding_window_increases(readings);
    auto end_time = MonoTime.currTime;

    writefln("Part 1: %d depth increases", pt1_result);
    writefln("Part 2: %d depth increases (sliding window)", pt2_result);

    // This might be mixin-able.
    writeln("Elapsed Time:");
    // We request usecs and then convert to msecs for extra precision.
    // If we request msecs, we just get an integer value.
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}

// if __name__ == "__main__":
//     os.chdir(os.path.split(__file__)[0])
//     main("../../inputs/2021/day01.txt")

