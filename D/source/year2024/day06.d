module year2024.day06;

import std.stdio;
import std.conv;
import std.regex;
import std.string;
import std.algorithm;
import std.array;
import std.exception;
import core.time;

import input;
import directions;  // NEW!    (as of file creation anyway)

struct Layout
{
    Grid2D!bool grid;
    Point!int start;
} 

Layout parse_input()
{
    Layout layout;
    bool[] layout_arr = [];
    Point!int layout_size = Point!int(-1, 0);
    int current_x;
    auto contents = get_input(2024, 6);
    foreach(c; contents)
    {
        switch(c)
        {
        case '.':
            layout_arr ~= false;
            break;
        case '#':
            layout_arr ~= true;
            break;
        case '\r':
            continue;
        case '\n':
            ++layout_size.y;
            if (layout_size.x == -1) layout_size.x = current_x;
            if (layout_size.x != current_x) enforce(0, "Bad size!");
            current_x = 0;
            continue;
        case '^':
            layout.start = Point!int(current_x, layout_size.y);
            layout_arr ~= false;
            break;
        default:
            enforce(0, format!("Bad char in input: %s")(c));
        }
        ++current_x;
    }
    layout.grid = new Grid2D!bool(layout_size, layout_arr);
    return layout;
}

struct Guard
{
    Point!int position;
    Point!int direction;
    size_t dir_i;
}

// If this gets used enough more times I might move it into the directions module
// but for now I'm keeping this separate.
enum DirBitmask
{
    None,
    North = 1,
    East = 2,
    South = 4,
    West = 8
}

enum DirBitmask[4] DIR_BITMASKS = [DirBitmask.North, DirBitmask.East, DirBitmask.South, DirBitmask.West];

struct Part1Return
{
    int solution;
    Grid2D!DirBitmask visited;
}

Part1Return part_1(const ref Layout layout, bool pt2_return = false)
{
    Part1Return ret;
    ret.visited = new Grid2D!DirBitmask(layout.grid.size, DirBitmask.None);
    auto guard = Guard(layout.start, NORTH, 0);
    static assert(DIRECTIONS[0] == NORTH);
    while (true)
    {
        auto pos_index = ret.visited.index_at_pt(guard.position);
        if (ret.visited.layout[pos_index] & DIR_BITMASKS[guard.dir_i])
        {
            break;
        }
        ret.visited.layout[pos_index] |= DIR_BITMASKS[guard.dir_i];
        guard.position += guard.direction;
        if (!layout.grid.in_bounds(guard.position))
        {
            ret.solution = pt2_return ? 1 : ret.visited.layout.count!(a => a != DirBitmask.None).to!int;
            return ret;
        }
        else if (layout.grid[guard.position]) 
        {
            guard.position -= guard.direction;
            guard.dir_i += 1;
            guard.dir_i %= DIRECTIONS.length;
            guard.direction = DIRECTIONS[guard.dir_i];
        }
    }
    ret.solution = 0;
    return ret;
}

int part_2(ref Layout layout, Grid2D!DirBitmask visited_pt1)
{
    int loops;
    for(int y = 0; y < visited_pt1.size.y; ++y)
    for(int x = 0; x < visited_pt1.size.x; ++x)
    {
        auto pt = Point!int(x, y);
        if (visited_pt1[pt] == DirBitmask.None || pt == layout.start) continue;
        layout.grid[pt] = true;  // modify the layout in place to avoid more allocations...
        auto result = part_1(layout, true);
        if (!result.solution) 
        {
            loops += 1;
        }
        layout.grid[pt] = false;  // ...and don't forget to change it back when you're done
    }
    return loops;
}

bool run_2024_day06()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input, pt1_solution.visited);
    auto end_time = MonoTime.currTime;

    writefln("Unique tiles visited by guard (part 1): %s", pt1_solution.solution);
    writefln("Number of times guard was looped (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}
