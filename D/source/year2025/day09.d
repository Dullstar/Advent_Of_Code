module year2025.day09;

import core.time;
import std.stdio;
import std.regex;
import std.algorithm;
import std.stdio;
import std.array;
import std.stdint;
import std.conv;
import std.exception;
import std.format;
import std.range;

import input;
import utility;
import dict;

alias Point = utility.Point!int64_t;
Point[] parse_input()
{
    return get_input(2025, 9)
        .matchAll(regex(`(\d+),(\d+)`))
        .map!(a => Point(
            a[1].to!int64_t,
            a[2].to!int64_t,
        ))
        .array;
}

int64_t get_area(Point a, Point b)
{
    return (max(a.x, b.x) - min(a.x, b.x) + 1) * (max(a.y, b.y) - min(a.y, b.y) + 1);
}

struct Rectangle
{
    this(Point A, Point B, int64_t Area)
    {
        a = Point(min(A.x, B.x), min(A.y, B.y));
        b = Point(max(A.x, B.x), max(A.y, B.y));
        area = Area;      
    }
    Point a;
    Point b;
    int64_t area;
}

struct Pt1Result
{
    int64_t best = 0;
    Rectangle[] rects;
}

Pt1Result part_1(Point[] input)
{
    Pt1Result pt1;
    for (int64_t a = 0; a < input.length - 1; ++a)
    for (int64_t b = a + 1; b < input.length; ++b)
    {
        int64_t area = get_area(input[a], input[b]);
        pt1.best = max(pt1.best, area);
        pt1.rects ~= Rectangle(input[a], input[b], area);
    }
    return pt1;
}

// All lines in valid input should be axis-aligned.
// This was used before the Segment struct was added, but the code that
// distinguishes between vertical and horizontal lines still makes use of it.
struct Line
{
    this(Point A, Point B)
    {
        assert((A.x == B.x) ^ (A.y == B.y), "Lines should be axis aligned.");
        // I want the smaller coordinate to be first. This method only works because they're axis aligned.
        // If they weren't, then we'd potentially end up with two different points than the ones we started with.
        a = Point(min(A.x, B.x), min(A.y, B.y));
        b = Point(max(A.x, B.x), max(A.y, B.y));
    }
    Point a;
    Point b;
}

struct Segment
{
    int64_t start;
    int64_t end;
}

struct UpdateScanlineResult
{
    Segment[] scanline;
    Segment[] remove_next;
}

Segment[] process_remove_next(const ref UpdateScanlineResult s)
{
    if (s.scanline.length == 0) return [];
    if (s.remove_next.length == 0) return s.scanline.dup;
    // Descriptive names for these variables were too annoying to follow just because it was too verbose.
    size_t i, r;  // i = scanline_index; r = remove_index;
    Segment[] updated;
    while (i < s.scanline.length && r < s.remove_next.length)
    {
        if (s.scanline[i].end < s.remove_next[r].start)
        {
            updated ~= s.scanline[i++];
            continue;
        }
        assert(s.remove_next[r].end <= s.scanline[i].end);
        auto a = Segment(s.scanline[i].start, s.remove_next[r].start - 1);
        auto b = Segment(s.remove_next[r++].end + 1, s.scanline[i++].end);
        if (a.start <= a.end) updated ~= a;
        if (b.start <= b.end) updated ~= b;
    }
    while (i < s.scanline.length)
    {
        updated ~= s.scanline[i++];  // don't drop whatever's left...
    }
    return updated;
}

UpdateScanlineResult merge_adjacent(ref UpdateScanlineResult res)
{
    // only merge if there is something to merge
    if (res.scanline.length <= 1) return res;
    Segment[] merged;
    Segment current = res.scanline[0];
    foreach(i; 1..res.scanline.length)
    {
        if (current.end + 1 == res.scanline[i].start || current.end == res.scanline[i].start)
        {
            current.end = res.scanline[i].end;
        }
        else
        {
            merged ~= current;
            current = res.scanline[i];
        }
    }
    merged ~= current;
    res.scanline = merged;
    return res;
}

