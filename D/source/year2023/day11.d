module year2023.day11;

import core.time;
import std.exception;
import std.algorithm;
import std.stdio;
import std.conv;
import std.string;
import std.math;
import std.stdint;

import utility;
import input;

enum Tile: char
{
    Empty = '.',
    Galaxy = '#',
    Debug = '!'
}

bool column_is_empty(Grid2D!Tile grid, int x)
{
    foreach (y; 0..grid.size.y) {
        if (grid[x, y] == Tile.Galaxy) return false;
    }
    return true;
}

bool row_is_empty(Grid2D!Tile grid, int y) 
{
    foreach (x; 0..grid.size.x) {
        if (grid[x, y] == Tile.Galaxy) return false;
    }
    return true;
}

Grid2D!Tile parse_input()
{
    auto file = File(get_input_path(2023, 11));
    string line;
    int size_x = 0;
    int size_y = 0;
    Tile[] layout;

    while ((line = file.readln.strip) !is null) {
        size_y += 1;
        if (size_x == 0) size_x = line.length.to!int;
        enforce(size_x == line.length, "Bad input!");
        foreach (c; line) {
            layout ~= c.to!Tile;
        }
    } 

    return new Grid2D!Tile(Point!int(size_x, size_y), layout);
}

Point!int64_t[] expand_space(Grid2D!Tile grid, int64_t expansion_size)
{
    auto expand_x = new int64_t[grid.size.x];
    auto expand_y = new int64_t[grid.size.y];
    foreach(x; 1..grid.size.x) {
        expand_x[x] = grid.column_is_empty(x - 1) * expansion_size + expand_x[x - 1];
    }
    foreach(y; 1..grid.size.y) {
        expand_y[y] = grid.row_is_empty(y - 1) * expansion_size + expand_y[y - 1];
    }
    Point!int64_t[] galaxy_coords;

    int64_t x = -1;
    int64_t y = 0;
    foreach(tile; grid.layout) {
        x += 1;
        if (x == grid.size.x) {
            x = 0;
            y += 1;
        }
        if (tile == Tile.Galaxy) {
            galaxy_coords ~= Point!int64_t(x + expand_x[x], y + expand_y[y]);
        }
    }
    return galaxy_coords;
}

// The problem statement makes it SOUND like this is pathfinding,
// but I'm pretty sure we can just Manhattan Distance it because grids.
int64_t manhattan_distance(Point!int64_t a, Point!int64_t b)
{
    return abs((a.x - b.x)) + abs((a.y - b.y));
}

T[2][] combinations_of_2(T)(T[] input)
{
    T[2][] combos;
    foreach(first; 0..input.length.to!int64_t) {
        foreach(second; (first + 1)..input.length.to!int64_t) {
            combos ~= [input[first], input[second]];
        }
    }
    return combos;
}

int64_t solve(Grid2D!Tile grid, int64_t expansion_size) 
{
    auto galaxy_coords = grid.expand_space(expansion_size);
    auto combos = galaxy_coords.combinations_of_2;
    return combos.map!(a => manhattan_distance(a[0], a[1])).sum;
}

bool run_2023_day11()
{
    auto start_time = MonoTime.currTime;
    auto galaxy_grid = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = solve(galaxy_grid, 1);
    auto pt2_start = MonoTime.currTime;
    // We have to subtract one since the problem defines it as the number of rows/columns to replace with,
    // but I've treated it as the number of rows/columns to add.
    auto pt2_solution = solve(galaxy_grid, 1_000_000 - 1);
    auto end_time = MonoTime.currTime;

    writefln("Distances (part 1): %s", pt1_solution);
    writefln("Distances (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}
