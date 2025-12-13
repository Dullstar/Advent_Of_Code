module run_day;

import std.format;
import std.stdio;
import std.file;

import year2021;
import year2022;
import year2023;
import year2024;
import year2025;

const int MAX_YEAR = 2025;
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
		if (year < 2025)
		{			
			if (day < 1 || day > 25) 
			{
				throw new Exception(format("2015-2024: Day must be between %d and %d; %d was provided", 1, 25, day));
			}
		}
		else
		{
			if (day < 1 || day > 12)
			{
				throw new Exception(format("2025-%d: Day must be between %d and %d; %d was provided", MAX_YEAR, 1, 12, day));
			}
		}
	}
	int year;
	int day;
}

bool run_day(Day day)
{
	try
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
		case 2024:
			res = run_day_2024(day.day);
			break;
		case 2025:
			res = run_day_2025(day.day);
			break;
		default: break;
		}
		if (!res) {
			writeln("Not implemented yet.");
		}
		writeln();
		return res;
	}
	catch (FileException e)
	{
		stderr.writeln(e.msg);
		return false;
	}
}