module year2021.day23;

import std.stdio;
import std.conv;
import std.format;
import std.container;

import input;
import utility;
 /*
alias Point = utility.Point!int;

enum Tile
{
    Empty = 0,
    A = 1,
    B = 10,
    C = 100,
    D = 1000,
    Wall = -1
}

immutable size_t[] occupiable_indices_pt_1 = 
[
    14, 15, 17, 19, 21, 23, 24, 
    29, 31, 33, 35,
    42, 44, 46, 48
];

// There's probably a way to avoid this intermediate.
immutable size_t[] additional_occupiable_indices_pt_2 = 
[
    55, 57, 59, 61,
    68, 70, 72, 74
];

immutable size_t[] occupiable_indices_pt_2 = occupiable_indices_pt_1 ~ additional_occupiable_indices_pt_2;

struct InputReturn
{
    string startpos;
    Grid2D!Tile empty_layout;
}

struct Move
{
    string new_pos;
    int cost;
    bool has_priority;  // means this move should ALWAYS be taken if it is available.
}

auto string_to_layout(string pos, const ref Grid2D!Tile empty_layout, const ref size_t[] occupiable_indices)
{
    assert(pos.length == occupiable_indices.length);
    auto grid = new Grid2D!Tile(empty_layout.size, empty_layout.layout.dup);
    foreach (i, c; pos)
    {
        grid.layout[occupiable_indices[i]] = 
            (c == '.') ? Tile.Empty : c.to!string.to!Tile;  // string intermediate is required, can't convert char to enum.
    }
    return grid;
}

struct Change
{
    this(size_t from_, size_t to_)
    {
        change = true;
        from = from_;
        to = to_;
    }
    bool change = false;
    size_t from;
    size_t to;
}
auto layout_to_string(const ref Grid2D!Tile layout, const ref size_t[] occupiable_indices, Change change=Change())
{

    char[] str;
    char held;
    foreach (i; occupiable_indices)
    {
        char c = (layout.layout[i] == Tile.Empty) ? '.' : layout.layout[i].to!string[0];
        if (change.change && i == change.from)
        {
            held = c;
        }
    }
    if (change.change)
    {
        str[change.from] = '.';
        str[change.to] = held;
    }
    return str.to!string;
}

auto get_costs(const ref Grid2D!Tile empty_layout, const ref size_t[] indices)
{
    Grid2D!int[size_t] costs;
    foreach(i; indices)
    {
        writefln("Testing index: %d", i);
        costs[i] = _get_costs_individual(empty_layout.pt_at_index(i), empty_layout);
    }
    return -1;
}

Grid2D!int _get_costs_individual(Point pos, const ref Grid2D!Tile empty_layout)
{
    writefln("Testing point: %s", pos);
    auto queue = DList!Point(pos);
    auto neighbors = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)];
    auto costs = new Grid2D!int(empty_layout.size, -1);
    costs[pos] = 0;
    while (!queue.empty)
    {
        auto pt = queue.front();
        queue.removeFront();
        int current_cost = costs[pt];
        foreach(n; neighbors)
        {
            auto new_pt = pt + n;
            if (!empty_layout.in_bounds(new_pt)) continue;
            auto new_index = empty_layout.index_at_pt(new_pt);
            if (empty_layout.layout[new_index] != Tile.Wall && costs.layout[new_index] == -1)
            {
                costs.layout[new_index] = current_cost + 1;
                queue.insert(new_pt);
            }
        }
    }
    print_costs(costs);
    writeln();
    return costs;
}

auto get_moves(
    string str_layout,
    const ref Grid2D!Tile empty_layout,
    const ref Grid2D!int[size_t] costs,
    const ref size_t[] occupiable_indices,
    Move[][string] known_moves
)
{
    auto ptr = str_layout in known_moves;
    if (ptr !is null) return *ptr;
    auto layout = string_to_layout(str_layout, empty_layout, occupiable_indices);
    Move[] moves;
    foreach (i; occupiable_indices)
    {
        if (layout.layout[i] != Tile.Empty)
        {
            auto mv = _get_moves_individual(i, layout, costs[i], occupiable_indices, empty_layout);
            if (mv.length > 0 && mv[0].has_priority)
            {
                auto ret = mv;
                known_moves[str_layout] = ret;
                return ret;
            }
            else moves ~= mv;
        }
    }
    known_moves[str_layout] = moves;
    return moves;
}

Move[] _get_moves_individual(
    size_t pos,
    const ref Grid2D!Tile layout, 
    const ref Grid2D!int costs,
    const ref size_t[] occupiable_indices,
    const ref Grid2D!Tile empty_layout
)
{
    auto stuff = new Grid2D!int(empty_layout.size, -1);
    auto queue = DList!Point(layout.pt_at_index(pos));
    auto neighbors = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)];
    Move[] moves;
    while (!queue.empty)
    {
        auto pt = queue.front();
        queue.removeFront();
        foreach(n; neighbors)
        {
            auto new_pt = pt + n;
            if (!empty_layout.in_bounds(new_pt)) continue;
            auto new_index = empty_layout.index_at_pt(new_pt);
            if (
                empty_layout.layout[new_index] != Tile.Wall 
                && layout.layout[new_index] == Tile.Empty 
                && stuff.layout[new_index] == -1)
            {
                stuff.layout[new_index] = 0;
                int test = 0;
                Move mv = {
                    new_pos: layout_to_string(layout, occupiable_indices, Change(pos, new_index)),
                    cost: costs.layout[new_index],
                    has_priority: new_index >= 29
                };
                queue.insert(new_pt);
            }
        }
    }
    throw new Exception("Not implemented yet.");
}

bool _move_ok(size_t start_pos, size_t new_pos, const ref Grid2D!Tile layout)
{
    // Stuff not in the hallway can only move into the hallway.
    if (start_pos >= 29)
    {
        return new_pos < 29;
    }
}

bool _locked(size_t pos, const ref Grid2D!Tile layout, const ref int[] occupiable_indices)
{
    if (pos < 29) return false;
    
}

void print_layout(const ref Grid2D!Tile layout)
{
    size_t x = 0;
    foreach (c; layout.layout)
    {
        switch(c)
        {
        case Tile.Empty:
            write(" ");
            break;
        case Tile.Wall:
            write("#");
            break;
        default:
            write(c);
        }
        x += 1;
        if (x == layout.size.x)
        {
            x = 0;
            writeln();
        }
    }
}

void print_costs(const ref Grid2D!int layout)
{
    size_t x = 0;
    foreach (c; layout.layout)
    {
        if (c == -1)
            writef("   ");
        else 
        {
            writef("%02d ", c);
        }
        x += 1;
        if (x == layout.size.x)
        {
            x = 0;
            writeln();
        }
    }
}

InputReturn parse_input()
{
    auto contents = get_input(2021, 23);
    writeln(contents);
    Tile[] layout;
    layout.reserve(13 * 5);
    char[] startpos;
    auto x = 0;
    auto max_x = -1;
    foreach(c; contents)
    {        
        x += 1;
        switch (c)
        {
        case 'A':
        case 'B':
        case 'C':
        case 'D':
            startpos ~= c;
            goto case;
        case ' ':
        case '.':
            layout ~= Tile.Empty;
            break;
        case '#':
            layout ~= Tile.Wall;
            break;
        // case 'A':
        // case 'B':
        // case 'C':
        // case 'D':
            // layout ~= c.to!string.to!Tile;  // the string intermediate is required, unfortunately
            // break;
        case '\n':
            if (x < max_x)  // inelegant but effective; makes sure the empty spaces on the bottom right don't get left out
            {
                layout ~= Tile.Empty;
                layout ~= Tile.Empty;
            }
            else { max_x = x; }  // This is done this way and not hardcoded just to pre-emptively prevent any Windows /r shenanigans.
            x = 0;
            break;
        case '\r':  // in case of Windows stupidity.
            break;
        default:
            assert(0);
        }
    }
    assert(layout.length == 13 * 5, format("layout length %d doesn't equal 13 * 5 = %d", layout.length, 13 * 5));
    InputReturn output = 
        {startpos: "......." ~ startpos.to!string, empty_layout: new Grid2D!Tile(Point(13, 5), layout)};
    return output;
}

bool run_2021_day23()
{
    writeln("We're inside here. Just checking in.\n");

    auto input = parse_input();
    auto thing = string_to_layout(input.startpos, input.empty_layout, occupiable_indices_pt_1);
    print_layout(thing);
    get_costs(input.empty_layout, occupiable_indices_pt_1);
    return false;
}

*/

bool run_2021_day23()
{
    return false;
    // Looks like I broke it at some point before this was added to git, so for now we just want to keep it out of the way.
}