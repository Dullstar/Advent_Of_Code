import time
import os
import re


# To avoid confusion with, you know, actual files -- just in case.
class TotallyNotFile:
    def __init__(self, size: int):
        self.size = size


class Directory:
    def __init__(self, name: str, parent=None):
        self.contents: dict[str: TotallyNotFile or Directory] = dict()
        self.name = name
        self.parent = parent
        self._size = None

    def get_size(self):
        if self._size is not None:
            return self._size
        current_total = 0
        for item in self.contents.values():
            if type(item) == TotallyNotFile:
                current_total += item.size
            elif type(item) == Directory:
                current_total += item.get_size()
        self._size = current_total
        return current_total

    def get_sum_contents_at_most_size(self, cutoff):
        current_total = 0
        for item in self.contents.values():
            if type(item) == Directory:
                size = item.get_size()
                current_total += size if size <= cutoff else 0
                current_total += item.get_sum_contents_at_most_size(cutoff)
        return current_total

    def get_all_directory_internal_sizes(self):
        sizes = set()
        for item in self.contents.values():
            if type(item) == Directory:
                sizes.add(item.get_size())
                sizes.update(item.get_all_directory_internal_sizes())
        return sizes

    def find_deletable_directory_size(self):
        sizes = self.get_all_directory_internal_sizes()
        disk_space = 70_000_000
        required = 30_000_000
        available = disk_space - self.get_size()
        return min(filter(lambda n: n + available > required, sizes))


def parse_input(filename: str):
    directory: Directory or None = None
    re_cd = re.compile(r"\$ cd (.+)")
    # We ignore entries for ls and dir, as we don't need them: there's nothing to confuse ls's output with that would
    # necessitate checking for it, and the input cds into every directory in order to run ls, so we just ignore the
    # dirs until they get cd'd into.
    re_file = re.compile(r"(\d+) (.+)")
    with open(filename, "r") as file:
        for line in file:
            if match := re_cd.match(line):
                dir_name = match[1]
                if directory is not None:
                    if dir_name == "..":
                        assert directory.parent is not None
                        directory = directory.parent
                    else:  # dir_name...
                        directory.contents[dir_name] = Directory(dir_name, directory)
                        directory = directory.contents[dir_name]
                else:  # directory is not None
                    directory = Directory(dir_name)
            elif match := re_file.match(line):
                f_size, f_name = int(match[1]), match[2]
                assert directory is not None
                directory.contents[f_name] = TotallyNotFile(f_size)
    # Return to outermost directory
    while directory.parent is not None:
        directory = directory.parent
    return directory


def main(input_filename: str):
    start_time = time.time()
    directory_tree = parse_input(input_filename)

    part1_start = time.time()
    pt1 = directory_tree.get_sum_contents_at_most_size(100_000)
    print(f"Part 1: Sum of sizes of directories with total size at most 100,000: {pt1}")

    part2_start = time.time()
    pt2 = directory_tree.find_deletable_directory_size()
    print(f"Part 2: Size of smallest directory that would free enough space: {pt2}")

    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")
    return


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day07.txt")


    run_main()


'''
Decluttering segment:  I've moved some debug functions down here that I wanted to keep around but I didn't want
them cluttering up the main solution with extra stuff that the reader likely doesn't care about and the solution
doesn't actually use. Really, it's mostly for just having some code lying around that prints out the tree to refer
to at a later time.

All removed methods depend on TotallyNotFile having a field called "name". In order to add it back, the only change
needed is to allow the constructor to accept it and then pass it f_name from parse_input, which is NOT removed because
it's used as a dictionary key (though realistically not required for files since we only ever retrieve them specifically
through iteration, but then we'd have to come up with SOMETHING for them, or store them elsewhere, or something.

Removed from class Directory:
    def __repr__(self):
        return self.debug_print(0)

    def debug_print(self, depth):
        output = f"{'    ' * depth}Dir {self.name} -> {self.get_size()}\n"
        for item in self.contents.values():
            if type(item) == TotallyNotFile:
                output += f"{'    ' * (depth + 1)}{item}\n"
            elif type(item) == Directory:
                output += f"{item.debug_print(depth + 1)}"
        return output
        
Removed from class TotallyNotFile:
    def __repr__(self):
        return f"File {self.name} -> Size: {self.size}"
'''