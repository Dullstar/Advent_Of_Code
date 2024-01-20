module year2023.day18;

import std.conv;
import std.string;
import std.container;
import std.algorithm;
import std.stdio;
import std.exception;
import std.regex;
import std.range;
import std.typecons;
import std.array;
import std.stdint;
import core.time;

import utility;
import input;

alias Pt = Point!int;

// There's probably some room to clean this up but for now this will do.

enum Direction: char
{
    North,
    East,
    South,
    West,
}

enum NORTH = Pt(0, -1);
enum EAST = Pt(1, 0);
enum SOUTH = Pt(0, 1);
enum WEST = Pt(-1, 0);
const Pt[4] directions = [NORTH, EAST, SOUTH, WEST];


struct Instruction
{
    Direction dir;
    int cuts;
    string color;  // good enough for now
}

Instruction[] parse_input()
{
    const Direction[string] dir_dict = 
        ["U": Direction.North, "D": Direction.South, "L": Direction.West, "R": Direction.East];
    auto re = regex(r"([UDLR]) (\d+) \(#([a-f0-9]{6})\)");
    auto contents = get_input(2023, 18);
    auto matches = contents.matchAll(re);
    Instruction[] instructions;
    foreach(match; matches) {
        instructions ~= Instruction(dir_dict[match[1]], match[2].to!int, match[3]);
    }
    return instructions;
}

enum Tile
{
    Dig = '#',
    Outside = '.',
    Unidentified = '?'
}

Pt[] run_instructions(const ref Instruction[] instructions)
{
    Pt current = Pt(0, 0);
    Pt[] vertices = [current];
    foreach(instr; instructions) {
        Pt dir = directions[instr.dir];
        // should result in 0 and +/-(cuts) for x and y, in the appropriate direction.
        Pt delta = Pt(dir.x * instr.cuts, dir.y * instr.cuts);
        current = current + delta;
        vertices ~= current;
    }
    return vertices;
}

struct Line
{
    this(int p1, int p2, int _axis_pos) 
    {
        start = min(p1, p2);
        end = max(p1, p2);
        axis_pos = _axis_pos;
    }
    invariant
    {
        assert(start <= end);
    }
    int start;
    int end;
    int axis_pos;

    int get_length() const nothrow
    {
        return end - start + 1;
    }

    string toString() const
    {
        return format("Line(%s->%s, pos %s)", start, end, axis_pos);
    }

    bool inside(int p) const nothrow
    {
        return (p >= start) && (p <= end);
    }
}

int[][int] test_dict;

Line[] get_overlaps(const ref Line[] scanline, const ref Line[] horizontals) 
{
    Line[] overlaps;
    foreach(toggler; horizontals) {
        foreach(line; scanline) {
            assert(line.axis_pos == 0);
            int start = max(toggler.start, line.start);
            int end = min(toggler.end, line.end);
            // I've excluded start == end since we never want to remove an overlap of size 1:
            // I believe it always indicates a line that's adding more area (and thus we don't want to remove it);
            // at the very least, I was unable to come up with a counterexample without allowing the digger's path to
            // intersect with itself which as far as I can tell doesn't happen in the input.
            // It's easier to ignore those overlaps here than to have the trim function ignore them since the trim
            // function needs specific handling for when there aren't any overlaps at all.
            if (start < end) overlaps ~= Line(start, end, 0);
        }
    }
    return overlaps;
}

Line[] merge_segments(const ref Line[] orig_scanline, const ref Line[] horizontal)
{
    Line[] all = orig_scanline.dup ~ horizontal.dup;
    all.sort!((a, b) => a.start < b.start).array;
    int start = all[0].start;
    int end = all[0].end;
    Line[] new_scanline;
    foreach(line; all[1..$]) {
        // +1 because e.g. 0,5 6,10 should become 0,10
        if (end + 1 >= line.start) {
            end = max(line.end, end);
        }
        else {
            new_scanline ~= Line(start, end, 0);
            start = line.start;
            end = line.end;
        }
    }
    return new_scanline ~ Line(start, end, 0);
}

int get_trim_removal_size(const ref Line orig, const ref Line[] trimmed)
{
    return orig.get_length - trimmed.fold!((int a, Line b) => a + b.get_length)(0);
}

