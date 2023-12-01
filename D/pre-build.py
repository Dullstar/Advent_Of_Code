MIN_YEAR = 2015
MAX_YEAR = 2022

import os.path
import time

days = dict()

for year in range(MIN_YEAR, MAX_YEAR + 1):
    for day in range(1, 26):
        if os.path.exists(path := f"source/year{year:04}/day{day:02}.d"):
            # print(f"Found {path}")
            if year not in days:
                days[year] = []
            days[year].append(day)

for year, ds in days.items():
    with open(f"source/year{year:04}/list{year:04}.d", "w") as file:
        # file.write(f"// Generated by pre-build.py on {time.strftime('%a %b %d %Y')}\n")
        # The timestamps have been removed so these don't spam git when there's no meaningful changes.
        file.write(f"// Generated by pre-build.py. Do not manually edit.\n")
        file.write(f"module year{year:04}.list{year:04};\n\n")
        file.write(f"immutable days{year:04} = {ds};")
