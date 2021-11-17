import time
import os


def main(input_filename: str):
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Couldn't find input file: {input_filename}")
    # Generated by generate_files.py on Wed Nov 17 2021

    start_time = time.time
    # Return value of -1 is used to signal that this isn't implemented.
    # Once it is, remove/replace that return (implicitly returning None is fine).
    return -1


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        filename = "../../inputs/2019/day24.txt"
        main(filename)

    run_main()
