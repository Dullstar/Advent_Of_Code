module input;

import std.stdio;  // TEMPORARY
import std.file;
import std.path;
import std.format;
import std.string;
import std.conv;

import run_day;

immutable input_location = "input_location.txt";
immutable test_input_location = "test_input_location.txt";

private bool _is_test = false;
bool is_test_input()
{
    return _is_test;
}

void init_path(bool use_test_input)
{
    _is_test = use_test_input;
    string location = (use_test_input) ? test_input_location : input_location;
    chdir(thisExePath.dirName);
    if (!exists(location))
    {
        ask_for_path(use_test_input);
    }
    // auto file = File(input_location, "r");
    assert(exists(location));
    auto text = readText(location);
    try 
    {
        chdir(readText(location));
    }
    catch (FileException e)
    {

        writefln("Error: Stored path \"%s\" is invalid.", text);
        ask_for_path(use_test_input);
    }
    // scope(exit) file.close();
    writefln("Retrieving inputs from: %s", getcwd);
}

void ask_for_path(bool use_test_input)
{
    write("Where are the input files located? ");
    string inpath = readln().strip();
    // We may want to allow it to be created, but for now it will do.
    string location = (use_test_input) ? test_input_location : input_location;
    if (!exists(inpath) || !isDir(inpath)) throw new Exception(format("\"%s\" is not a valid directory.", inpath));
    auto file = File(location, "w");
    scope(exit) file.close();
    file.write(inpath);
}

string get_input(int year, int day)
{
    return readText(get_input_path(year, day));
}

string get_input_path(int year, int day)
{
    return format!("%04d/day%02d.txt")(year, day);
}

// Added to handle cases where there are multiple test inputs provided.
// It's an overload instead of a default since usually this functionality isn't needed.
// Usually, these correspond to Part 1 and Part 2, but not necessarily.
// For test_no=1, the normal filename is retained, since we won't see that Part 2
// has a new example until after completing Part 1.
string get_input(int year, int day, uint test_no)
{
    assert(test_no >= 1, "test_no must be a positive nonzero number.");
    return readText(get_input_path(year, day, test_no));
}

string get_input_path(int year, int day, uint test_no)
{
    assert(test_no >= 1, "test_no must be a positive nonzero number.");
    if (!_is_test || test_no == 1) return get_input_path(year, day);
    return format!("%04d/day%02d-%d.txt")(year, day, test_no);
}