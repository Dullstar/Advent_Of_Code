module year2021;

import std.format;
import std.stdio;
import std.file;

import year2021.list2021;

static foreach(d; days2021)
{
    mixin(format("public import year2021.day%02d;", d));
}


// I think it's extremely likely we can do something with mixin templates here but I'm not sure
// that I understand them well enough yet.
bool run_day_2021(int day)
{
    // writeln(import("day24.d"));
    switch (day)
    {
    static foreach(d; days2021)
    {
        mixin(format("case %d:", d));
        mixin(format("return run_2021_day%02d();", d));
    }
    /*case 23:
        return run_2021_day23();*/
    default:
        return false;
    }
    assert(false);
}