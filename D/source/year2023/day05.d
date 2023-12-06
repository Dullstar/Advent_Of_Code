module year2023.day05;

import std.stdio;
import core.time;
import std.string;
import std.regex;
import std.range;
import std.exception;
import std.conv;
import std.algorithm;
import std.stdint;

import input;

struct SeedsInfo
{
    int64_t[] seeds;
    PlantMap[][string] map_dict;
}

struct PlantMap
{
    int64_t dest;
    int64_t source;
    int64_t range_size;
}

SeedsInfo parse_input()
{
    auto contents = get_input(2023, 5);
    auto sections = contents.split(regex("\r?\n\r?\n"));
    SeedsInfo seeds_info;
    foreach(i, section; sections) {
        string[] lines = section.strip.split(regex("\r?\n"));
        if (i == 0) {
            string[] seedstrings = lines[0].split(":");
            enforce(seedstrings.length == 2, "Bad seeds");
            seeds_info.seeds = seedstrings[1].split.map!(a => a.to!int64_t).array;
        }
        else {
            enforce(lines.length > 1, "Bad section.");
            seeds_info.map_dict[lines[0]] = [];
            PlantMap[]* pmap = lines[0] in seeds_info.map_dict;
            foreach(line; lines[1..$]) {
                auto numbers = line.split;
                enforce(numbers.length == 3, format("Not enough numbers in line: %s", line));
                (*pmap) ~= PlantMap(
                    numbers[0].to!int64_t,
                    numbers[1].to!int64_t,
                    numbers[2].to!int64_t
                );
            }
        }
    }
    return seeds_info;
}

int64_t part_1(const ref SeedsInfo seeds_info)
{
    int64_t[] go_next_stage(string id, const ref int64_t[] input) {
        const PlantMap[]* pmap = id in seeds_info.map_dict;
        enforce(pmap !is null, format("section \"%s\" is missing", id));
        auto source_ranges = (*pmap).map!(a => iota(a.source, a.source + a.range_size)).array;
        auto dest_ranges = (*pmap).map!(a => iota(a.dest, a.dest + a.range_size)).array;
        int64_t[] output;
        foreach(number; input) {
            int64_t outnum = number;
            foreach(i, range; source_ranges) {
                if (number in range) {
                    outnum = (number - range[0]) + dest_ranges[i][0];
                    break;
                }
            }
            output ~= outnum;
        }
        return output;
    }
    auto soils = go_next_stage("seed-to-soil map:", seeds_info.seeds);
    auto fert = go_next_stage("soil-to-fertilizer map:", soils);
    auto water = go_next_stage("fertilizer-to-water map:", fert);
    auto light = go_next_stage("water-to-light map:", water);
    auto temp = go_next_stage("light-to-temperature map:", light);
    auto humid = go_next_stage("temperature-to-humidity map:", temp);
    auto location = go_next_stage("humidity-to-location map:", humid);

    return minElement(location);
}

bool run_2023_day05()
{
    auto start_time = MonoTime.currTime;
    auto plant_maps = parse_input;

    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(plant_maps);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = 0;
    auto end_time = MonoTime.currTime;

    writefln("Sum of game IDs (part 1): %s", pt1_solution);
    writefln("Sum of cube set powers (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return false;
}