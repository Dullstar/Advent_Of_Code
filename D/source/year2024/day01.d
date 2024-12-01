module year2024.day01;

import std.array;
import std.range;
import std.string;
import std.conv;
import std.stdio;
import std.regex;
import std.algorithm;
import std.exception;
import std.math;
import core.time;

import input;

struct Lists
{
    void add_pair(int lhs, int rhs)
    {
        left ~= lhs;
        right ~= rhs;
    }
    int[] left;
    int[] right;
}

Lists parse_input()
{
    string contents = get_input(2024, 1);
    auto split_contents = contents.strip.split(regex("\r?\n"));
    Lists output;
    foreach(line; split_contents) 
    {
        auto temp = line.split();
        output.add_pair(temp[0].to!int, temp[1].to!int);
    }
    return output;
}

int get_list_distance(ref Lists lists)
{
    assert(lists.left.length == lists.right.length);
    // Note: the original ordering is lost because std.algorithm.sort modifies the original range
    // Not an issue because Part 2 doesn't need the original order.
    return zip(lists.left.sort, lists.right.sort).map!(a => abs(a[0] - a[1])).sum;
}

int get_similarity_score_simple(ref Lists lists)
{
    int sum = 0;
    foreach (left_num; lists.left)
    {
        sum += count(lists.right, left_num) * left_num;
    }
    return sum;
}

int get_similarity_score_caching(ref Lists lists)
{
    // Mostly this just demonstrates that count is sufficiently fast for a dataset of this size
    // for caching the result to potentially end up being slower, at least not using an associative array.
    int sum = 0;
    auto right = SortedRange!(int[], "a<b", SortedRangeOptions.assumeSorted)(lists.right);
    int[int] counts;
    foreach (left_num; lists.left)
    {
        int* ptr = left_num in counts;
        int score;
        if (ptr !is null) {
            score = *ptr;
        }
        else {
            score = count(right, left_num).to!int * left_num;
            counts[left_num] = score;
        }
        sum += score;
    }
    return sum;
}

int get_similarity_score_fast(ref Lists lists)
{
    int sum = 0;
    // This takes advantage of the fact that we had to sort the lists in Part 1.
    // This is probably not worth the trouble for a dataset of the size given, but I wanted to compare.
    size_t left_i = 0;
    size_t right_i = 0;
    int count_l = 0;
    int count_r = 0;
    int last_l = lists.left[0];
    int last_r = lists.right[0];
    outer: while (left_i < lists.left.length && right_i < lists.right.length)
    {
        count_l = 0;
        count_r = 0;
        last_l = lists.left[left_i];
        last_r = lists.right[right_i];
        while (lists.left[left_i] < lists.right[right_i]) {
            left_i += 1;
            if (left_i >= lists.left.length) break outer;
            last_l = lists.left[left_i];
        } 
        while (last_l > lists.right[right_i]) {
            right_i += 1;
            if (right_i >= lists.right.length) break outer;
            last_r = lists.right[right_i];
        }
        if (last_l != last_r)
        {
            continue outer;
        }
        while (left_i < lists.left.length && last_l == lists.left[left_i]) {
            count_l += 1;
            left_i += 1;
        }
        while (right_i < lists.right.length && last_r == lists.right[right_i]) {
            count_r += 1;
            right_i += 1;
        }
        sum += count_l * count_r * last_l;
    }
    return sum;
}

bool run_2024_day01()
{
    auto start_time = MonoTime.currTime;
    auto lists = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = get_list_distance(lists);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = get_similarity_score_fast(lists);
    auto end_time = MonoTime.currTime;

    auto pt2_simple = get_similarity_score_simple(lists);
    auto pt2_compare_t1 = MonoTime.currTime;
    auto pt2_caching = get_similarity_score_caching(lists);
    auto pt2_compare_t2 = MonoTime.currTime;

    // Arguably assert is better here semantically, but there's no point in outputting the same value 3 times
    // so the enforce call makes it so the methods not used for printing are still technically being used
    // and thus can't get optimized out by the compiler and thus interfering with timing comparisons.
    enforce(pt2_solution == pt2_simple && pt2_solution == pt2_caching);

    writefln("Total Distance (part 1): %s", pt1_solution);
    writefln("Similarity Score (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writeln("    Part 2:");
    writefln("        Fast: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("        Simple: %s ms", float((pt2_compare_t1 - end_time).total!"usecs") / 1000);
    writefln("        Caching: %s ms", float((pt2_compare_t2 - pt2_compare_t1).total!"usecs") / 1000);
    // Note: assumes that get_similarity_score_fast() is always the fastest regardless of hardware, compiler, stdlib implementation, etc.
    writefln("    Total (using fast pt2): %s ms", float((end_time - start_time).total!"usecs") / 1000);
    writefln("    Combined total: %s ms", float((pt2_compare_t2 - start_time).total!"usecs") / 1000);

    return true;
}
