module year2023.day13;

import std.regex;
import std.stdio;
import std.array;
import std.string;
import std.exception;
import std.algorithm;
import std.conv;
import std.range;
import std.stdint;
import core.time;

import utility;
import input;

enum Tile: char
{
    Ash = '.',
    Rock = '#'
}

alias Grid = Grid2D!Tile;
alias Pt = Point!int;

Grid parse_pattern(const ref string pattern)
{
    Pt size;
    Tile[] layout;
    auto lines = pattern.split(regex("\r?\n"));
    size.y = lines.length.to!int;
    foreach(line; lines) {
        if (size.x == 0) size.x = line.length.to!int;
        enforce(size.x == line.length.to!int, "Bad input.");
        foreach(c; line) {
            layout ~= c.to!Tile;
        }
    }
    return new Grid(size, layout);
}

Grid[] parse_input()
{
    auto contents = get_input(2023, 13);
    return contents.strip.split(regex("\r?\n\r?\n")).map!(a=>a.parse_pattern).array;
}

enum Reflection
{
    Horizontal,
    Vertical,
}

struct ReflectResult
{
    Reflection reflection;
    int pos;
}

ReflectResult find_reflection_part1(const ref Grid pattern)
{
    // The names were based off reflection on a vertical line.
    bool reflect(Reflection _axis)(int x, int offset, Pt size)
    {
        assert(x > 0 && x < size.x);
        int x1 = x + offset;
        int x2 = x - offset - 1;
        if (x2 < 0 || x1 >= size.x) return true;
        foreach(y; 0..size.y) {
            static if (_axis == Reflection.Vertical)
                if (pattern[x1, y] != pattern[x2, y]) {
                    return false;
                }
            static if (_axis == Reflection.Horizontal)
                if (pattern[y, x1] != pattern[y, x2]) {
                    return false;
                }
        }
        return true;
    }

    // Technically, it should be ==, but I used <= to prevent an infinite loop if something goes wrong.
    bool done(bool[int] a, bool[int] b) { return a.length + b.length <= 1; }

    ReflectResult find_refl(int offset, ref bool[int] possible_x, ref bool[int] possible_y)
    {
        foreach(x; 1..pattern.size.x) {
            if (x in possible_x && !reflect!(Reflection.Vertical)(x, offset, pattern.size)) 
                possible_x.remove(x);
        }
        foreach(y; 1..pattern.size.y) {
            if (y in possible_y && !reflect!(Reflection.Horizontal)(y, offset, Pt(pattern.size.y, pattern.size.x)))
                possible_y.remove(y);
        }
        if (!done(possible_x, possible_y)) {
            return find_refl(offset + 1, possible_x, possible_y);
        }
        if (possible_x.length == 1) return ReflectResult(Reflection.Horizontal, possible_x.keys[0]);
        if (possible_y.length == 1) return ReflectResult(Reflection.Vertical, possible_y.keys[0]);
        assert(0, "Well, that's not good.");
    }
    bool[int] possible_x;
    bool[int] possible_y;
    iota(1, pattern.size.x).each!(a=>possible_x[a]=true);  // The true false is meaningless, I'm just not aware of any way
    iota(1, pattern.size.y).each!(a=>possible_y[a]=true);  // to make a hash set in D, but we can make a hashmap.
    return find_refl(0, possible_x, possible_y);
}

// This CAN solve Part 1 and Part 2. However, the dedicated Part 1 function is faster (probably because it needs fewer comparisons).
ReflectResult find_reflection_part2(const ref Grid pattern, int target_flaws)
{
    // This one's really just here to explicitly state this assumption instead of keeping it implicit.
    // I'm not sure how well the "done"/"clean_up" logic would hold up if targeting 2+ since a line
    // with e.g. one flaw would never be removed, but fortunately it doesn't NEED to account for that.
    assert (target_flaws <= 1, "This is not designed to handle more than 1 flaw.");
    
    // The names were based off reflection on a vertical line.
    int reflect(Reflection _axis)(int x, int offset, Pt size)
    {
        assert(x > 0 && x < size.x);
        int x1 = x + offset;
        int x2 = x - offset - 1;
        if (x2 < 0 || x1 >= size.x) return 0;
        int flaws = 0;
        foreach(y; 0..size.y) {
            static if (_axis == Reflection.Vertical)
                if (pattern[x1, y] != pattern[x2, y]) {
                    flaws += 1;
                }
            static if (_axis == Reflection.Horizontal)
                if (pattern[y, x1] != pattern[y, x2]) {
                    flaws += 1;
                }
        }
        return flaws;
    }

    // Well this got more complicated than Part 1. Slightly.
    // I'm a little concerned this may be a *smidge* too optimistic to declare completion, however.
    bool done(int[int] a, int[int] b) 
    { 
        if (a.values.length + b.values.length > 2) return false;
        return a.values.count(target_flaws) + b.values.count(target_flaws) == 1;
    }

    void clean_up(int[int] a)
    {
        foreach(pair; a.byKeyValue) {
            if (pair.value != target_flaws) a.remove(pair.key);
        }
    }

    ReflectResult find_refl(int offset, ref int[int] possible_x, ref int[int] possible_y)
    {
        int* ptr;
        assert (offset < max(pattern.size.x, pattern.size.y));
        foreach(x; 1..pattern.size.x) {
            if ((ptr = x in possible_x) !is null) {
                int flaws = reflect!(Reflection.Vertical)(x, offset, pattern.size);
                *ptr += flaws;
                if (*ptr > target_flaws) possible_x.remove(x);
            }
        }
        foreach(y; 1..pattern.size.y) {
            if ((ptr = y in possible_y) !is null) {
                int flaws = reflect!(Reflection.Horizontal)(y, offset, Pt(pattern.size.y, pattern.size.x));
                *ptr += flaws;
                if (*ptr > target_flaws) possible_y.remove(y);
            }
        }
        if (!done(possible_x, possible_y)) {
            return find_refl(offset + 1, possible_x, possible_y);
        }
        clean_up(possible_x);
        clean_up(possible_y);
        if (possible_x.length == 1) return ReflectResult(Reflection.Horizontal, possible_x.keys[0]);
        if (possible_y.length == 1) return ReflectResult(Reflection.Vertical, possible_y.keys[0]);
        assert(0, "Well, that's not good.");
    }
    int[int] possible_x;
    int[int] possible_y;
    iota(1, pattern.size.x).each!(a=>possible_x[a]=0);
    iota(1, pattern.size.y).each!(a=>possible_y[a]=0);
    return find_refl(0, possible_x, possible_y);
}

enum Part { Pt1, Pt2 }
int solve(Grid[] grids, Part pt)
{
    int[] horizontal;
    int[] vertical;
    foreach(grid; grids) {
        auto res = (pt == Part.Pt1) ? find_reflection_part1(grid) : find_reflection_part2(grid, 1);
        final switch(res.reflection) {
        case Reflection.Horizontal:
            horizontal ~= res.pos;
            break;
        case Reflection.Vertical:
            vertical ~= res.pos;
            break;
        }
    }
    return sum(horizontal) + (sum(vertical) * 100);
}

bool run_2023_day13()
{
    auto start_time = MonoTime.currTime;
    auto grids = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = solve(grids, Part.Pt1);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = solve(grids, Part.Pt2);
    auto end_time = MonoTime.currTime;

    writefln("Result of reflections (part 1): %s", pt1_solution);
    writefln("Result of flawed reflections (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}
