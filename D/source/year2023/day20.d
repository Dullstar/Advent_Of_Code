module year2023.day20;

import std.stdio;
import std.conv;
import std.regex;
import core.time;
import std.container;
import std.typecons;
import std.string;
import std.array;

import input;

enum PulseType
{
    Low,
    High,
}

struct Pulse
{
    PulseType type;
    string src;
    string[] dest;
}

class Module
{
public:
    this(string[] listeners_, string id_)
    {
        listeners = listeners_;
        id = id_;
    }
    // Responsibility of parse input. Allows us to blindly pull stuff out of the assoc. array.
    final void activate(ref Module[string] modules)
    {
        foreach(listener; listeners) {
            auto ptr = listener in modules;
            if (ptr !is null) {
                ptr.inputs[id] = PulseType.Low;
            }
            else {
                modules[listener] = new OutputModule(listener);
                modules[listener].inputs[id] = PulseType.Low;
            }
        }
    }
    void receive_pulse(string src, PulseType input)
    {
        inputs[src] = input;
    }
    void reset()
    {
        foreach(input; inputs.keys) {
            inputs[input] = PulseType.Low;
        }
    }
    abstract Nullable!Pulse make_pulse();
    // We could probably speed this up with pointers, but setting that up could be a bit
    // of a mess, so let's do this the easy way first before some premature optimization.
    string[] listeners;
    PulseType[string] inputs;
    string id;
}

final class BroadcastModule : Module
{
public:
    this(string[] listeners_, string id_)
    {
        super(listeners_, id_); 
    }
    override Nullable!Pulse make_pulse()
    {
        return Nullable!Pulse(Pulse(PulseType.Low, id, listeners));
    }
}

final class FlipFlopModule : Module
{
public:
    this(string[] listeners_, string id_)
    {
        super(listeners_, id_); 
    }
    override Nullable!Pulse make_pulse()
    {
        if (!_armed) return Nullable!Pulse();
        _armed = false;
        on = !on;
        return Nullable!Pulse(Pulse(on ? PulseType.High : PulseType.Low, id, listeners));
    }
    override void receive_pulse(string src, PulseType input)
    {
        // Required for now, but really receive and make can quite possibly be merged.
        // They were initially done separated as an incorect way of handling multiple at the same time.
        assert(!_armed || input == PulseType.High, format("FF %s: multiple low inputs arriving at same time", id));
        _armed |= (input == PulseType.Low);
    }
    override void reset() {
        super.reset;
        on = false;
        _armed = false;
    }
    bool on = false;
private:
    bool _armed = false;
}

final class ConjuctionModule : Module
{
public:
    this(string[] listeners_, string id_)
    {
        super(listeners_, id_); 
    }
    override Nullable!Pulse make_pulse()
    {
        PulseType type = PulseType.Low;
        foreach(input; inputs.values) {
            if (input == PulseType.Low) {
                type = PulseType.High;
                break;
            }
        }
        return Nullable!Pulse(Pulse(type, id, listeners));
    }
}

// serves as a dead end that never makes pulses.
final class OutputModule : Module
{
public:
    this(string id_)
    {
        super([], id_);
    }
    override void receive_pulse(string src, PulseType input)
    {
        received_low |= (input == PulseType.Low);
    }
    override Nullable!Pulse make_pulse()
    {
        return Nullable!Pulse();
    }
    bool received_low;
    int low_step = int.max;
}

Module[string] parse_input()
{
    auto re = regex(r"([%&])?(.+) -> (.+)");
    auto file = File(get_input_path(2023, 20), "r");
    string line;
    Module[string] modules;
    while ((line = file.readln) !is null) {
        line = line.strip;
        auto match = line.matchFirst(re);
        assert(!match.empty, format("Line '%s' doesn't match the regex.", line));
        string[] listeners = match[3].split(", ").array;
        switch (match[1]) {
        case "%":
            modules[match[2]] = new FlipFlopModule(listeners, match[2]);
            break;
        case "&":
            modules[match[2]] = new ConjuctionModule(listeners, match[2]);
            break;
        case "":
            assert(match[2] == "broadcaster", format("Unexpected broadcaster name: %s", match[2]));
            modules[match[2]] = new BroadcastModule(listeners, match[2]);
            break;
        default:
            assert(0);
        }
    }
    foreach(ref mod; modules.values) {
        mod.activate(modules);
    }
    return modules;
}

