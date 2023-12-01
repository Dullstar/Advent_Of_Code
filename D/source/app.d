import std.stdio;
import std.format;
import std.getopt;
import std.conv;
import std.string;

import run_day;
import input;

struct Options
{
	bool report = false;
	bool use_test_input = false;
	Day[] days;
}

Options process_args(string[] args)
{
	// getopts wants this to be present even though we don't care what's in it.
	// I don't think it actually matters what's in there, but I don't now if it'll still process it,
	// and even so there's no required arguments so it could very well be empty otherwise.
	string[] option_args = [args[0]];

	string[] num_args;
	foreach (arg ; args[1..$])
	{
		if (arg.length >= 2 && arg[0..2] == "--") option_args ~= arg;
		else num_args ~= arg;
	}

	Options opts;
	getopt(
		option_args,
		"report", &opts.report,
		"test", &opts.use_test_input
	);
	bool year_provided = false;
	int year;
	foreach (arg ; num_args)
	{
		try 
		{
			int conv_arg = arg.to!int;
			if (conv_arg <= 25 && conv_arg >= 1)
			{
				if (!year_provided) throw new Exception(format("Day %d was specified, but no year.", conv_arg));
				opts.days ~= Day(year, conv_arg);
			}
			else
			{
				year_provided = true;
				year = conv_arg;
			}
		}
		catch (ConvException e)
		{
			throw new Exception(format("Unexpected argument: %s", arg));
		}
	}
	if (opts.days.length == 0) 
	{
		if (!year_provided)
		{
			write("Enter the year to run: ");
			year = readln.strip.to!int;
		}
		writef("Enter the day to run (year %d): ", year);
		int day = readln.strip.to!int;
		opts.days ~= Day(year, day);
	}
	return opts;
}

void main(string[] args)
{
	try 
	{
		auto opts = process_args(args);
		input.init_path(opts.use_test_input);
		foreach (day; opts.days) 
		{
			run_day.run_day(day);
		}
	}
	catch (Exception e)
	{
		writefln("Error: %s", e.msg);
		throw(e);
	}
	// It doesn't seem to obey the setting to not immediately close the window when the program terminates
	// on Visual Studio, so we do this to force it to remain open so that the output can actually be read.
	// Should probably add some conditional compilation so this is skipped in Linux.
	// writeln("Press any key to exit...");
	// readln();
}