// Also sorts the horizontal segments.
UpdateScanlineResult update_scanline(const ref UpdateScanlineResult orig_scanline, ref Segment[] horiz)
{
    alias Result = UpdateScanlineResult;
    auto scanline = process_remove_next(orig_scanline);
    if (horiz.length == 0) return Result(scanline, []);
    horiz.sort!((a, b) => a.start < b.start);
    if (scanline.length == 0) return Result(horiz.dup, []);
    // Process the horizontal segments. If overlap other than start == end then it should remove.
    size_t s, h;
    Result res;
    while (s < scanline.length && h < horiz.length)
    {
        if (scanline[s].end < horiz[h].start)
        {
            res.scanline ~= scanline[s++];
        }
        else if (horiz[h].end < scanline[s].start)
        {
            res.scanline ~= horiz[h++];
        }
        else if (scanline[s].start == horiz[h].end)
        {
            res.scanline ~= Segment(horiz[h++].start, scanline[s++].end);
        }
        else if (scanline[s].end == horiz[h].start)
        {
            res.scanline ~= Segment(scanline[s++].start, horiz[h++].end);
        }
        else
        {
            assert (
                scanline[s].start <= horiz[h].start && horiz[h].end <= scanline[s].end,
                format!("Uh oh... Scanline: %s; Horiz: %s.\n"
                ~ "Failed comparison would be: %s <= %s && %s <= %s\n"
                ~ "Args to function: orig_scanline %s, horiz %s\n"
                ~ "current scanline set to: %s"
                )(scanline[s], horiz[h], scanline[s].start, horiz[h].start, horiz[h].end, scanline[s].end,
                    orig_scanline, horiz, scanline
                )
            );
            Segment remove = horiz[h];
            // Handles edge cases involving whether or not the start and end points get removed.
            // Basically, if it's on the edge of the current profile, it gets removed.
            // Otherwise, the start and end points are still there.
            remove.start += (scanline[s].start != horiz[h].start);
            remove.end -= (scanline[s].end != horiz[h].end);
            h += 1;
            res.remove_next ~= remove;
        }
    }
    while (s < scanline.length)
    {
        res.scanline ~= scanline[s++];  // don't drop whatever's left.
    }
    while (h < horiz.length)
    {
        res.scanline ~= horiz[h++];
    }
    return merge_adjacent(res);
}

Dict!(int64_t, Segment[]) make_scanlines(Dict!(int64_t, Segment[]) horiz)
{
    auto scanlines = Dict!(int64_t, Segment[]).init;
    auto y_positions = horiz.data.keys.sort;
    auto current = UpdateScanlineResult([], []);
    foreach(y; y_positions)
    {
        // We still need to check the y positions, because we do forcibly insert some more of them.
        // This is because when we encounter a horizontal line that removes from the shape, those
        // parts are still there for one more y.
        start:
        Segment[] this_horiz;
        auto temp = horiz[y];
        if (!temp.isNull) this_horiz = temp.get;
        auto next = update_scanline(current, this_horiz);
        if (next.scanline != current.scanline)
        {
            scanlines[y] = next.scanline;
        }
        current = next;
        if (current.remove_next.length > 0)
        {
            // See if y + 1 will be our next iteration...
            auto ptr = y + 1 in horiz.data;
            if (ptr is null)
            {
                // and if not, manually take over the next iteration.
                y += 1;
                goto start;
            }
        }
    }
    return scanlines;
}

bool check_rect(Rectangle rect, ref Dict!(int64_t, Segment[]) scanlines)
{
    auto ys = scanlines.data.keys.filter!(a => (a >= rect.a.y && a <= rect.b.y));
    outer: foreach (y; ys)
    {
        foreach(segment; scanlines[y])
        {
            if (rect.a.x >= segment.start && rect.b.x <= segment.end) continue outer;
            // We could return false in the event that we pass exactly one of those two conditions,
            // but I don't think it's worth checking for since a typical scanline has just one segment.
        }
        // reaching this point means our rectangle's width isn't contained in any segment, so it fails.
        return false;
    }
    return true;
}

int64_t part_2(Point[] input, Rectangle[] rects)
{
    auto horiz = Dict!(int64_t, Segment[]).init;
    foreach(i; 0..input.length)
    {
        auto line = Line(input[i], input[(i + 1) % $]);
        if (line.a.y == line.b.y)
        {
            auto temp = horiz[line.a.y];
            if (temp.isNull) horiz[line.a.y] = [Segment(line.a.x, line.b.x)];
            else temp.get ~= Segment(line.a.x, line.b.x);
        }
    }
    auto scanlines = make_scanlines(horiz);
    rects.sort!((a, b) => a.area > b.area);
    foreach(rect; rects)
    {
        if (check_rect(rect, scanlines)) 
        {
            return rect.area;
        }
    }
    return 0;
}

bool run_2025_day09()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input, pt1_solution.rects);
    auto end_time = MonoTime.currTime;
    writefln("Largest possible rectangle (part 1): %s", pt1_solution.best);
    writefln("??? (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}