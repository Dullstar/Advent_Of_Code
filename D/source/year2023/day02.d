module year2023.day02;

import core.time;
import std.regex;
import std.stdio;
import std.string;
import std.algorithm;
import std.conv;
import input;

struct Game
{
    this(string s) 
    {
        static auto id_parse = regex(r"Game (\d+)");
        static auto colors_parse = regex(r"(\d+) (b|r|g)");
        auto split_s = s.split(":");
        assert (split_s.length == 2);
        auto game_match = matchFirst(split_s[0], id_parse);
        id = game_match[1].to!int;
        auto draw_match = matchAll(split_s[1], colors_parse);
        foreach(match; draw_match) {
            switch (match[2]) {
            case "r":
                red ~= match[1].to!int;
                break;
            case "g":
                green ~= match[1].to!int;
                break;
            case "b":
                blue ~= match[1].to!int;
                break;
            default:
                assert(0);
            }
        }
    }
    // I've stored this because while the inputs seem to just increment the game number,
    // the problem doesn't explicitly state that it works like that; theoretically they
    // COULD be arbitrary numbers even if our input doesn't seem to have done it that way.
    int id;
    int[] red;
    int[] green;
    int[] blue;

    bool is_possible(int rMax, int gMax, int bMax) const {
        return (rMax >= maxElement(red) && gMax >= maxElement(green) && bMax >= maxElement(blue));
    }
}

Game[] parse_input()
{
    auto file = File(get_input_path(2023, 2), "r");
    string line;
    Game[] games;
    while ((line = file.readln) !is null) {
        line = line.strip;
        // writeln(line);
        games ~= Game(line);
    }
    return games;
}

int get_sum_of_possible_games_pt1(const ref Game[] games)
{
    enum rMax = 12;
    enum gMax = 13;
    enum bMax = 14;
    return games
        .filter!(game => game.is_possible(rMax, gMax, bMax))
        .fold!((int a, const Game b) => a + b.id)(0);
}

int get_sum_of_cube_power_sets(const ref Game[] games)
{
    int power_function(const Game game) {
        return game.red.maxElement * game.green.maxElement * game.blue.maxElement;
    }
    return games.fold!((int a, const Game b) => a + power_function(b))(0);
}

bool run_2023_day02()
{
    auto start_time = MonoTime.currTime;
    auto games = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = get_sum_of_possible_games_pt1(games);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = get_sum_of_cube_power_sets(games);
    auto end_time = MonoTime.currTime;

    writefln("Sum of game IDs (part 1): %s", pt1_solution);
    writefln("Sum of cube set powers (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}