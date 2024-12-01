module year2023.day19;

import core.time;
import std.stdio;
import std.regex;
import std.format;
import std.string;
import std.array;
import std.conv;
import std.stdint;
import std.algorithm;
import std.exception;

import input;

enum Check
{
    None,
    LessThan,
    GreaterThan,
}

enum Category
{
    x,
    m,
    a,
    s
}

struct Condition
{
    Check check;
    Category category;  // lhs
    int value;  // rhs
    bool compare(int lhs) const
    {
        final switch(check) {
        case Check.None:
            return true;
        case Check.LessThan:
            return lhs < value;
        case Check.GreaterThan:
            return lhs > value;
        }
    }
}

enum Action
{
    Goto,
    Accept,
    Reject,
}

struct Rule
{
    Condition condition;
    Action action;
    string dest;
    bool compare(Part p) const
    {
        return condition.compare(p[condition.category.to!size_t]);
    }
}

alias Part = int[4];

Action parse_action(string action_str)
{
    switch(action_str) {
    case "R":
        return Action.Reject;
    case "A":
        return Action.Accept;
    default:
        return Action.Goto;
    }
}

Rule parse_rule(string rule_str)
{
    static auto rule_re = regex(r"([xmas]+)([<>])([0-9]+):([AR]|[a-z]+)");
    auto match = rule_str.matchFirst(rule_re);
    if (match.empty) {
        auto act = rule_str.parse_action;
        return Rule(Condition(Check.None), act, act == Action.Goto ? rule_str : "");
    }
    Check check;
    switch (match[2])
    {
    case "<":
        check = Check.LessThan;
        break;
    case ">":
        check = Check.GreaterThan;
        break;
    default:
        assert(0);
    }
    auto act = match[4].parse_action;
    return Rule(
        Condition(check, match[1].to!Category, match[3].to!int),
        act,
        act == Action.Goto ? match[4] : ""
    );
}

struct Input
{
    Rule[][string] workflows;
    Part[] parts;
}

Input parse_input()
{
    Input input;
    static auto line_re = regex("\r?\n");

    void parse_workflow(string wf_str)
    {
        static auto wf_regex = regex(r"([a-zA-Z]+)\{(.*)\}");
        auto match = wf_str.matchFirst(wf_regex);
        enforce(!match.empty, format("Bad workflow: %s", wf_str));
        input.workflows[match[1]] = match[2].split(",").map!(a => a.parse_rule).array;
    }

    auto contents = get_input(2023, 19).strip.split(regex("\r?\n\r?\n"));
    enforce(contents.length == 2, "Bad input");
    auto part_re = regex(r"x=(\d+),m=(\d+),a=(\d+),s=(\d+)");
    foreach(part_str; contents[1].strip.split(line_re)) {
        auto match = part_str.matchFirst(part_re);
        enforce(!match.empty, format("Bad part in input: %s", part_str));
        input.parts ~= [match[1].to!int, match[2].to!int, match[3].to!int, match[4].to!int];
    }
    contents[0].strip.split(line_re).each!(a => parse_workflow(a));
    auto ptr = "in" in input.workflows;
    enforce(ptr !is null, "Required \"in\" workflow is missing.");
    return input;
}

bool check_part(const ref Part p, const ref Rule[][string] workflows)
{
    string wf = "in";
    // This doesn't check for infinite loops in the input. It just assumes they won't happen.
    outer: while (true)
    {
        auto rules = wf in workflows;
        enforce(rules !is null, format("Can't find workflow: %s", wf));
        inner: foreach(rule; *rules) {
            if (!rule.compare(p)) { 
                continue inner;
            }
            final switch(rule.action)
            {
            case Action.Accept:
                return true;
            case Action.Reject:
                return false;
            case Action.Goto:
                wf = rule.dest;
                // This continue allows us to distinguish between hitting a rule (good)
                // and falling through because none of the rules match (shouldn't happen)
                continue outer;
            }
        }
        assert(0, "At least one of the rules should have applied.");
    }
    assert(0);  // unreachable but syntactically required.
}

int part_1(const ref Input input)
{
    return input.parts.filter!(a => a.check_part(input.workflows)).map!(a => a[0] + a[1] + a[2] + a[3]).sum;
}

struct Interval
{
    int start;
    int end = -1;  // Makes Interval.size() return 0 for an empty interval.
    invariant
    {
        assert(start <= end || (start == 0 && end == -1));
    }
    int size() const
    {
        assert(start > 0 && end >= start, 
            format("Interval %s->%s isn't valid (is it empty?)", start, end)
        );
        return end - start + 1;
    }
    bool empty() const
    {
        return start == 0;  // no need to also check end; see the invariant block.
    }
}

alias PartGroup = Interval[4];

int64_t get_part_group_size(const ref PartGroup p)
{
    // For some reason, D static arrays seem to be incompatible with std.algorithm's templates,
    // but dynamic ones work fine. I have no idea why. There's probably a way to force it to take it,
    // but at a certain point we should really just write the basic foreach loop instead of being fancy;
    // way less effort than figuring out whatever chain of conversions is required.
    int64_t total = 1;
    foreach(interval; p) {
        total *= interval.size.to!int64_t;
    }
    return total;
}

struct FilterPartResult
{
    PartGroup pass;
    PartGroup fail;
}

FilterPartResult filter_part_group(const ref PartGroup p, const ref Rule rule)
{
    if (rule.condition.check == Check.None) return FilterPartResult(p);
    FilterPartResult result;
    Interval passed;
    Interval failed;
    auto interval = p[rule.condition.category];
    final switch(rule.condition.check)
    {
    case Check.LessThan:
        if (interval.start >= rule.condition.value) failed = interval;
        else if (interval.end >= rule.condition.value) {
            passed = Interval(interval.start, rule.condition.value - 1);
            failed = Interval(rule.condition.value, interval.end);
        }
        break;
    case Check.GreaterThan:
        if (interval.end <= rule.condition.value) failed = interval;
        else if (interval.start <= rule.condition.value) {
            passed = Interval(rule.condition.value + 1, interval.end);
            failed = Interval(interval.start, rule.condition.value);
        }
        break;
    case Check.None:
        assert(0);
    }
    if (!passed.empty) {
        result.pass = p;
        result.pass[rule.condition.category] = passed;
    }
    if (!failed.empty) {
        result.fail = p;
        result.fail[rule.condition.category] = failed;
    }
    return result;
}

int64_t part_2(const ref Rule[][string] workflows)
{
    PartGroup to_process = [Interval(1, 4000), Interval(1, 4000), Interval(1, 4000), Interval(1, 4000)];
    int64_t total_accepted = 0;

    void do_step(string wf, size_t i, PartGroup p)
    {
        const Rule* rule = &workflows[wf][i];
        auto step_result = filter_part_group(p, *rule);
        if (!step_result.pass[0].empty) {
            final switch(rule.action)
            {
            case Action.Accept:
                total_accepted += get_part_group_size(step_result.pass);
                break;
            case Action.Reject:
                break;
            case Action.Goto:
                do_step(rule.dest, 0, step_result.pass);
                break;
            }
        }
        if (!step_result.fail[0].empty) {
            assert(i + 1 < workflows[wf].length, format("Overflowed workflow: %s", wf));
            do_step(wf, i + 1, step_result.fail);
        }
    }
    
    do_step("in", 0, to_process);

    return total_accepted;
}

bool run_2023_day19()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input.workflows);
    auto end_time = MonoTime.currTime;

    writefln("Rating number sum (part 1): %s", pt1_solution);
    writefln("Total accepted parts (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}
