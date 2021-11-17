import os


def get_filename(year: int, day: int):
    filename = f"../inputs/{year}/day{day:02d}.txt"
    if os.path.exists("../inputs"):
        return filename
    elif os.path.exists("../../inputs"):
        return f"../{filename}"
    raise FileNotFoundError("Couldn't find inputs folder.")