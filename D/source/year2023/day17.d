module year2023.day17;

import std.conv;
import std.string;
import std.container;
import std.algorithm;
import std.stdio;
import std.exception;
import core.time;

import utility;
import input;

alias Grid = Grid2D!int;
alias Pt = Point!int;

// The following reddit post was quite helpful in getting this working:
// https://www.reddit.com/r/adventofcode/comments/18luw6q/2023_day_17_a_longform_tutorial_on_day_17/
// 
// I kept my basic structure the same as it was originally (see Day 10), 
// but the thread was helpful in determining what did/did not need to be tracked,
// and helped to organize the queue better.

Grid parse_input()
{ 
    Pt size;
    int[] layout;
    auto pattern = File(get_input_path(2023, 17));
    string line;
    while((line = pattern.readln.strip) !is null) {
        if (size.x == 0) size.x = line.length.to!int;
        enforce(size.x == line.length.to!int, "Bad input.");
        size.y += 1;
        foreach(c; line) {
            layout ~= c.to!int ^ 0x30;  // ASCII -> number
        }
    }
    return new Grid(size, layout);
}

// Hmmmm, this is popping up a lot this year, might be worth putting it in utility.d
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

struct Move
{
    Pt pos;
    Direction dir;
    int dist;
}

struct MoveCost
{
    Move move;
    int cost;
    int opCmp(const ref MoveCost other) const
    {
        return cost - other.cost;
    }
}

int solve(Grid costs, int min_distance, int max_distance)
{
    bool[Move] visited;
    Pt start = Pt(0, 0);
    Pt target_pos = Pt(costs.size.x - 1, costs.size.y - 1);
    MoveCost[] container = [MoveCost(Move(start, Direction.South, 0), 0), MoveCost(Move(start, Direction.East, 0), 0)];
    // D's binary heap gives the LARGEST element by default, but the predicate "expects" less than.
    // If you feed it greater than instead, it gets reversed to instead give the smallest, which is what we want.
    auto queue = heapify!"a > b"(container);
    while (!queue.empty) {
        auto m = queue.front;
        foreach(dir, dpos; directions) {
            int dist = (dir == m.move.dir) ? m.move.dist + 1 : 0;
            if (dist >= max_distance) continue;
            if ((m.move.dist + 1 < min_distance) && (dir != m.move.dir)) continue;
            if ((dir + 2) % 4 == m.move.dir) continue;  // no backtracking.
            auto npos = m.move.pos + dpos;  // npos = *n*ew *pos*ition
            if (!costs.in_bounds(npos)) continue;
            auto nmove = Move(npos, dir.to!Direction, dist);
            if (nmove in visited) continue;
            auto ncost = m.cost + costs[npos];
            // I *think* this +1 is needed since we need to know if we can turn ON THE LAST TILE.
            if (npos == target_pos && dist + 1 >= min_distance) {
                return ncost;
            }
            queue.insert(MoveCost(nmove, ncost));
            visited[nmove] = true;
        }
        queue.removeFront;
    } 
    return enforce(0, "No path found.");
}

bool run_2023_day17()
{
    auto start_time = MonoTime.currTime;
    auto costs = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = solve(costs, 0, 3);
    writefln("Heat loss (part 1): %s", pt1_solution);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = solve(costs, 4, 10);
    auto end_time = MonoTime.currTime;

    writefln("Heat loss (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}
