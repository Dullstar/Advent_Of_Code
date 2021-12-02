import time
import os


# An older version of this script printed a lot of information. But this does create a *lot* of output that's not
# actually what we care about, and this would (probably) have a non-negligible amount of overhead for this problem
# (okay, so I didn't actually check). Still, now that running multiple days is a possibility overall, I don't want
# to clutter up the output with too much extraneous output.
# But I've left them commented out instead of removing them entirely, in case anyone is interested in restoring them...
# especially as it's not entirely out of the question that I may eventually chose to add some sort of --verbose mode


class Entry:
    def __init__(self, entry: dict):
        self.entry: dict = entry
        self.pt1_valid: bool or None = None  # we store this so we can skip invalid pt1 entries during pt2


def parse_input(filename: str):
    with open(filename, "r") as file:
        lines = file.read()
        entries = []
        # Split 1: Separates different entries
        lines = lines.strip().split("\n\n")
        for line in lines:
            # Split 2: Separates different fields within a single entry
            line = line.split()
            dictionary = {}
            for item in line:
                # Split 3: Separates fields from their values
                item = item.split(":")
                dictionary[item[0]] = item[1]
            entries.append(Entry(dictionary))
        return entries


def validate_entry_count(entry: Entry):
    required_keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    # print("Checking entry: ", entry)
    for key in required_keys:
        if key not in entry.entry:
            # print("This entry is missing key: ", key)
            # print()
            entry.pt1_valid = False
            return False
    # print("No (important) missing keys detected.")
    entry.pt1_valid = True
    return True


def validate_entry_values(entry: Entry):
    # It's not possible for an entry to fail part 1 and pass part 2, so if it failed part 1 we can skip.
    if not entry.pt1_valid:
        return False

    required_keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    for key in required_keys:
        if key == "byr":
            byr = int(entry.entry[key])
            if byr < 1920 or byr > 2002:
                # print(f"Birth year of {byr} is not between 1920 and 2002")
                return False
        elif key == "iyr":
            iyr = int(entry.entry[key])
            if iyr < 2010 or iyr > 2020:
                # print(f"Issue year of {iyr} is not between 2010 and 2020")
                return False
        elif key == "eyr":
            eyr = int(entry.entry[key])
            if eyr < 2020 or eyr > 2030:
                # print(f"Expiration year of {eyr} is not between 2020 and 2030")
                return False
        elif key == "hgt":
            value = ""
            unit = ""
            stop_checking_numbers = False
            for i in range(len(entry.entry[key])):
                # Probably over-engineered considering the input file
                char = entry.entry[key][i]
                if not stop_checking_numbers and char.isnumeric():
                    value += char
                    continue
                elif not stop_checking_numbers:
                    stop_checking_numbers = True
                unit += char
            value = int(value)

            if unit == "in":
                if value < 59 or value > 76:
                    # print("The airline discriminates against people who are too tall or too short,")
                    # print(f"and a height of {value} inches is not between 59 and 76")
                    return False
            elif unit == "cm":
                if value < 150 or value > 193:
                    # print("The airline discriminates against people who are too tall or too short,")
                    # print(f"and a height of {value} cm is not between 150 and 193")
                    return False
            else:
                # print(f"Unit {unit} is not either in or cm")
                return False
        elif key == "hcl":
            hcl_valid = True
            if entry.entry[key][0] != "#" or len(entry.entry[key]) != 7:
                hcl_valid = False
            else:
                try:
                    # If this value cannot be converted to hex, i.e. does not consist of 0-9 and a-f,
                    # then this throws a ValueError, telling us this isn't valid
                    int(entry.entry[key][1:], 16)
                except ValueError:
                    hcl_valid = False
            if not hcl_valid:
                # print(f"Hair color {entry[key]} does not comply to expected format #nnnnnn where n is a hex number")
                return False
        elif key == "ecl":
            allowed_values = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
            if entry.entry[key] not in allowed_values:
                # print(f"Eye color {entry[key]} not in allowed list of colors: {allowed_values}")
                return False
        elif key == "pid":
            if len(entry.entry[key]) != 9:
                # print(f"The Passport ID {entry[key]} does not consist of 9 digits.")
                return False
            elif not entry.entry[key].isnumeric():
                # print(f"The Passport ID {entry[key]} is not a numeric value.")
                return False
    # If you've made it here, congratulations! It's a valid result.
    # print("All entries are valid.")
    return True


def main(input_filename: str):
    start_time = time.time()
    entries = parse_input(input_filename)
    total_entries = len(entries)

    part1_start = time.time()
    valid_entries = 0
    for entry in entries:
        valid_entries += validate_entry_count(entry)

    part2_start = time.time()
    valid_entries_2 = 0
    for entry in entries:
        valid_entries_2 += validate_entry_values(entry)

    end_time = time.time()
    print(f"Part 1: {valid_entries} out of {total_entries} are valid")
    print(f"Part 2: {valid_entries_2} out of {total_entries} are valid")

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2020/day04.txt")
