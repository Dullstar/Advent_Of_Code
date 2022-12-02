import time
import os


class Move:
    Rock = 1
    Paper = 2
    Scissors = 3

    Win = 6
    Loss = 0
    Draw = 3


class Round:
    def __init__(self, move1, move2, desired_result):
        self.p1_move = move1
        self.p2_move = move2
        if desired_result == Move.Draw:
            self.p2_move_pt2 = move1
        elif move1 == Move.Rock:
            self.p2_move_pt2 = Move.Paper if desired_result == Move.Win else Move.Scissors
        elif move1 == Move.Scissors:
            self.p2_move_pt2 = Move.Rock if desired_result == Move.Win else Move.Paper
        elif move1 == Move.Paper:
            self.p2_move_pt2 = Move.Scissors if desired_result == Move.Win else Move.Rock

    def get_round_score(self) -> (int, int):
        if self.p1_move == self.p2_move:
            return Move.Draw + self.p1_move, Move.Draw + self.p2_move

        winner = None
        # Ignore which player made the move in determining the winner to do less checks...
        moves = sorted([self.p1_move, self.p2_move])
        if moves[0] == Move.Rock and moves[1] == Move.Scissors:
            winner = 0
        elif moves[0] == Move.Rock and moves[1] == Move.Paper:
            winner = 1
        elif moves[0] == Move.Paper and moves[1] == Move.Scissors:
            winner = 1

        # Then correct for it if it's the opposite configuration
        if moves[0] != self.p1_move:
            moves.reverse()
            winner += 1
            winner %= 2

        return self.p1_move + (Move.Win if winner == 0 else Move.Loss), \
            self.p2_move + (Move.Win if winner == 1 else Move.Loss)


def parse_input(filename: str):
    # I know r is the default but for some reason I just always explicitly specify it.
    rounds = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip().split(" ")
            assert len(line) == 2, "Good input should have 2 things per line"
            STUFF = {"A": Move.Rock, "X": Move.Rock,
                     "B": Move.Paper, "Y": Move.Paper,
                     "C": Move.Scissors, "Z": Move.Scissors}
            STUFF2 = {"X": Move.Loss, "Y": Move.Draw, "Z": Move.Win}
            rounds.append(Round(STUFF[line[0]], STUFF[line[1]], STUFF2[line[1]]))

    return rounds


def main(input_filename: str):
    start_time = time.time()
    moves = parse_input(input_filename)

    part1_start = time.time()
    p1_score = 0
    p2_score = 0
    for move in moves:
        dp1, dp2 = move.get_round_score()
        p1_score += dp1
        p2_score += dp2

    part2_start = time.time()
    p1_score_pt2 = 0
    p2_score_pt2 = 0
    for move in moves:
        move.p2_move = move.p2_move_pt2
        dp1, dp2 = move.get_round_score()
        p1_score_pt2 += dp1
        p2_score_pt2 += dp2

    end_time = time.time()
    print(f"Part 1: You scored {p2_score} points!")
    print(f"    This {'beats' if p2_score > p1_score else 'does not beat'} the elf's {p1_score} points.")
    print(f"Part 2: You scored {p2_score_pt2} points!")
    print(f"    This {'beats' if p2_score_pt2 > p1_score_pt2 else 'does not beat'} the elf's {p1_score_pt2} points.")
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day02.txt")


    run_main()
