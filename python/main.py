import sys
import os
import run_day

MIN_YEAR = 2015
MAX_YEAR = 2020


class DayToRun:
    def __init__(self, year, day):
        self.year = year
        self.day = day

    def __str__(self):
        return f"Year {self.year} Day {self.day}"


def generate_all_days_for_year(year: int) -> list[DayToRun]:
    return [DayToRun(year, i) for i in range(1, 26)]


def generate_all_days() -> list[DayToRun]:
    to_run = []
    for year in range(MIN_YEAR, MAX_YEAR + 1):
        to_run += generate_all_days_for_year(year)
    return to_run


def interpret_args() -> list[DayToRun]:
    current_year = None
    to_run = []

    # There might be a builtin somewhere to do this "cleaner" but this works.
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg == "all":
            if current_year:
                to_run += generate_all_days_for_year(current_year)
            else:
                to_run += generate_all_days()
        else:
            try:
                arg = int(arg)
                if current_year and arg in range(1, 26):
                    to_run.append(DayToRun(current_year, arg))
                elif arg in range(MIN_YEAR, MAX_YEAR + 1):
                    current_year = arg
                else:
                    raise Exception(f"Argument 'arg' out of range.")
            except ValueError:
                print(f"Can't interpret argument: {arg}", file=sys.stderr)
    return to_run


def create_unimplemented_report(unimplemented: list[DayToRun]) -> None:
    import time
    with open("report.txt", "w") as file:
        file.write(f"Generated {time.ctime()}\n\n")
        file.write("Unimplemented days:\n\n")

        day_dict = dict()
        for day in unimplemented:
            if day.year not in day_dict:
                day_dict[day.year] = [day.day]
            else:
                day_dict[day.year].append(day.day)

        for year in sorted(day_dict.keys()):
            file.write(f"{year}:\n    ")
            file.write(str(day_dict[year])[1:-1])
            file.write("\n")


def print_help() -> None:
    print("Advent of Code: Python Script Loader for Dullstar's Solutions\n")
    print("Usage: python main.py [year] [day(s)] [year] [day(s)] [etc.]\n")
    print("Example: python main.py 2020 8 11 2019 2")
    print("    would run days 8 and 11 from 2020, and day 2 from 2019")
    print(f"[year] must be between {MIN_YEAR} and {MAX_YEAR}, inclusive")
    print("[day] must be between 1 and 25, inclusive")
    print("You can also set day to 'all' to select all days from a year:")
    print("    e.g. \"python main.py 2020 all\" would run all days from 2020")
    print("Using 'all' before a year has been specified will run all days from all years.")
    print("    i.e. \"python main.py all\"")
    print("If 'all' was the only argument, the file \"report.txt\" will be generated")
    print("detailing which days are not implemented.")
    print("Otherwise, unimplemented days are reported on stdout as they are encountered.\n")
    print("Note: If you only want to run one day, you can run individual day scripts independently.")


def main() -> None:
    print(sys.argv)
    if len(sys.argv) == 1:
        print_help()
        exit()
    os.chdir(os.path.split(__file__)[0])
    # Consider if > 2 would make more sense than == 2 (would also require editing print_help())
    report = True if len(sys.argv) == 2 and sys.argv[1] == "all" else False
    unimplemented = []
    for day in interpret_args():
        # print(day)
        if run_day.run_day(day.year, day.day) == -1:
            if report:
                unimplemented.append(day)
                create_unimplemented_report(unimplemented)
            else:
                print(f"{day} not implemented yet.")


# Currently, this allows importing only because there's constants
# here that are useful to use in generate_files as well.
# If MIN_YEAR and MAX_YEAR are used in more places, it may be worth
# considering extracting those to another module and re-prohibiting
# importing this file.
if __name__ == "__main__":
    main()
