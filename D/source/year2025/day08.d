module year2025.day08;

import core.time;
import std.stdio;
import std.string;
import std.conv;
import std.stdint;
import std.algorithm;
import std.array;
import std.regex;
import std.range;

import input;
import dict;

struct Point
{
    int64_t x;
    int64_t y;
    int64_t z;
}

// we can save ourselves a little computation since if a > b then sqrt(a) > sqrt(b)
// we only need to *sort* according to distance, but we don't need the actual value,
// so we can stop once we have enough info to conclude which distance is larger.
int64_t dist_sq(Point a, Point b)
{
    int64_t x = (a.x - b.x);
    int64_t y = (a.y - b.y);
    int64_t z = (a.z - b.z);
    return (x * x) + (y * y) + (z * z);
}

Point[] parse_input()
{
    return get_input(2025, 8)
        .matchAll(regex(`(\d+),(\d+),(\d+)`))
        .map!(a => Point(
            a[1].to!int64_t,
            a[2].to!int64_t,
            a[3].to!int64_t
        ))
        .array;
}

struct DistRecord
{
    int64_t dist;
    size_t first;
    size_t second;
}

struct Solution
{
    int64_t pt1_solution;
    int64_t pt2_solution;
    typeof(MonoTime.currTime) pt1_start;
    typeof(MonoTime.currTime) pt2_start;
    typeof(MonoTime.currTime) end_time;
}

Solution solve(DistRecord[] dists, Point[] input, size_t pt1_boundary)
{
    Solution result;
    result.pt1_start = MonoTime.currTime;
    int[] box_circuits;
    box_circuits.length = input.length;
    box_circuits[] = 0;
    auto circuits = Dict!(int, size_t[]).init;
    
    // Each circuit needs a unique id. Also, each isolated box is its own circuit.
    // So for simplicity we'll just set a circuit's ID to be the index of the single box it started with.
    // But as long as each circuit ID is unique, it doesn't actually matter what they are.
    for (int circuit_id = 0; circuit_id < input.length.to!int; ++circuit_id)
    {
        alias box_id = circuit_id;  // just for clarity
        box_circuits[box_id] = circuit_id;
        circuits.data[circuit_id] ~= box_id;
    }
    // Takes two circuits with different ids and makes one circuit with one id.
    // The id that's kept vs. the id that's discarded is an arbitrary choice,
    // and this behavior is not intended to be relied on.
    void merge_circuits(int a, int b)
    {
        auto ref circ_b = circuits.data[b];
        foreach(box; circ_b)
        {
            box_circuits[box] = a;
        }
        circuits.data[a] ~= circ_b;
        circuits.data.remove(b);
    }
    
    // because we need to use this twice
    void loop_body(DistRecord pair)
    {
        if (box_circuits[pair.first] != box_circuits[pair.second])
        {
            merge_circuits(box_circuits[pair.first], box_circuits[pair.second]);
        }
    }

    foreach (pair; dists[0..pt1_boundary])
    {
        loop_body(pair);
    }

    result.pt1_solution = circuits.data.values
        .topN!((a, b) => a.length > b.length)(3)
        .fold!((a, b) => a * b.length.to!int64_t)(1.to!int64_t);

    result.pt2_start = MonoTime.currTime;
    foreach (pair; dists[pt1_boundary..$])
    {
        loop_body(pair);
        if (circuits.data.length == 1)
        {
            result.pt2_solution = input[pair.first].x * input[pair.second].x;
            break;
        }
    }

    result.end_time = MonoTime.currTime;
    return result;
}

DistRecord[] get_distances(Point[] input)
{
    DistRecord[] dists;
    for (size_t first = 0; first < input.length - 1; ++first)
    for (size_t second = first + 1; second < input.length; ++second)
    {
        dists ~= DistRecord(dist_sq(input[first], input[second]), first, second);
    }
    dists.sort!((a, b) => a.dist < b.dist);
    return dists;
}

bool run_2025_day08()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto dist_start = MonoTime.currTime;
    auto dists = get_distances(input);
    // timing code is directly with the solution today, because of Part 2 picking up where Part 1 left off.
    // the times can be extracted from the return value
    size_t pt1_boundary = is_test_input ? 10 : 1000;
    auto res = solve(dists, input, pt1_boundary);
    writefln("Product of three largest circuits (part 1): %s", res.pt1_solution);
    writefln("Product of final two x coordinates (part 2): %s", res.pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((dist_start - start_time).total!"usecs") / 1000);
    writefln("    Finding pairwise distances: %s ms", float((res.pt1_start - dist_start).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((res.pt2_start - res.pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((res.end_time - res.pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((res.end_time - start_time).total!"usecs") / 1000);
    return true;
}