import os
import time
from main import MIN_YEAR, MAX_YEAR

FILE = os.path.basename(__file__)
HEADER = f"# Generated by {FILE} on {time.strftime('%a %b %d %Y')}\n\n"
# NO_IMPORT = 'if __name__ != "__main__":\n' \
#     '    raise ImportError(f"Module {__name__} cannot be imported.")\n' \
#     'else:\n' \
#     '    main()\n'
IMPORT_ONLY = 'if __name__ == "__main__":\n' \
    '    print("This module is intended to be imported.")\n'


def generate_run_day():
    with open("run_day.py", "w") as file:
        file.write(HEADER)
        file.write("def run_day(year: int, day: int):\n")
        file.write('    filename = f"../inputs/{year}/day{day:02d}.txt"\n')
        file.write('    # We could eliminate this if/elif branch with eval, but then we have to import\n')
        file.write('    # every day, even if we don\'t run them all. Since there\'s a lot of them,\n')
        file.write('    # we\'d still definitely want to generate the code to import them all.\n')
        for year in range(MIN_YEAR, MAX_YEAR + 1):
            file.write(f"    {'if' if year == MIN_YEAR else 'elif'} year == {year}:\n")
            for day in range(1, 26):
                file.write(f"{' ' * 8}{'if' if day == 1 else 'elif'} day == {day}:\n")
                file.write(f"{' ' * 12}import year{year}.day{day:02d}\n")
                file.write(f"{' ' * 12}return year{year}.day{day:02d}.main(filename)\n")
            file.write("\n")
        file.write(f"\n{IMPORT_ONLY}")


def generate_day(year: int, day: int):
    filename = f"year{year}/day{day:02d}.py"
    if not os.path.exists(f"year{year}"):
        os.mkdir(f"year{year}")
    if os.path.exists(filename):
        # This is just for generating templates,
        # so if the file already exists,
        # we don't want to touch it.
        return
    with open(filename, "w") as file:
        file.write("import time\n")
        file.write("import os\n\n\n")
        file.write("def main(input_filename: str):\n")
        file.write(f"    {HEADER}")
        file.write("    # Return value of -1 is used to signal that this isn't implemented.\n")
        file.write("    # Once it is, remove/replace that return (implicitly returning None is fine).\n")
        file.write("    return -1\n\n\n")
        file.write('if __name__ == "__main__":\n')
        # We make run_main a function specifically to ensure that filename is constrained to a local scope.
        file.write("    def run_main():\n")
        # Make sure that the working directory is as expected, even if the user called it from somewhere different,
        # to make sure we're looking for the inputs where they're supposed to be.
        file.write('        os.chdir(os.path.split(__file__)[0])\n')
        file.write(f'        main("../../inputs/{year}/day{day:02d}.txt")\n\n')
        file.write('    run_main()\n')


def main():
    generate_run_day()
    for year in range(MIN_YEAR, MAX_YEAR + 1):
        for day in range(1, 26):
            generate_day(year, day)


if __name__ != '__main__':
    raise ImportError(f"Module {__name__} cannot be imported.")
else:
    main()