int trim(ref Line[] scanline, const ref Line[] overlaps, const ref Line[] vertical, const ref Line[] horizontal, int y)
{
    if (overlaps.length == 0) return 0;
    int removed = 0;
    bool[int] keep;
    bool[int] starts;
    bool[int] ends;
    foreach(line; vertical) {
        if (line.start == y) keep[line.axis_pos] = true;
    }
    foreach(line; horizontal) {
        starts[line.start] = true;
        ends[line.end] = true;
    }
    foreach(overlap; overlaps) {
        Line[] new_scanline;
        // Potential edge case to worry about: two adjacent horizontal lines when the overlaps are determined.
        // I'm guessing the input will be nice enough to make this unnecessary to worry about. If it becomes a problem,
        // I think? pre-merging the horizontal lines will fix it (and maybe also deal with potential intersections?)
        foreach(line; scanline) {
            auto sorted = [line.start, line.end, overlap.start, overlap.end].sort.array;
            auto line1 = Line(sorted[0], sorted[1], 0);
            auto line2 = Line(sorted[2], sorted[3], 0);
            bool overlap1 = (line1.start == line.start && line1.end == overlap.start && line1.start != line1.end);
            bool overlap2 = (line2.start == overlap.end && line2.end == line.end && line2.start != line2.end);
            Line[] trimmed;
            if (overlap1) {
                bool keep_end = (line1.end in keep) !is null;
                trimmed ~= Line(line1.start, line1.end - !keep_end, 0);
            }
            if (overlap2) {
                bool keep_start = (line2.start in keep) !is null;
                trimmed ~= Line(line2.start + !keep_start, line2.end, 0);
            }
            if (!overlap1 && !overlap2 && !(line1.start == line1.end && line2.start == line2.end)) {
                trimmed ~= line;
            }
            removed += get_trim_removal_size(line, trimmed);
            new_scanline ~= trimmed;
        }
        scanline = new_scanline;
    }
    return removed;
}

int64_t get_scanline_area(const ref Line[] vertical, const ref Line[] horizontal, ref Line[] scanline, int y1, int y2)
in (y1 < y2, format("y1=%s should be less than y2=%s", y1, y2))
{
    auto overlaps = get_overlaps(scanline, horizontal);
    scanline = merge_segments(scanline, horizontal);
    auto removed = trim(scanline, overlaps, vertical, horizontal, y1);
    int64_t area_ish = scanline.fold!((int64_t a, Line b) => a + b.get_length)(0.to!int64_t);
    return area_ish * (y2 - y1) + removed;
}

int64_t find_area(const ref Instruction[] instructions)
{
    auto vertices = instructions.run_instructions;
    Line[] verticals;
    Line[][int] horizontals;
    assert(vertices[0] == vertices[$-1], "The instructions don't appear to be a complete circuit.");
    foreach(i, vertex1; vertices[0..$-1]) {
        auto vertex2 = vertices[i + 1];
        if (vertex1.x == vertex2.x) {
            verticals ~= Line(vertex1.y, vertex2.y, vertex1.x);
        }
        else if (vertex1.y == vertex2.y) {
            Line line = Line(vertex1.x, vertex2.x, vertex1.y);
            Line[]* ptr = vertex1.y in horizontals;
            if (ptr is null) {
                horizontals[vertex1.y] = [line];
            }
            else {
                *ptr ~= line;
            }
        }
        else assert(0, format("%s and %s don't form an axis-aligned line.", vertex1, vertex2));
    }
    verticals.sort!((a, b)=>a.axis_pos < b.axis_pos);
    bool[int] y_set;
    foreach(vertex; vertices) {
        y_set[vertex.y] = true;
    }
    int[] y_list = y_set.keys.sort.array;
    y_list ~= y_list[$-1] + 1;
    int64_t area = 0;
    Line[] scanline = [];
    foreach(i; 0..y_list.length - 1) {
        area += get_scanline_area(verticals, horizontals[y_list[i]], scanline, y_list[i], y_list[i+1]);
    }
    return area;
}

Instruction decode_hexcode(string hexstring) 
{
    int amount = hexstring[0..$-1].to!int(16);
    Direction dir;
    // We couldr revise the enum to match the numbers given, but I'd have to check to make sure I don't
    // break anything elsewhere. Maybe a change to make later.
    switch (hexstring[$-1]) {
    case '0':
        dir = Direction.East;
        break;
    case '1':
        dir = Direction.South;
        break;
    case '2':
        dir = Direction.West;
        break;
    case '3':
        dir = Direction.North;
        break;
    default:
        assert(0, format("Final character of hexstring %s doesn't correspond with any direction.", hexstring));
    }
    return Instruction(dir, amount, "");
}

int64_t part_2(Instruction[] instructions)
{
    auto new_instructions = instructions.map!(a => a.color.decode_hexcode).array;
    return find_area(new_instructions);
}

bool run_2023_day18()
{
    auto start_time = MonoTime.currTime;
    auto instructions = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = find_area(instructions);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(instructions);
    auto end_time = MonoTime.currTime;

    writefln("Lava pool size (part 1): %s", pt1_solution);
    writefln("Lava pool size (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}
