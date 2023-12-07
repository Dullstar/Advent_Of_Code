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
import std.traits;

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

// The typenames in the std library ranges seem to be an issue if I want to pass them around...
// so simple solution, let's just make our own.
struct CustRange
{
    int64_t start;
    int64_t end;  // INCLUDED

    bool opBinaryRight(string op: "in", T)(T n) if (isIntegral!T) {
        return (n >= start) && (n <= end);
    }
    
    static CustRange from_size(int64_t _start, int64_t size)
    {
        return CustRange(_start, _start + size - 1);
    }
}

struct Remapper
{
    this(const ref PlantMap[] raw_rules) {
        rules = raw_rules
            .map!(a => RemapRule(CustRange.from_size(a.source, a.range_size), a.dest - a.source)).array
            .sort!((a, b) => a.source.start < b.source.start).array;
    }
    RemapRule[] rules;

    CustRange[] remap(CustRange in_range) {
        CustRange[] out_range;
        foreach(rule; rules) {
            if (in_range.start in rule.source) {
                if (in_range.end in rule.source) {
                    out_range ~= CustRange(
                        in_range.start + rule.dest_offset, 
                        in_range.end + rule.dest_offset
                    );
                    return out_range;
                }
                else {  // start is in the range, but end is not.
                    out_range ~= CustRange(
                        in_range.start + rule.dest_offset,
                        rule.source.end + rule.dest_offset
                    );  // do what we can
                    in_range.start = rule.source.end + 1;  // change our range to be the chunk we didn't do yet.
                    continue;  // technically doesn't do anything but hopefully more clear.
                }
            }
            else if (in_range.start < rule.source.start) { // there's stuff before our (remaining) rules start that needs the identity mapping
                if (in_range.end < rule.source.start) { // it's fully outside the range of (remaining) rules
                    out_range ~= in_range;
                    return out_range;
                }
                else {  // the range STARTS before our rules, but doesn't END before our rules end.
                    out_range ~= CustRange(in_range.start, rule.source.start - 1);
                    in_range.start = rule.source.start;
                }
            }
            // there's also when in_range.start > rule.source.end, but we don't handle it until all rules are processed.
        }
        if (in_range.start > rules[$-1].source.end) {
            out_range ~= in_range;
        }
        return out_range;
    }

    CustRange[] remap_range(const ref CustRange[] in_ranges)
    {
        CustRange[] out_range;
        foreach(in_range; in_ranges) {
            out_range ~= remap(in_range);
        }
        return out_range;
    }
}

struct RemapRule
{
    CustRange source;
    int64_t dest_offset;
}

CustRange[] transform_ranges(const ref CustRange[] in_ranges, const ref PlantMap[] rules)
{
    auto remapper = new Remapper(rules);
    auto out_ranges = remapper.remap_range(in_ranges);
    return out_ranges;
}

int64_t part_2(const ref SeedsInfo seeds_info)
{
    // Reinterpret the input.
    CustRange[] seeds;
    int64_t temp_seed = 0;
    foreach (i, seed; seeds_info.seeds) {
        if ((i & 1) == 0) {
            temp_seed = seed;
        }
        else {
            seeds ~= CustRange.from_size(temp_seed, seed);
        }
    }

    auto soil = transform_ranges(seeds, seeds_info.map_dict["seed-to-soil map:"]);
    auto fert = transform_ranges(soil, seeds_info.map_dict["soil-to-fertilizer map:"]);
    auto water = transform_ranges(fert, seeds_info.map_dict["fertilizer-to-water map:"]);
    auto light = transform_ranges(water, seeds_info.map_dict["water-to-light map:"]);
    auto temp = transform_ranges(light, seeds_info.map_dict["light-to-temperature map:"]);
    auto humid = transform_ranges(temp, seeds_info.map_dict["temperature-to-humidity map:"]);
    auto location = transform_ranges(humid, seeds_info.map_dict["humidity-to-location map:"]);

    return location.minElement!((a, b) => a.start < b.start).start;
}

bool run_2023_day05()
{
    auto start_time = MonoTime.currTime;
    auto plant_maps = parse_input;

    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(plant_maps);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(plant_maps);
    auto end_time = MonoTime.currTime;

    writefln("Closest location (part 1): %s", pt1_solution);
    writefln("Closest location (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}