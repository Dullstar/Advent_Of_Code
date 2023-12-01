module year2023.day01_cursed;

import std.conv;
import std.string;

// This function is VERY ugly, but it's very efficient.
// The way I see it, it's worth keeping around for that reason.
// But I don't want to make it the showcased solution as it's hyperspecific to this problem;
// even a slightly different problem would require nearly completely rewriting it.
// There are tradeoffs, of course, between optimizing for the specific problem for best performance,
// and making something that's reasonably extensible, maintainable, reusable, etc.
char check_char(string value, size_t index) 
{
    enum fail = 'a';
    if (value[index].to!string.isNumeric) return value[index];
    if (value[index..$].length < 3) return fail;
    switch (value[index]) {
    case 'o':
        if ((value[index + 1] != 'n') 
            || value[index + 2] != 'e'
        ) return fail;
        return '1';
    case 't':
        switch (value[index + 1]) {
        case 'w':
            if (value[index + 2] != 'o') return fail;
            return '2';
        case 'h':
            if (value[index..$].length < 5) return fail;
            if (value[index + 2] != 'r' || value[index + 3] != 'e' || value[index + 4] != 'e') return fail;
            return '3';
        default: 
            return fail;
        }
        // return fail;
    case 'f':
        if (value[index..$].length < 4) return fail;
        switch (value[index + 1]) {
            case 'o':
                if (value[index + 2] != 'u' || value[index + 3] != 'r') return fail;
                return '4';
            case 'i':
                if (value[index + 2] != 'v' || value[index + 3] != 'e') return fail;
                return '5';
            default:
                return fail;
        }
        // return fail;
    case 's':
        switch (value[index + 1]) {
            case 'i':
                if (value[index + 2] != 'x') return fail;
                return '6';
            case 'e':
                if (value[index..$].length < 5
                    || value[index + 2] != 'v'
                    || value[index + 3] != 'e'
                    || value[index + 4] != 'n'
                ) return fail;
                return '7';
            default:
                return fail;
        }
        // return fail;
    case 'e':
        if (value[index..$].length < 5
            || value[index + 1] != 'i'
            || value[index + 2] != 'g'
            || value[index + 3] != 'h'
            || value[index + 4] != 't'
        ) return fail;
        return '8';
    case 'n':
        if (value[index..$].length < 4
            || value[index + 1] != 'i'
            || value[index + 2] != 'n'
            || value[index + 3] != 'e'
        ) return fail;
        return '9';
    default:
        return fail;
    }
    assert(0);
}

int process_value_pt2_cursed(string value)
{
    char[2] digits = ['a', 'a'];
    for (int i = 0; i < value.length; ++i) {
        digits[0] = check_char(value, i);
        if (digits[0] != 'a') break;
    }
    for (int i = value.length.to!int - 1; i >= 0; --i) {
        digits[1] = check_char(value, i);
        if (digits[1] != 'a') break;
    }
    return digits.to!int;
}

int get_calibration_values_sum(string[] values) 
{
    int total = 0;
    foreach (value; values) {
        total += process_value_pt2_cursed(value);
    }
    return total;
}
