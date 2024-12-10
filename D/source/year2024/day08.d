module year2024.day08;

import std.stdio;
import std.conv;
import std.exception;
import core.time;

import input;
import utility;

alias Pt = Point!int;

struct Input
{
    Pt[][char] dict;
    Pt size;
}

Input parse_input()
{
    int x = 0;
    int y = 0;
    Input inp;
    inp.size = Pt(-1, 0);
    foreach (c; get_input(2024, 8))
    {
        switch (c)
        {
        case '\n':
            y += 1;
            if (inp.size.x == -1)
            {
                inp.size.x = x;
            }
            enforce(inp.size.x == x, "Bad input!");
            x = 0;
            break;
        case '\r':
            break;
        default:
            // the update function SHOULD work here but unfortunately it's too finicky because
            // it tries to be too flexible and thus enters Template Error Purgatory
            Pt[]* ptr = c in inp.dict;
            if (ptr is null)
            {
                inp.dict[c] = [Pt(x, y)];
            }
            else
            {
                inp.dict[c] ~= Pt(x, y);
            }
            goto case;
        case '.':
            x += 1;
            break;
        }
    }
    inp.size.y = y;
    return inp;
}

// I'd say boundary second makes more sense in isolation, but
// given the Grid2D version of in_bounds this should be more consistent.
bool in_bounds(Pt boundary, Pt pt)
{
    return pt.x > 0 && pt.y > 0 && pt.x < boundary.x && pt.y < boundary.y;
}

Pt find_antinode(Pt a, Pt b)
{
    int _find_axis(int first, int second)
    {
        return (2 * second) - first;
    }
    return Pt(_find_axis(a.x, b.x), _find_axis(a.y, b.y));
}

int part_1(Input input)
{
    auto grid = new Grid2D!bool(input.size, false);
    int hits = 0;
    foreach (frequency; input.dict.keys)
    {
        foreach (i, antenna_a; input.dict[frequency])
        {
            foreach (j, antenna_b; input.dict[frequency])
            {
                if (i != j)
                {
                    auto antinode = find_antinode(antenna_a, antenna_b);
                    // writefln("Found an antinode at %s,%s using beacons %s,%s and %s,%s at %s Hz",
                    //     antinode.x, antinode.y, antenna_a.x, antenna_a.y, antenna_b.x, antenna_b.y, frequency);
                    if (grid.in_bounds(antinode) && !grid[antinode])
                    {
                        hits += 1;
                        grid[antinode] = true;
                    }
                }
            }
        }
    }
    return hits;
}

int part_2(Input input)
{
    auto grid = new Grid2D!bool(input.size, false);
    int hits = 0;
    void _register_antenna(Pt antenna)
    {
        if (!grid[antenna])
        {
            hits += 1;
            grid[antenna] = true;
        }
    }
    foreach (frequency; input.dict.keys)
    {
        foreach (i, antenna_a; input.dict[frequency])
        {
            _register_antenna(antenna_a);
            foreach (j, antenna_b; input.dict[frequency])
            {
                _register_antenna(antenna_b);
                if (i != j)
                {
                    antenna_a = input.dict[frequency][i];  // gotta reset after shifting for Part 2
                    auto antinode = find_antinode(antenna_a, antenna_b);
                    while (grid.in_bounds(antinode))
                    {
                        if (!grid[antinode])
                        {
                            hits += 1;
                            grid[antinode] = true;
                        }
                        antenna_a = antenna_b;
                        antenna_b = antinode;
                        antinode = find_antinode(antenna_a, antenna_b);
                    }
                }
            }
        }
    }
    return hits;
}

bool run_2024_day08()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input);
    auto end_time = MonoTime.currTime;
    writefln("Antinodes (part 1): %s", pt1_solution);
    writefln("Antinodes (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}
