module year2025.day11;

import core.time;
import std.stdio;
import std.regex;
import std.string;
import std.exception;
import std.stdint;

import dict;
import input;

alias Network = Dict!(string, string[]);

Network parse_input(uint test_part)
{
    Network network = Network.init;
    auto contents = get_input(2025, 11, test_part).strip.split(regex("\r?\n"));
    foreach(line; contents)
    {
        auto devices = line.split(" ");
        enforce(devices.length > 1 && devices[0][$-1] == ':', "Invalid input!");
        network[devices[0][0..$-1]] = devices[1..$];
    }
    return network;
}

// As of the time of writing, network is not const due to a limitation in Dict's implementation.
// Need to experiment to get a fix working.
int64_t find_paths(ref Network network, ref Dict!(string, int64_t) cache, string start)
{
    auto num = cache[start];
    if (!num.isNull) return num.get;
    int64_t paths = 0;
    // Treat null network[start] as a dead end to avoid potential crashes/segfaults on bad inputs.
    if (network[start].isNull) return 0;
    foreach (device; network[start])
    {
        if (device == "out")
        {
            paths += 1;  // It looks like we could get away with returning 1 here,
            // as in the input it appears that devices are connected either to out, or to other devices, but never both,
            // but seeing as the loop will terminate after this iteration anyway in such cases,
            // I don't think it makes sense to rely on this implicit restriction.
        }
        else
        {
            paths += find_paths(network, cache, device);
        }
    }
    cache[start] = paths;
    return paths;
}

int64_t part_1(Network network)
{
    enforce(!network["you"].isNull, "Invalid input: starting point 'you' is missing!");
    auto cache = Dict!(string, int64_t).init;
    return find_paths(network, cache, "you");
}

struct Pt2_State
{
    string start;
    bool passed_dac = false;
    bool passed_fft = false;
}

int64_t find_paths_pt2(ref Network network, ref Dict!(Pt2_State, int64_t) cache, Pt2_State state)
{
    auto num = cache[state];
    if (!num.isNull) return num.get;
    auto devices = network[state.start];
    if (devices.isNull) return 0;
    int64_t paths = 0;
    foreach (device; devices)
    {
        Pt2_State next_state = state;
        switch(device)
        {
        case "dac":
            next_state.passed_dac = true;
            goto default;
        case "fft":
            next_state.passed_fft = true;
            goto default;
        case "out":
            if (state.passed_dac && state.passed_fft) return 1;
            break;
        default:
            paths += find_paths_pt2(
                network, cache, 
                Pt2_State(device, next_state.passed_dac, next_state.passed_fft)
            );
            break;
        }
    }
    cache[state] = paths;
    return paths;
}

int64_t part_2(Network network)
{
    enforce(!network["svr"].isNull, "Invalid input: starting point 'svr' is missing!");
    auto cache = Dict!(Pt2_State, int64_t).init;
    int64_t result = find_paths_pt2(network, cache, Pt2_State("svr"));
    return result;
}

bool run_2025_day11()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input(1);
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    if (is_test_input) input = parse_input(2);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input);
    auto end_time = MonoTime.currTime;
    writefln("Paths (part 1): %s", pt1_solution);
    writefln("Paths (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}