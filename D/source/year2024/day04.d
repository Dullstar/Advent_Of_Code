module year2024.day04;

import std.stdio;
import std.exception;
import core.time;

import input;
import utility;


Grid2D!char parse_input()
{
    string contents = get_input(2024, 4);
    Point!int size = Point!int(-1, 0);
    int x = 0;
    char[] layout;
    layout.reserve(contents.length);
    foreach (c; contents)
    {
        switch (c)
        {
        case '\r':
            break;
        case '\n':
            if (size.x == -1)
            {
                size.x = x;
            }
            enforce(x == size.x, "Bad input (line size mismatch)");
            size.y += 1;
            x = 0;
            break;
        default:
            layout ~= c;
            x += 1;
        }
    }
    return new Grid2D!char(size, layout);
}

enum Point!int[8] neighbors = 
[
    Point!int(-1, -1),
    Point!int(-1, 0),
    Point!int(-1, 1),
    Point!int(0, -1),
    Point!int(0, 1),
    Point!int(1, -1),
    Point!int(1, 0),
    Point!int(1, 1)
];

int xmas_word_search(Grid2D!char layout)
{
    int hits = 0;
    for (int y = 0; y < layout.size.y; ++y)
    for (int x = 0; x < layout.size.x; ++x)
    {
        if (layout[x, y] == 'X')
        {
            neighbor_loop: foreach (neighbor; neighbors)
            {
                auto target_coord = Point!int(x, y);
                foreach (i, target; "MAS")
                {
                    target_coord = target_coord + neighbor;  // I don't THINK I implemented += for this.
                    if (!layout.in_bounds(target_coord) || layout[target_coord] != target)
                    {
                        continue neighbor_loop;
                    }
                }
                hits += 1;
            }
        }
    }
    return hits;
}

// I think x and + would be considered different formations here,
// but if answer is too low then we can try that, I suppose.
enum Point!int[2][2] neighbors_pt2 =
[
    [Point!int(-1, -1), Point!int(1, 1)],
    [Point!int(-1, 1), Point!int(1, -1)],
];

int xmas_word_search_pt2(Grid2D!char layout)
{
    int hits = 0;
    for (int y = 1; y < layout.size.y - 1; ++y)
    x_loop: for (int x = 1; x < layout.size.x - 1; ++x)
    {
        if (layout[x, y] == 'A')
        {
            foreach (neighbor; neighbors_pt2)
            {
                auto target1 = neighbor[0] + Point!int(x, y);
                auto target2 = neighbor[1] + Point!int(x, y);
                if 
                (
                    !(layout[target1] == 'S' && layout[target2] == 'M')
                    && !(layout[target1] == 'M' && layout[target2] == 'S')
                )
                {
                    continue x_loop;
                }
            }
            hits += 1;
        }
    }
    return hits;
}

bool run_2024_day04()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = xmas_word_search(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = xmas_word_search_pt2(input);
    auto end_time = MonoTime.currTime;

    writefln("XMAS puzzle hits (part 1): %s", pt1_solution);
    writefln("X-MAS puzzle hits (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}
