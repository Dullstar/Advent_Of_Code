module year2024.day12;

import std.stdio;
import std.conv;
import std.exception;
import std.container;
import core.time;

import input;
import utility;
import directions;

Grid2D!char parse_input()
{
    int x = 0;
    int y = 0;
    Point!int size = Point!int(-1, 0);
    char[] layout;
    foreach (c; get_input(2024, 12))
    {
        switch (c)
        {
        case '\n':
            y += 1;
            if (size.x == -1)
            {
                size.x = x;
            }
            enforce(size.x == x, "Bad input!");
            x = 0;
            break;
        case '\r':
            break;
        default:
            layout ~= c;
            x += 1;
            break;
        }
    }
    size.y = y;
    return new Grid2D!char(size, layout);
}

int get_region_cost(Point!int start, const ref Grid2D!char layout, ref Grid2D!bool visited)
{
    if (visited[start]) return 0;
    visited[start] = true;
    auto queue = DList!(Point!int)([start]);
    char region_id = layout[start];
    int perimeter;
    int area;
    while (!queue.empty)
    {
        auto current = queue.front;
        queue.removeFront;
        area += 1;
        foreach (dir; DIRECTIONS)
        {
            auto next = current + dir;
            if (!layout.in_bounds(next) || layout[next] != region_id) 
            {
                perimeter += 1;
            }
            else if (!visited[next])
            {
                visited[next] = true;
                queue.insert(next);
            }
        }
    }
    return area * perimeter;
}

int get_fencing_cost(Grid2D!char layout)
{
    int cost = 0;
    auto visited = new Grid2D!bool(layout.size, false);
    for (int y = 0; y < layout.size.y; ++y)
    for (int x = 0; x < layout.size.x; ++x)
    {
        cost += get_region_cost(Point!int(x, y), layout, visited);
    }
    return cost;
}

// A hacky solution to make vertex detection easier by reducing possible combinations of neighbors.
// Outside corners -> 2 neighbors are missing
//      Because of zoom: each tile is missing at most 2 neighbors.
// Inside corners -> No neighbors are missing, but one of the diagonals is missing
//      Because of zoom: A tile that has all four neighbors present is either:
//          - fully inside: all diagonals are present
//          - an inside corner: exactly one diagonal is missing
// Because of zoom: No tile can contain multiple vertices. Without zoom, one tile can contain up to four.
Grid2D!char zoom_2x(Grid2D!char layout)
{
    auto layout2x = new Grid2D!char(layout.size * 2);
    for (int y = 0; y < layout.size.y; ++y)
    for (int x = 0; x < layout.size.x; ++x)
    {
        auto content = layout[x, y];
        auto t1 = Point!int(x * 2, y * 2);
        auto t2 = t1 + Point!int(1, 0);
        auto t3 = t1 + Point!int(0, 1);
        auto t4 = t1 + Point!int(1, 1);
        layout2x[t1] = content;
        layout2x[t2] = content;
        layout2x[t3] = content;
        layout2x[t4] = content;
    }
    return layout2x;
}

enum Point!int[4] CORNERS = [NORTHWEST, NORTHEAST, SOUTHWEST, SOUTHEAST];

int get_region_cost_pt2(Point!int start, const ref Grid2D!char layout2x, ref Grid2D!bool visited) 
{
    if (visited[start]) return 0;
    visited[start] = true;
    auto queue = DList!(Point!int)([start]);
    char region_id = layout2x[start];
    int area;
    int sides = 0;
    while (!queue.empty)
    {
        auto current = queue.front;
        queue.removeFront;
        area += 1;
        int neighbors_missing = 0;
        foreach (dir; DIRECTIONS)
        {
            auto next = current + dir;
            if (!layout2x.in_bounds(next) || layout2x[next] != region_id) 
            {
                neighbors_missing += 1;
            }
            if (layout2x.in_bounds(next) && layout2x[next] == region_id && !visited[next])
            {
                visited[next] = true;
                queue.insert(next);
            }
        }
        assert(neighbors_missing <= 2);
        if (neighbors_missing == 2)
        {
            sides += 1;  // sides == vertices
        }
        else if (neighbors_missing == 0)
        {
            foreach (dir; CORNERS)
            {
                auto corner = current + dir;
                if (!layout2x.in_bounds(corner) || layout2x[corner] != region_id)
                {
                    sides += 1;
                    break;
                }
            }
        }
    }
    return (area / 4) * sides;  // we have to undo the zoom for the area calculation.
}


int get_fencing_cost_pt2(Grid2D!char layout)
{
    
    auto layout2x = layout.zoom_2x;
    int cost = 0;
    auto visited = new Grid2D!bool(layout2x.size, false);
    for (int y = 0; y < layout2x.size.y; ++y)
    for (int x = 0; x < layout2x.size.x; ++x)
    {
        cost += get_region_cost_pt2(Point!int(x, y), layout2x, visited);
    }
    return cost;
}

bool run_2024_day12()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = get_fencing_cost(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = get_fencing_cost_pt2(input);
    auto end_time = MonoTime.currTime;
    writefln("Fencing cost (part 1): %s", pt1_solution);
    writefln("Discounted fencing cost (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}
