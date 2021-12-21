#include <iostream>
#include <sstream>
#include <fstream>
#include <array>
#include <unordered_map>
#include <numeric>
#include <fmt/format.h>
#include <dstr/string.h>
#include "../days.h"

// ----- PART 1 -----
struct Player
{
	int32_t position;
	int32_t score;
};

class DeterministicDice
{
public:
	DeterministicDice() : current_value(0), rolls(0) {}
	int32_t current_value;
	int32_t rolls;
	int32_t roll()
	{
		++current_value;
		current_value %= 100;
		++rolls;
		return current_value;
	}
};

std::array<Player, 2> parse_input(const std::string& filename)
{
	auto file = std::ifstream(filename);
	std::stringstream contents;
	contents << file.rdbuf();
	auto lines = dstr::split(dstr::strip(contents.str()), "\n");
	std::array<Player, 2> players{};
	for (size_t i = 0; i < lines.size(); ++i) {
		std::cout << fmt::format("Current line: {}\n", lines[i]);
		players[i] = { std::stoi(dstr::split(lines[i], ":")[1]) - 1, 0 };
	}
	return players;
}

bool do_round_pt1(Player& player, DeterministicDice& dice)
{
	for (int i = 0; i < 3; ++i) {
		auto roll = dice.roll();
		player.position += roll;
	}
	player.position %= 10;
	player.score += player.position + 1;
	return player.score >= 1000;
}

size_t play_game_pt1(std::array<Player, 2>& players, DeterministicDice& dice)
{
	while (true) {
		for (size_t i = 0; i < players.size(); ++i) {
			if (do_round_pt1(players[i], dice)) return i;
		}
	}
}

// ----- PART 2 -----
struct PlayerState
{
	int32_t p1_pos;
	int32_t p1_score;
	int32_t p2_pos;
	int32_t p2_score;
	int32_t current_player;

	bool operator==(const PlayerState& other) const noexcept {
		return p1_pos == other.p1_pos
			&& p1_score == other.p1_score
			&& p2_pos == other.p2_pos
			&& p2_score == other.p2_score
			&& current_player == other.current_player;
	}
};

template<>
struct std::hash<PlayerState>
{
	std::size_t operator()(const PlayerState& s) const noexcept
	{
		return static_cast<size_t>(s.p1_pos | (s.p1_score << 4) | (s.p2_pos << 9) | (s.p2_score << 13) | (s.current_player << 18));
	}
};

std::vector<PlayerState> find_next_state(const PlayerState& state) 
{
	std::vector<PlayerState> states;
	for (int32_t i = 1; i < 4; ++i) {
		for (int32_t j = 1; j < 4; ++j) {
			for (int32_t k = 1; k < 4; ++k) {
				int32_t pos = state.current_player == 0 ? state.p1_pos : state.p2_pos;
				pos += i + j + k;
				pos %= 10;
				int32_t score = (state.current_player == 0 ? state.p1_score : state.p2_score) + 1 + pos;
				if (state.current_player == 0) {
					states.emplace_back(PlayerState{ pos, score, state.p2_pos, state.p2_score, 1 });
				}
				else { // (state.current_player == 1)
					states.emplace_back(PlayerState{ state.p1_pos, state.p1_score, pos, score, 0 });
				}
			}
		}
	}
	return states;
}

bool is_empty(const std::unordered_map<PlayerState, int64_t>& umap)
{
	for (const auto& entry : umap) {
		if (entry.second > 0) return false;
	}
	return true;
}

void play_game_pt2(int32_t p1_start, int32_t p2_start)
{
	constexpr int32_t WIN = 21;
	std::unordered_map<PlayerState, std::vector<PlayerState>> states;
	std::unordered_map<PlayerState, int64_t> quantities;
	quantities[PlayerState{ p1_start, 0, p2_start, 0, 0 }] = 1;
	int64_t p2_wins = 0;
	int64_t p1_wins = 0;
	while (!is_empty(quantities)) {
		std::unordered_map<PlayerState, int64_t> next_quantities;
		for (const auto& entry : quantities) {
			auto& start_state = entry.first;
			auto& quantity = entry.second;
			if (states.find(start_state) == states.end()) {
				states[start_state] = find_next_state(start_state);
			}
			for (const auto& state : states[start_state]) {
				if (state.p1_score >= WIN) p1_wins += quantities[start_state];
				else if (state.p2_score >= WIN) p2_wins += quantities[start_state];
				else next_quantities[state] += quantities[start_state];
			}
		}
		std::swap(quantities, next_quantities);
	}
	auto win_score = std::max(p1_wins, p2_wins);
	auto lose_score = std::min(p1_wins, p2_wins);
	int winner = p1_wins < p2_wins;
	int loser = p1_wins > p2_wins;
	std::cout << fmt::format("Part 2: The winner, player {}, wins in {} universes\n", winner, win_score);
	std::cout << fmt::format("Extra: The loser, player {}, wins in {} universes\n", loser, lose_score);
}

std::optional<std::chrono::duration<float>> run_2021_day_21(const std::string& filename)
{
	auto start_time = std::chrono::system_clock::now();
	auto players = parse_input(filename);
	auto p1_start = players[0].position;
	auto p2_start = players[1].position;

	auto part1_start = std::chrono::system_clock::now();
	auto dice = DeterministicDice();
	auto loser = (play_game_pt1(players, dice) + 1) % 2;
	std::cout << fmt::format(
		"Part 1: Loser's score {} * number of rolls {} = {}\n",
		players[loser].score,
		dice.rolls,
		players[loser].score * dice.rolls
	);

	auto part2_start = std::chrono::system_clock::now();
	// Note: To simplify returns here, Part 2's functions will handle printing results.
	play_game_pt2(p1_start, p2_start);
	auto end_time = std::chrono::system_clock::now();

	typedef std::chrono::duration<float> time;
	std::cout << "Elapsed Time:\n";
	std::cout << fmt::format("    Parsing: {:.03} ms\n", time(part1_start - start_time).count() * 1000);
	std::cout << fmt::format("    Part 1: {:.03} ms\n", time(part2_start - part1_start).count() * 1000);
	std::cout << fmt::format("    Part 2: {:.03} ms\n", time(end_time - part2_start).count() * 1000);
	time elapsed_time = (end_time - start_time);
	std::cout << fmt::format("    Total: {:.03} ms\n", elapsed_time.count() * 1000);
	return std::make_optional(elapsed_time);
}