module year2024.day10;

import std.stdio;
import std.conv;
import std.exception;
import std.container;
import core.time;

import input;
import utility;
import directions;
import dict;  // NEW

struct Input
{
    Grid2D!int layout;
    Point!int[] trailheads;
}

Input parse_input()
{
    int x = 0;
    int y = 0;
    Point!int size = Point!int(-1, 0);
    int[] layout;
    Point!int[] trailheads;
    foreach (c; get_input(2024, 10))
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
        case '.':  // Appears in some samples even though it doesn't in the real input.
            layout ~= -1;
            x += 1;
            break;
        case '0':
            trailheads ~= Point!int(x, y);
            goto default;
        default:
            layout ~= (c ^ 0x30).to!int;
            x += 1;
            break;
        }
    }
    size.y = y;
    return Input(new Grid2D!int(size, layout), trailheads);
}

int rate_trailhead(Point!int trailhead, Grid2D!int layout)
{
    int current = layout[trailhead];
    // writefln("Current step: %s at %s", current, trailhead);
    if (current == 9) return 1;
    int score = 0;
    foreach (direction; DIRECTIONS)
    {
        auto next = trailhead + direction;
        if (layout.in_bounds(next) && layout[next] == (current + 1))
        {
            score += rate_trailhead(next, layout);
        }
    }
    return score;
}

int score_trailhead(Point!int trailhead, Grid2D!int layout)
{
    auto queue = DList!(Point!int)([trailhead]);
    auto visited = Dict!(Point!int, bool)();  // only tracks trail endpoints; the others shouldn't matter
    int score;
    while (!queue.empty)
    {
        auto current = queue.front;
        auto elevation = layout[current];
        queue.removeFront;
        if (elevation == 9)
        {
            if (visited[current].isNull)
            {
                visited[current] = true;
                ++score;
            }
            else continue;
        }
        foreach (direction; DIRECTIONS)
        {
            auto next = current + direction;
            if (layout.in_bounds(next) && layout[next] == elevation + 1)
            {
                queue.insert(next);
            }
        }
    }
    return score;
}

int part_1(Input inp)
{
    int score = 0;
    foreach (trailhead; inp.trailheads)
    {
        score += score_trailhead(trailhead, inp.layout);
    }
    return score;
}

int part_2(Input inp)
{
    int score = 0;
    foreach (trailhead; inp.trailheads)
    {
        score += rate_trailhead(trailhead, inp.layout);
    }
    return score;
}

bool run_2024_day10()
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
