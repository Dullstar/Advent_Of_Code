module run_day;

import std.format;
import std.stdio;

import year2021;
import year2022;
import year2023;

const int MAX_YEAR = 2023;
const int MIN_YEAR = 2015;

struct Day
{	
	this(int year_, int day_)
	{
		year = year_;
		day = day_;
		if (year < MIN_YEAR || year > MAX_YEAR) 
		{
			auto test = format("Year must be between %d and %d; %d was provided", MIN_YEAR, MAX_YEAR, year);
			throw new Exception(test);
		}
		if (day < 1 || day > 25) 
		{
			throw new Exception(format("Day must be between %d and %d; %d was provided", 1, 25, day));
		}
	}
	int year;
	int day;
}

bool run_day(Day day)
{
    writefln("%d Day %d", day.year, day.day);
    bool res = false;
    switch (day.year)
    {
    case 2021:
        res = run_day_2021(day.day);
        break;
	case 2022:
		res = run_day_2022(day.day);
		break;
	case 2023:
		res = run_day_2023(day.day);
		break;
    default: break;
    }
    if (!res) {
        writeln("Not implemented yet.");
    }
    writeln();
    return res;
}