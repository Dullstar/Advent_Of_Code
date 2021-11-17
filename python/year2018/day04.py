def main(input_filename: str):
    # if not os.path.exists(input_filename):    #     raise FileNotFoundError(f"Couldn't find file: {input_filename}")
    # Generated by generate_files.py on Wed Nov 17 2021

    # Return value of -1 is used to signal that this isn't implemented.
    # Once it is, remove/replace that return (implicitly returning None is fine).
    return -1


if __name__ == "__main__":
    import os
    # Ensure working directory is as expected so we can find the input properly
    os.chdir(os.path.split(__file__)[0])
    filename = "../../inputs/2018/day04.txt"
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Couldn't find input file: {filename}")
    main(filename)
