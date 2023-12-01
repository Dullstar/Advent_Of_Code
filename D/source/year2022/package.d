module year2022;

import std.format;
import std.stdio;
import std.file;

import year2022.list2022;

static foreach(d; days2022)
{
    // I'm honestly not sure why it doesn't like this.
    // mixin(format("public import year2022.day%02d;", d))
    mixin(format("public import year2022.day%02d;", d));
}

bool run_day_2022(int day)
{
    switch (day)
    {
    static foreach(d; days2022)
    {
        mixin(format("case %d:", d));
        mixin(format("return run_2022_day%02d();", d));
    }
    default:
        return false;
    }
    assert(false);
}