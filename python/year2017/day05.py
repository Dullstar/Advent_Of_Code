def main(input_filename: str):
    # if not os.path.exists(input_filename):    #     raise FileNotFoundError(f"Couldn't find file: {input_filename}")
    # Generated by generate_files.py on Sun Nov 14 2021

    # Return value of -1 is used to signal that this isn't implemented.
    # Once it is, remove/replace that return (implicitly returning None is fine).
    return -1


if __name__ == "__main__":
    import os
    filename = "../../inputs/2017/day05.txt"
    if not os.path.exists("../../inputs"):
        filename = filename[3:]
        if not os.path.exists("../inputs"):
            FileNotFoundError("Couldn't find inputs directory.")
