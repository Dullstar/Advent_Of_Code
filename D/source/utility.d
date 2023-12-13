module utility;

import std.traits;
import std.format;
import std.conv;
import std.stdio;

struct Point(T)
    if (isIntegral!T)
{
    this(T x_, T y_) { this.x = x_; this.y = y_; }
    T x;
    T y;

    Point opBinary(string op)(in Point other) const if(op == "+" || op == "-")
    {
        return Point(x + other.x, y + other.y);
    }

    // Reminder: D has a default for opEquals, so we don't need to do that one.
}

class Grid2D(T, S = int)
    if (isIntegral!S)
{
public:
    this(Point!S size_, T default_fill = T.init)
    // in(size_.x > 0 && size_.y > 0, "Zero-length dimensions aren't allowed.")
    {
        size = size_;
        layout.length = size.x * size.y;
        layout[] = default_fill;
    }

    this(Point!S size_, T[] layout_)
    {
        layout = layout_;
        size = size_;
        assert (layout_.length == size_.x * size_.y, 
            format("Can't create layout: x=%s * y=%s != %s", size_.x, size_.y, layout_.length)
        );
    }

    T opIndex(S x, S y) const
    // in(x >= 0 && y >= 0 && x < size_x && x < size_y, format("%d, %d out of bounds! (must be between 0, 0 and %d, %d)"))
    {
        return layout[index_at_pt(Point!S(x, y))];
    }

    T opIndex(Point!S pt) const
    {
        return layout[index_at_pt(pt)];
    }

    void opIndexAssign(T val, Point!S pt)
    {
        layout[index_at_pt(pt)] = val;
    }

    void opIndexAssign(T val, S x, S y)
    {
        layout[index_at_pt(Point!S(x, y))] = val;
    }

    Point!S pt_at_index(size_t i) const
    // in(i < layout.length, format("Index %d out of bounds! (max: %d)", i, layout.length - 1))
    {
        return Point!S((i % size.x).to!S, (i / size.x).to!S);
    }

    size_t index_at_pt(Point!S pt) const
    {
        return (pt.y * size.x + pt.x).to!size_t;
    }

    bool in_bounds(Point!S pt) const
    {
        return pt.x >= 0 && pt.y >= 0 && pt.x < size.x && pt.y < size.y;
    }
    Point!S size;
    T[] layout;
}
 
 version(none)
 {
    // This is for copy/pasting when you need a pretty print for debugging,
    // as for a lot of types to!string doesn't work well.
    // You'd think we'd be able to make it accept a function for the string conversion,
    // but there's no examples given for passing functions to a template, particularly when
    // the type of the functions argument's is itself a template parameter.
    // I tried like 50 different ways and the compiler found like 51 different ways to say no.
    // So now it's not even TRYING to be a template and you can just replace the types yourself.
    void pretty_print(Grid2D!int grid)
    {
        writefln("Grid2D: %s by %s", grid.size.x, grid.size.y);
        foreach (y; 0..grid.size.y) {
            foreach(x; 0..grid.size.x) {
                grid[x, y].to!string;
            }
            writeln;
        }
        return;
    }
}