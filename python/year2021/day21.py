import time
import os
import collections
import itertools


# ------ Part 1 ------ #
class Player:
    def __init__(self, start_position):
        self.position = start_position
        self.score = 0


class DeterministicDice:
    def __init__(self):
        self.current_value = 0
        self.rolls = 0

    def roll(self):
        self.current_value += 1
        self.current_value %= 100
        self.rolls += 1
        return self.current_value


def parse_input(filename: str) -> (list[Player], int, int):
    with open(filename) as file:
        players = []
        for line in file:
            players.append(Player(int(line.split(":")[1]) - 1))
    return players, players[0].position, players[1].position


def do_round_pt1(player: Player, dice: DeterministicDice) -> bool:
    rolls = (dice.roll(), dice.roll(), dice.roll())
    player.position += sum(rolls)
    player.position %= 10
    player.score += player.position + 1  # The board is numbered from 1-10, but I'm storing 0-9.
    return player.score >= 1000


def play_game_pt1(players: list[Player], dice: DeterministicDice):
    while True:
        for i, player in enumerate(players):
            if do_round_pt1(player, dice):
                return i


# ------ Part 2 ------ #
PlayerState = collections.namedtuple("PlayerState", ["p1_pos", "p1_score", "p2_pos", "p2_score", "current_player"])
Win = collections.namedtuple("Win", ["player"])  # mostly just to give a more specific name than "int"


def find_next_state(player_state: PlayerState):
    states: list[PlayerState or Win] = []

    for rolls in itertools.product(range(1, 4), repeat=3):
        pos = (player_state.p1_pos if player_state.current_player == 0 else player_state.p2_pos)
        pos += sum(rolls)
        pos %= 10
        score = (player_state.p1_score if player_state.current_player == 0 else player_state.p2_score) + 1 + pos
        if score >= 21:
            states.append(Win(player_state.current_player))
        elif player_state.current_player == 0:
            states.append(PlayerState(pos, score, player_state.p2_pos, player_state.p2_score, 1))
        elif player_state.current_player == 1:
            states.append(PlayerState(player_state.p1_pos, player_state.p1_score, pos, score, 0))
    return states


def play_game_pt2(p1_start, p2_start):
    states = dict()
    quantities = collections.Counter()
    quantities[PlayerState(p1_start, 0, p2_start, 0, 0)] = 1
    p1_wins = 0
    p2_wins = 0
    while sum(quantities.values()) > 0:
        next_quantities = collections.Counter()
        for start_state in quantities:
            # This check saves having to work out states that can't actually happen, which evidentally seems
            # to be a sizable number since it more than halves the run time to do it this way compared to
            # checking every state that seems even remotely maybe possible.
            if start_state not in states:
                states[start_state] = find_next_state(start_state)
            for state in states[start_state]:
                if type(state) == Win:
                    if state.player == 0:
                        p1_wins += quantities[start_state]
                    elif state.player == 1:
                        p2_wins += quantities[start_state]
                else:  # type(state) == PlayerState
                    next_quantities[state] += quantities[start_state]
        quantities = next_quantities
    return max(p1_wins, p2_wins), min(p1_wins, p2_wins), int(p1_wins < p2_wins), int(p1_wins > p2_wins)


def main(input_filename: str):
    start_time = time.time()
    players, p1_start, p2_start = parse_input(input_filename)

    part1_start = time.time()
    dice = DeterministicDice()
    loser = (play_game_pt1(players, dice) + 1) % 2  # only works because there's only two players.
    print(f"Part 1: Loser's score {players[loser].score} * number of rolls {dice.rolls} = ", end="")
    print(players[loser].score * dice.rolls)

    part2_start = time.time()
    winner_wins, loser_wins, winner_id, loser_id = play_game_pt2(p1_start, p2_start)
    print(f"Part 2: The winner, player {winner_id + 1}, wins in {winner_wins} universes")
    print(f"Extra: The loser, player {loser_id + 1}, wins in {loser_wins} universes")

    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day21.txt")
