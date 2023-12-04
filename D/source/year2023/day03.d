module year2023.day03;

import core.time;
import std.stdio;
import std.string;
import std.conv;
import input;
import utility;
import core.stdc.stdio;
import std.algorithm;

enum TileType
{
    Empty,
    Symbol,
    Number
}

struct Tile
{
    TileType type;
    char symbol;
}

struct Number
{
    this(char* buf, ref size_t buf_index, Point!int cur_pos)
    {
        // Probably it would be more appropriate for this to be a local factory function than a constructor
        // considering some assumptions this is making about the call site...
        // Note: cur_pos will be excluded.
        xMax = cur_pos.x - 1;
        while (buf_index > 0) {
            buf_index -= 1;
            cur_pos.x -= 1;
        }
        y = cur_pos.y;
        xMin = cur_pos.x;
        // std.conv doesn't seem to know how to handle a fixed length char array, so C functions it is.
        sscanf(buf, "%d", &number);
    }
    int number;
    int xMin;
    int xMax;
    int y;
    Point!int[] get_neighbors(const ref NumberGrid grid) const 
    { 
        return _get_neighbors(xMin, xMax, y, grid); 
    }
}

// This function was historically part of Number, but I extracted it early in
// Part 2 to re-use it for the gears (could just pass the same value for xMin and xMax and it'd get the gear's neighbors),
// but given how I laid out the data in Part 1 I decided it would be easier to have the numbers check for the gears than the
// other way around, so... probably should put it back, but it's also not broken. Maybe I'll do it later if I do an improvement pass.
Point!int[] _get_neighbors(int xMin, int xMax, int y, const ref NumberGrid grid)
{
    Point!int[] neighbors;
    void add_neighbor(Point!int pt) {
        if (grid.grid.in_bounds(pt)) neighbors ~= pt;
    }
    neighbors.reserve(2 * (xMax - xMin + 1) + 6);
    foreach(x; xMin - 1 .. xMax + 2) {
        add_neighbor(Point!int(x, y + 1));
        add_neighbor(Point!int(x, y - 1));
    }
    add_neighbor(Point!int(xMin - 1, y));
    add_neighbor(Point!int(xMax + 1, y));
    return neighbors;
}

struct NumberGrid
{
    Number[] numbers;
    Point!int[] gears;
    Grid2D!Tile grid;
}

NumberGrid parse_input()
{
    Tile[] layout;
    Number[] numbers;
    Point!int[] gears;
    char[5] buffer = 0;  // 4 should be enough, (3 digits + null in case it matters for to!whatever) but I've made it bigger just in case.
    size_t buffer_index;
    bool was_num = false;
    auto file = File(get_input_path(2023, 3), "r");
    string line;
    size_t len = 0;
    int y = 0;

    void commit_number_if_applicable(size_t x) {
        if (was_num) {
            numbers ~= Number(&buffer[0], buffer_index, Point!int(x.to!int, y));
            buffer[] = 0;
            buffer_index = 0;
            was_num = false;
        }
    }

    while ((line = file.readln.strip) !is null) {
        assert(len == line.length || len == 0);
        len = line.length;
        foreach(x, c; line) {
            if (c >= '0' && c <= '9') {
                assert(c != '-');
                buffer[buffer_index++] = c;
                was_num = true;
                layout ~= Tile(TileType.Number, c);
            }
            else {
                commit_number_if_applicable(x);
                if (c == '.') {
                    layout ~= Tile(TileType.Empty, c);
                }
                else {
                    layout ~= Tile(TileType.Symbol, c);
                    if (c == '*') gears ~= Point!int(x.to!int, y);
                }
            }
        }
        commit_number_if_applicable(len);
        ++y;
    }
    return NumberGrid(numbers, gears, new Grid2D!Tile(Point!int(len.to!int, y), layout));
}

int part1(const ref NumberGrid grid)
{
    int total = 0;
    foreach (num; grid.numbers) {
        bool found = false;
        foreach (neighbor; num.get_neighbors(grid)) {
            if (grid.grid[neighbor].type == TileType.Symbol) {
                found = true;
                break;
            }
        }
        if (found) total += num.number;
    }

    return total;
}

int part2(const ref NumberGrid grid)
{
    // This is pretty janky because the data structure I did in part 1 doesn't play nice with this.
    int[][Point!int] gear_dict;
    foreach(gear; grid.gears) {
        gear_dict[gear] = [];
    }

    foreach(number; grid.numbers) {
        foreach(neighbor; number.get_neighbors(grid)) {
            int[]* p = neighbor in gear_dict;
            if (p !is null) {
                *p ~= number.number;
                break;
            }
        }
    }
    int total = 0;
    foreach (gear; gear_dict.keys) {
        if (gear_dict[gear].length > 1) total += gear_dict[gear].fold!((a, b) => a * b)(1);
    }
    return total;
}

bool run_2023_day03()
{
    auto start_time = MonoTime.currTime;
    auto grid = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part1(grid);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part2(grid);
    auto end_time = MonoTime.currTime;

    writefln("Sum of part numbers (part 1): %s", pt1_solution);
    writefln("Sum of gear ratios (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}