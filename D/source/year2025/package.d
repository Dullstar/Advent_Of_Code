module year2025;

import std.format;
import std.stdio;
import std.file;

import year2025.list2025;

static foreach(d; days2025)
{
    mixin(format("public import year2025.day%02d;", d));
}

bool run_day_2025(int day)
{
    switch (day)
    {
    static foreach(d; days2025)
    {
        mixin(format("case %d:", d));
        mixin(format("return run_2025_day%02d();", d));
    }
    default:
        return false;
    }
    assert(false);
}