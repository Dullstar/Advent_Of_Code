module year2025.day04;

import core.time;
import std.stdio;
import std.regex;
import std.conv;
import std.string;
import std.exception;

import input;
import utility;

enum Tile: char
{
    Empty = '.',
    Roll = '@',
    Accessible = 'x'
}

Grid2D!Tile parse_input()
{
    auto contents = get_input(2025, 4).strip.split(regex("\r?\n"));
    enforce(contents.length > 0, "Invalid input!");
    int size_y = contents.length.to!int;
    int size_x = contents[0].length.to!int;
    Tile[] layout;
    foreach(line; contents)
    {
        enforce(line.length == size_x);
        foreach (c; line)
        {
            layout ~= c.to!Tile;
        }
    }
    return new Grid2D!Tile(Point!int(size_x, size_y), layout);
}

enum Point!int[8] neighbors = 
[
    Point!int(-1, -1),
    Point!int(0, -1),
    Point!int(1, -1),
    Point!int(-1, 0),
    Point!int(1, 0),
    Point!int(-1, 1),
    Point!int(0, 1),
    Point!int(1, 1)
]; 

void pretty_print(Grid2D!Tile grid)
{
    writefln("Grid2D: %s by %s", grid.size.x, grid.size.y);
    foreach (y; 0..grid.size.y) {
        foreach(x; 0..grid.size.x) {
            write(grid[x, y].to!char);
        }
        writeln;
    }
    return;
}

int part_1(Grid2D!Tile layout)
{
    int accessible_rolls = 0;
    for (int y = 0; y < layout.size.y; ++y)
    for (int x = 0; x < layout.size.x; ++x)
    {
        Point!int pt = Point!int(x, y);
        if (layout[pt] == Tile.Empty) continue; 
        int adj_rolls = 0;
        foreach (offset; neighbors)
        {
            Point!int neighbor = pt + offset;
            adj_rolls += (layout.in_bounds(neighbor) && layout[neighbor] != Tile.Empty);
        }
        if (adj_rolls < 4)
        {
            accessible_rolls += 1;
            layout[pt] = Tile.Accessible;
        }
    }
    return accessible_rolls;
}

// part 1 is more or less just the first iteration of part 2, so...
int part_2(Grid2D!Tile layout, int pt1_solution)
{
    int total_removed_rolls;
    while (true)
    {
        // Remove any tiles that we already marked as accessible (part 1 already started this)
        foreach (ref tile; layout.layout)
        {
            if (tile == Tile.Accessible) tile = Tile.Empty;
        }
        int removed_rolls = part_1(layout);
        if (removed_rolls == 0) break;
        total_removed_rolls += removed_rolls;
    }
    return total_removed_rolls + pt1_solution;
}

bool run_2025_day04()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input, pt1_solution);
    auto end_time = MonoTime.currTime;
    writefln("Accessible rolls of paper (part 1): %s", pt1_solution);
    writefln("Rolls of paper removed (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}