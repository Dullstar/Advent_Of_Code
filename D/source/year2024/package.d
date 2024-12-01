module year2024;

import std.format;
import std.stdio;
import std.file;

import year2024.list2024;

static foreach(d; days2024)
{
    mixin(format("public import year2024.day%02d;", d));
}

bool run_day_2024(int day)
{
    switch (day)
    {
    static foreach(d; days2024)
    {
        mixin(format("case %d:", d));
        mixin(format("return run_2024_day%02d();", d));
    }
    default:
        return false;
    }
    assert(false);
}