int[2] push_button(ref Module[string] modules)
{
    int[2] total_pulses;
    auto pulses = DList!Pulse();
    pulses.insertBack(Pulse(PulseType.Low, "__button__", ["broadcaster"]));
    // bool[string] seen;  // = ["broadcaster": true];
    while (!pulses.empty) 
    {
        auto pulse = pulses.front;
        foreach(listener; pulse.dest) {
            // writefln("%s --%s--> %s", pulse.src, pulse.type, listener);
            total_pulses[PulseType.Low] += (pulse.type == PulseType.Low);
            total_pulses[PulseType.High] += (pulse.type == PulseType.High);
            modules[listener].receive_pulse(pulse.src, pulse.type);
            auto new_pulse = modules[listener].make_pulse();
            if (!new_pulse.isNull) pulses.insertBack(new_pulse.get);
            // auto seen_listener = listener in seen;
            // if (seen_listener !is null) writefln("Multiple pulses sent to %s", listener);
            // seen[listener] = true;
        }
        pulses.removeFront;
        // seen.clear;
    }
    return total_pulses;
}

int part_1(ref Module[string] modules)
{
    auto rx = cast(OutputModule*)("rx" in modules);
    if (rx is null) {
        writeln("No output module 'rx' found.");
        writeln("Could this be the test input for Part 1?");
        writeln("It's not valid for Part 2; Part 2 will be skipped.");
    }
    writeln(rx);
    // This probably SHOULD have loop detection but for now it doesn't.
    // On the other hand, it's not actually that bad; fortunately they didn't pull off a
    // "lmao now we gonna press it a gazillion times."
    int[2] result;
    foreach(i; 0..1000) {
        auto res = push_button(modules);
        result[0] += res[0];
        result[1] += res[1];
        if (rx !is null && rx.received_low && rx.low_step > i) {
            writeln("hi?");
            rx.low_step = i;
        }
        // writefln("Push %s gave %s low, %s high", i + 1, res[PulseType.Low], res[PulseType.High]);
        // writefln("Total: %s low, %s high\n", result[PulseType.Low], result[PulseType.High]);
    }
    return result[0] * result[1];
}

string[] merge_sets(string[] a, string[] b)
{
    bool[string] temp;
    foreach(c; a) {
        temp[c] = true;
    }
    foreach(c; b) {
        temp[c] = true;
    }
    return temp.keys;
}

string[] get_module_dependancies(ref Module[string] modules, ref string[][string] dict, string id)
{
    auto ptr = id in dict;
    if (ptr is null) {
        dict[id] = modules[id].inputs.keys;
        foreach(input; modules[id].inputs.keys) {
            dict[id] = merge_sets(get_module_dependancies(modules, dict, input), dict[id]);
        }
        return dict[id];
    }
    return *ptr;
}

// Assumes Part 1 was already run.
int part_2(ref Module[string] modules)
{
    // Okay, so this is one of those really big number problems.
    // Perhaps we should first handle the dependencies for each one.
    string[][string] dict;
    auto _ = get_module_dependancies(modules, dict, "rx");
    foreach(mod; modules) {
        writefln("Module %s", mod.id);
        writefln("    Inputs: %s", mod.inputs.keys);
        writefln("    Listeners: %s", mod.listeners);
        writefln("    Deps: %s", dict[mod.id]);
        writeln();
    }
    return 0;
}

bool run_2023_day20()
{
    auto start_time = MonoTime.currTime;
    auto modules = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = 0; //part_1(modules);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(modules);
    auto end_time = MonoTime.currTime;

    writefln("(part 1): %s", pt1_solution);
    writefln("(part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}