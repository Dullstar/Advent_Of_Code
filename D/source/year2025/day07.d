module year2025.day07;

import core.time;
import std.stdio;
import std.regex;
import std.conv;
import std.string;
import std.exception;
import std.stdint;

import input;
import utility;

enum Tile: char
{
    Empty = '.',
    Start = 'S',
    Splitter = '^',
    Beam = '|',
}

// This function will report a failure by throwing an exception (via enforce)
// We can save a lot of bounds checking this way,
// but I really don't want to do that without explicitly verifying the assumptions that make it safe to do so.
void verify_input_assumptions(Grid2D!Tile layout)
{
    enforce(layout.size.x >= 2 && layout.size.y >= 2, "Input is too small!");
    // Top should contain exactly one S.
    // Bottom should contain only empty space.
    int start_count = 0;
    for (int x = 0; x < layout.size.x; ++x)
    {
        switch (layout[x, 0])
        {
        case Tile.Empty:
            break;
        case Tile.Start:
            start_count += 1;
            enforce(start_count <= 1, "Assumption violated: top should have exactly one S (too many detected)");
            // but now make it a beam so we can make the checks a little simpler later.
            layout[x, 0] = Tile.Beam;
            break;
        default:
            enforce(0, "Assumption violated: top should contain nothing but S");
        }
        switch (layout[x, layout.size.y - 1])
        {
        case Tile.Empty:
            break;
        default:
            enforce(0, "Assumption violated: bottom should be empty");
        }
    }
    enforce(start_count > 0, "Assumption violated: top should have exactly one S (none detected)");

    // Sides should be empty.
    // Middle contains only splitters and empty space.
    // Splitters are never directly adjacent.
    for (int y = 1; y < layout.size.y - 1; ++y)
    {
        enforce(
            layout[0, y] == Tile.Empty && layout[layout.size.x - 1, y] == Tile.Empty,
            "Assumption violated: sides should be empty"
        );
        for (int x = 1; x < layout.size.x - 1; ++x)
        {
            switch (layout[x, y])
            {
            case Tile.Empty:
                break;
            case Tile.Splitter:
                enforce(
                    layout[x-1, y] == Tile.Empty && layout[x+1, y] == Tile.Empty,
                    "Assumption violated: splitters should not be directly adjacent."
                );
                break;
            default:
                enforce(0, "Assumption violated: middle contains only splitters.");
            }
        }
    }
}

Grid2D!Tile parse_input()
{
    auto contents = get_input(2025, 7).strip.split(regex("\r?\n"));
    Point!int size = Point!int(-1, contents.length.to!int);
    Tile[] layout;
    foreach(line; contents)
    {
        if (size.x == -1) size.x = line.length.to!int;
        else enforce(size.x == line.length.to!int, "Invalid input!");
        foreach(char c; line)
        {
            layout ~= c.to!Tile;
        }
    }
    auto grid = new Grid2D!Tile(size, layout);
    verify_input_assumptions(grid);
    return grid;
}

// Due to the input assumption verification checks we did earlier,
// we don't need to check:
//   - if a splitter would clobber another splitter
//   - if a splitter attempts to place a beam out of bounds
//   - if the bottom contains splitters

int part_1(const Grid2D!Tile orig_layout)
{
    auto layout = new Grid2D!Tile(orig_layout.size, orig_layout.layout.dup);
    // There's probably few enough beams that it might be worth considering just keeping track of where the beams
    // are instead of iterating through the grid, but this shouldn't be a problem, either.
    int splitter_collisions = 0;
    for (int y = 1; y < layout.size.y; ++y)
    for (int x = 0; x < layout.size.x; ++x)
    {
        Tile current = layout[x, y];
        Tile above = layout[x, y-1];
        if (above == Tile.Beam)
        {
            switch (current)
            {
            case Tile.Splitter:
                splitter_collisions += 1;
                layout[x-1, y] = Tile.Beam;
                layout[x+1, y] = Tile.Beam;
                break;
            case Tile.Empty:
                layout[x, y] = Tile.Beam;
                break;
            default:
                break;
            }
        }
    }
    return splitter_collisions;
}

int64_t part_2(Grid2D!Tile layout)
{
    auto counts = new Grid2D!int64_t(layout.size, 0);
    foreach(i, tile; layout.layout)
    {
        if (tile == Tile.Beam) 
        {
            counts.layout[i] = 1;
            break;
        }
    }
    for (int y = 1; y < layout.size.y; ++y)
    for (int x = 0; x < layout.size.x; ++x)
    {
        int64_t above = counts[x, y-1];
        if (layout[x, y] == Tile.Splitter)
        {
            // Unfortunately these don't support += 
            counts[x-1, y] = counts[x-1, y] + above;
            counts[x+1, y] = counts[x+1, y] + above;
        }
        else
        {
            counts[x, y] = counts[x, y] + above;
        }
    }
    int64_t paths = 0;
    for (int x = 0; x < layout.size.x; ++x)
    {
        // last row should still be empty, and if we'd processed it its contents would just a continuation of the second-to-last one.
        // So we just pull the counts from the second-to-last one.
        paths += counts[x, layout.size.y-2];
    }
    return paths;
}

bool run_2025_day07()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input);
    auto end_time = MonoTime.currTime;
    writefln("Beam splits (part 1): %s", pt1_solution);
    writefln("Timelines active (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}