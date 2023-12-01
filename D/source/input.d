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

void init_path(bool use_test_input)
{
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
    return format("%04d/day%02d.txt", year, day);
}

// This is fairly limited for now. Looks for a test_input.txt file
// in the same directory as the executable
string get_test_input()
{
    return readText(get_test_input_path());
}

string get_test_input_path()
{
    return chainPath(thisExePath(), "test_input.txt").to!string;
}