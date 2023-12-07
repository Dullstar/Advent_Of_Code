module year2023.day07;

import std.stdio;
import std.string;
import std.array;
import std.exception;
import std.conv;
import std.algorithm;
import std.stdint;
import core.time;

import input;

static const char[15] conversions = 
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'];
enum JOKER = 11;

enum HandType
{
    HighCard,
    OnePair,
    TwoPair,
    ThreeOfAKind,
    FullHouse,
    FourOfAKind,
    FiveOfAKind
}

struct Hand
{
    this(string hand_str, int _bid, int id) {
        enforce(hand_str.length == 5);
        foreach (i, c; hand_str) {
            // the values are arbitrary as long as they're in the right order.
            switch (c) {
            case '0': .. case '9':
                // you'd think to!int, but we don't have e.g. 1, we have 0x31, the ASCII code for 1! 
                hand[i] = c ^ 0x30;  // xor by 0x30 turns an ASCII digit to the actual digit it represents.
                break;
            case 'T':
                hand[i] = 10;
                break;
            case 'J':
                hand[i] = 11;
                break;
            case 'Q':
                hand[i] = 12;
                break;
            case 'K':
                hand[i] = 13;
                break;
            case 'A':
                hand[i] = 14;
                break;
            default:
                enforce(0, format("Bad hand: %s", hand_str));
            }
        }
        bid = _bid;
    }
    int[5] hand;
    int bid;
    int id;  // this is solely a tiebreaker value in case some cards are identical.
    bool pt2 = false;

    HandType get_hand_type_shared(int best, int second_best) const
    {
        switch (best) {
        case 1:
            return HandType.HighCard;
        case 2:
            switch (second_best) {
            case 1:
                return HandType.OnePair;
            case 2:
                return HandType.TwoPair;
            default:
                assert(0);
            }
        case 3:
            switch (second_best) {
            case 1:
                return HandType.ThreeOfAKind;
            case 2:
                return HandType.FullHouse;
            default:
                assert(0);
            }
            assert(0);
        case 4:
            return HandType.FourOfAKind;
        case 5:
            return HandType.FiveOfAKind;
        default:
            assert(0);
        }
    }

    HandType get_hand_type() const
    {
        int[] counts;
        counts.length = 15;
        counts[] = 0;  // pretty sure they're already zero initialized but just in case.
        foreach(n; hand) {
            counts[n] += 1;
        }
        int jokers = counts[JOKER];
        counts.partialSort!("a > b")(3);
        if (pt2) {
            // Add jokers if there's less jokers than the best, unless jokers are tied with the best.
            // I think that can only happen if there are 2 of the best and 2 jokers.
            if (counts[0] != jokers || counts[1] == jokers) counts[0] += jokers;
            else {  // more jokers than anything else, so add the other one and promote the third best to second best.
                counts[0] += counts[1];
                counts[1] = counts[2];
            }
        }
        return get_hand_type_shared(counts[0], counts[1]);
    }

    string toString() const {
        char[5] chars;
        foreach(i, n; hand) {
            chars[i] = conversions[n];
        }
        return format("%s (%s, %s)", chars, bid, pt2);
    }

    // after reading the documentation several times (it is VERY unclear), I believe this uses
    // C-style strcmp semantics for the return value.
    int opCmp(const ref Hand other) const 
    {
        int cmp = get_hand_type.to!int - other.get_hand_type.to!int;
        if (cmp != 0) return cmp;
        foreach(i, value; hand) {
            int x = value;
            int y = other.hand[i];
            if (pt2 && (x == JOKER)) x = 1;
            if (pt2 && (y == JOKER)) y = 1;
            cmp = x - y;
            if (cmp != 0) return cmp;
        }
        cmp = (bid - other.bid);
        if (cmp != 0) return cmp;
        // The dataset contains some duplicates and D's sort DOES NOT like if we can't
        // guarantee the order the ties will be in, so this id value exists solely to break ties.
        return id - other.id;
    }
}

Hand[] parse_input()
{
    auto file = File(get_input_path(2023, 7), "r");
    string line;
    Hand[] hands;
    int hand_id;
    while ((line = file.readln) !is null) {
        auto raw_hand = line.strip.split;
        enforce(raw_hand.length == 2);
        hands ~= Hand(raw_hand[0], raw_hand[1].to!int, hand_id);
        hand_id += 1;
    }
    return hands;
}

int64_t get_score(ref Hand[] hands, bool pt2 = false) {
    if (pt2) {
        foreach (ref hand; hands) {
            hand.pt2 = true;
        }
    }
    hands.sort!((const ref Hand a, const ref Hand b) => a < b);
    int64_t total = 0;  // this is going to be way easier than trying to convince std.algorithm to cooperate.
    foreach (i, ref hand; hands) {
        total += (i + 1) * hand.bid;
    }
    return total;
}

bool run_2023_day07()
{
    auto start_time = MonoTime.currTime;
    auto hands = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = get_score(hands);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = get_score(hands, true);
    auto end_time = MonoTime.currTime;

    writefln("Score (part 1): %s", pt1_solution);
    writefln("Score (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}