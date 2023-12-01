module year2023;

import std.format;
import std.stdio;
import std.file;

import year2023.list2023;

static foreach(d; days2023)
{
    mixin(format("public import year2023.day%02d;", d));
}

bool run_day_2023(int day)
{
    switch (day)
    {
    static foreach(d; days2023)
    {
        mixin(format("case %d:", d));
        mixin(format("return run_2023_day%02d();", d));
    }
    default:
        return false;
    }
    assert(false);
}