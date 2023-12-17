module year2023.day16;

import std.stdio;
import std.conv;
import std.string;
import std.exception;
import std.container;
import std.algorithm;
import core.time;

import input;
import utility;

alias Grid = Grid2D!Tile;
alias Pt = Point!int;

enum Direction
{
    North,
    East,
    South,
    West
}

// Why not just make these the values of the Direction enum?
// It breaks switch case, so that's why.
enum NORTH = Pt(0, -1);
enum EAST = Pt(1, 0);
enum SOUTH = Pt(0, 1);
enum WEST = Pt(-1, 0);
const Pt[4] directions = [NORTH, EAST, SOUTH, WEST];

enum TileType: char
{
    None = '.',
    SplitterHorizontal = '-',
    SplitterVertical = '|',
    MirrorForward = '/',    // short for MirrorForwardSlash
    MirrorBack = '\\'       //           MirrorBackSlash
}

struct BeamPath
{
    bool[4] dirs;
    bool has_beam()
    {
        foreach(beam; dirs) {
            if (beam) return true;
        }
        return false;
    }
}

struct Beam
{
    Pt pos;
    Direction dir;
}

struct Tile
{
    TileType type;
    BeamPath beams;
}

Grid parse_input()
{ 
    Pt size;
    Tile[] layout;
    auto pattern = File(get_input_path(2023, 16));
    string line;
    while((line = pattern.readln.strip) !is null) {
        if (size.x == 0) size.x = line.length.to!int;
        enforce(size.x == line.length.to!int, "Bad input.");
        size.y += 1;
        foreach(c; line) {
            layout ~= Tile(c.to!TileType);
        }
    }
    return new Grid(size, layout);
}

Beam[] advance_beam(Beam beam, TileType type)
{
    final switch(type) {
    case TileType.None:
        return [Beam(beam.pos + directions[beam.dir], beam.dir)];
    case TileType.SplitterHorizontal:
        return handle_horizontal_split(beam);
    case TileType.SplitterVertical:
        return handle_vertical_split(beam);
    case TileType.MirrorForward:
        return [handle_mirror_forward(beam)];
    case TileType.MirrorBack:
        return [handle_mirror_back(beam)];
    }
}

Beam[] handle_horizontal_split(Beam beam)
{
    final switch(beam.dir) {
    case Direction.East:
    case Direction.West:
        return [Beam(beam.pos + directions[beam.dir], beam.dir)];
    case Direction.North:
    case Direction.South:
        return [Beam(beam.pos + EAST, Direction.East), Beam(beam.pos + WEST, Direction.West)];
    }
}

Beam[] handle_vertical_split(Beam beam)
{
    final switch(beam.dir) {
    case Direction.North:
    case Direction.South:
        return [Beam(beam.pos + directions[beam.dir], beam.dir)];
    case Direction.East:
    case Direction.West:
        return [Beam(beam.pos + NORTH, Direction.North), Beam(beam.pos + SOUTH, Direction.South)];
    }
}

// These can get a little confusing, but remember that the direction we're
// passing in is the direction of travel, not the direction we approach from.
// Example: if we are traveling north, we're approaching from the south.
Beam handle_mirror_forward(Beam beam)
{ 
    final switch(beam.dir) {
    case Direction.North:
        return Beam(beam.pos + EAST, Direction.East);
    case Direction.East:
        return Beam(beam.pos + NORTH, Direction.North);
    case Direction.South:
        return Beam(beam.pos + WEST, Direction.West);
    case Direction.West:
        return Beam(beam.pos + SOUTH, Direction.South);
    }
}

Beam handle_mirror_back(Beam beam)
{
    final switch(beam.dir) {
    case Direction.North:
        return Beam(beam.pos + WEST, Direction.West);
    case Direction.East:
        return Beam(beam.pos + SOUTH, Direction.South);
    case Direction.South:
        return Beam(beam.pos + EAST, Direction.East);
    case Direction.West:
        return Beam(beam.pos + NORTH, Direction.North);
    }
}

void process_beam(Grid grid, Beam _beam)
{
    DList!Beam queue;
    // We can't use the grid[Pt] opIndex overload here due to a bug with it I'm not sure how to fix
    // since D seems to have opinions about returning references.
    // opIndex is returning a copy, so when we modify it nothing happens (I feel like this should be a warning...)
    grid.layout[grid.index_at_pt(_beam.pos)].beams.dirs[_beam.dir] = true;
    queue.insertBack(_beam);
    while (!queue.empty) {
        auto beam = queue.front;
        foreach(bm; advance_beam(beam, grid[beam.pos].type)) {
            if (grid.in_bounds(bm.pos) && !grid[bm.pos].beams.dirs[bm.dir]) {
                grid.layout[grid.index_at_pt(bm.pos)].beams.dirs[bm.dir] = true;
                queue.insertBack(bm);
            }
        }
        queue.removeFront;
    }
    return;
}

int solve_beam(Grid grid, Beam beam)
{
    grid.process_beam(beam);
    return grid.layout.count!(t=>t.beams.has_beam).to!int;
}

void reset(Grid grid)
{
    foreach(ref tile; grid.layout) {
        tile.beams.dirs[] = false;
    }
}

int part_2(Grid grid)
{
    int best = 0;
    foreach(y; 0..grid.size.y) {
        foreach(beam; [Beam(Pt(0, y), Direction.East), Beam(Pt(grid.size.x - 1, y), Direction.West)]) {
            grid.reset;
            int res = solve_beam(grid, beam);
            if (res > best) best = res;
        }
    }
    foreach(x; 0..grid.size.x) {
        foreach(beam; [Beam(Pt(x, 0), Direction.South), Beam(Pt(x, grid.size.y - 1), Direction.North)]) {
            grid.reset;
            int res = solve_beam(grid, beam);
            if (res > best) best = res;
        }
    }
    return best;
}

bool run_2023_day16()
{
    auto start_time = MonoTime.currTime;
    auto layout = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = solve_beam(layout, Beam(Pt(0, 0), Direction.East));
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(layout);
    auto end_time = MonoTime.currTime;

    writefln("Energized tiles (part 1): %s", pt1_solution);
    writefln("Energized tiles (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}

void pretty_print(Grid grid)
{
    writefln("Grid2D: %s by %s", grid.size.x, grid.size.y);
    foreach (y; 0..grid.size.y) {
        foreach(x; 0..grid.size.x) {
            write(grid[x, y].beams.has_beam ? '#' : '.');
        }
        writeln;
    }
    return;
}