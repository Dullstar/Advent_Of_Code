module year2023.day12;

import std.stdint;
import std.stdio;
import std.algorithm;
import core.time;
import std.string;
import std.array;
import std.conv;
import std.exception;
import std.math;
import std.regex;
import std.range;
import std.typecons : Yes;

import input;

struct Report
{
    string condition;
    int[] run_lengths;
}

Report[] parse_input()
{
    return get_input(2023, 12).strip.split("\n")
        .map!(a=>a.strip.split)
        .map!(a=>Report(
            a[0],
            a[1].split(",").map!(b=>b.to!int).array)
        )
    .array;
}

int64_t part_2(const ref Report[] reports)
{
    Report[] reportspt2;
    
    foreach(report; reports) {
        int[] rl = report.run_lengths.dup;
        string cond = report.condition ~ '?';
        reportspt2 ~= Report(
            cond ~ cond ~ cond ~ cond ~ report.condition,
            rl ~ rl ~ rl ~ rl ~ rl 
        );
    }
    return reportspt2.part_1(true);
}

int64_t part_1(Report[] reports, bool print_progress = false)
{
    int64_t total = 0;
    foreach(report; reports) {
        // writefln("Evaluating %s", report);
        int64_t res = count_possibilities(report, print_progress);
        // writefln("    Got: %s", res);
        total += res;
    }
    return total;
}

struct CacheStorage
{
    size_t str_index;
    size_t num_index;
}

struct OkayReturn
{
    bool okay;
    size_t num_index;
}

int64_t count_possibilities(Report report, bool print_progress = false)
{
    int64_t[CacheStorage] cache;
    char[] idk = report.condition.dup;
    auto re = regex("#+");
    // I tried caching this since the other cache relies on it a lot, but it didn't work.
    // Actually, it just made it worse.
    OkayReturn okay_so_far(char[] stuff, size_t stop, bool check_full = false)
    {
        // writefln("Evaluating %s, numbers are %s", stuff[0..stop], report.run_lengths);
        size_t i = 0;
        auto matches = stuff[0..stop].matchAll(re).array;
        if (check_full && matches.length < report.run_lengths.length) return OkayReturn(false, 0);
        if (matches.length > report.run_lengths.length) return OkayReturn(false, 0);
        foreach(run; matches) {
            // writefln("    chunk %s: %s >= %s || %s != %s", run, i, report.run_lengths.length, run[0].length, report.run_lengths[i]);
            if (!check_full && run.post.length == 0) break;
            if (i >= report.run_lengths.length || run[0].length != report.run_lengths[i]) return OkayReturn(false, 0);
            i += 1;
        }
        return OkayReturn(true, matches.length);
    }

    int64_t internal(char[] stuff, size_t index)
    {
        // if (print_progress) writefln("Currently at index %s in %s", index, stuff);
        if (index == report.condition.length) {
            return okay_so_far(stuff, report.condition.length, true).okay;
        }
        if (stuff[index] == '?') {
            if (!okay_so_far(stuff, index).okay) return 0;
            auto more_stuff = stuff.dup;
            auto more_stuff2 = stuff.dup;
            more_stuff[index] = '.';
            more_stuff2[index] = '#';
            // For '.' we don't add 1 to index since the caching uses '.'
            return internal(more_stuff, index) + internal(more_stuff2, index + 1);
        }
        if (stuff[index] == '.') {
            auto ok = okay_so_far(stuff, index + 1);  // it's a stop index after all.
            if (!ok.okay) {
                // writefln("cull %s", stuff);
                return 0;
            }
            int64_t* ptr = CacheStorage(index, ok.num_index) in cache;
            if (ptr !is null) {
                // writefln("Retrieving %s from cache[%s] at %s", *ptr, CacheStorage(index, ok.num_index), stuff);
                return *ptr;
            }
            // Maybe not though...
            auto res = internal(stuff, index + 1);
            // writefln("Storing %s to cache[%s] from %s: %s", res, CacheStorage(index, ok.num_index), stuff, ok);
            cache[CacheStorage(index, ok.num_index)] = res;
            return res;
        }
        return internal(stuff, index + 1);
    }
    auto res = internal(idk, 0);
    // writeln(cache);
    return res;
}

bool run_2023_day12()
{
    auto start_time = MonoTime.currTime;
    auto reports = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(reports);
    auto pt2_start = MonoTime.currTime;
    writefln("Number of arrangements (part 1): %s", pt1_solution);
    write("Number of arrangements (part 2) (this might take a bit): ");
    auto pt2_solution = part_2(reports);
    auto end_time = MonoTime.currTime;
    writeln(pt2_solution);

    // writeln(reports);


    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}
