#include <optional>
#include <chrono>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <queue>
#include <fmt/format.h>
#include <dstr/string.h>
#include "../days.h"

struct Point
{
	int32_t x;
	int32_t y;
};
class Map 
{
public:
	Map(std::vector<int32_t> layout_, size_t sizeX, size_t sizeY)
		: layout(layout_), size_x(sizeX), size_y(sizeY), start{ 0, 0 }, 
		end{ static_cast<int32_t>(sizeX) - 1, static_cast<int32_t>(sizeY) - 1 } {}

	int32_t find_path()
	{
		std::vector<int32_t> board(layout.size(), -1);
		board[get_index(end)] = 0;
		auto queue = std::queue<Point>();
		queue.emplace(end);
		constexpr Point neighbors[] = { {0, 1}, {0, -1}, {-1, 0}, {1, 0} };
		while (!queue.empty()) {
			auto& current = queue.front();
			auto current_index = get_index(current);
			for (const auto& neighbor_relative : neighbors) {
				Point neighbor{ neighbor_relative.x + current.x, neighbor_relative.y + current.y };
				if (!out_of_bounds(neighbor)) {
					auto neighbor_index = get_index(neighbor);
					auto new_value = board[current_index] + layout[current_index];
					if (board[neighbor_index] == -1 || board[neighbor_index] > new_value) {
						board[neighbor_index] = new_value;
						queue.emplace(neighbor);
					}
				}
			}
			queue.pop();
		}
		return board[0];
	}

	void grow(size_t grow_x, size_t grow_y) {
		auto new_size_x = size_x * grow_x;
		auto new_size_y = size_y * grow_y;
		std::vector<int32_t> new_layout(new_size_x * new_size_y, 0);
		for (size_t y = 0; y < new_size_y; ++y) {
			for (size_t x = 0; x < new_size_x; ++x) {
				auto check_x = x % size_x;
				auto check_y = y % size_y;
				int32_t add_x = static_cast<int32_t>(x / size_x);
				int32_t add_y = static_cast<int32_t>(y / size_y);
				new_layout[y * new_size_x + x] = (layout[get_index(check_x, check_y)] - 1 + add_x + add_y) % 9 + 1;
			}
		}
		std::swap(layout, new_layout);
		size_x = new_size_x;
		size_y = new_size_y;
		end.x = size_x - 1;
		end.y = size_y - 1;
	}
private:
	size_t get_index(Point point)
	{
		return get_index(point.x, point.y);
	}
	size_t get_index(int32_t x, int32_t y)
	{
		return static_cast<size_t>(y) * size_x + static_cast<size_t>(x);
	}
	std::vector<int32_t> layout;
	size_t size_x;
	size_t size_y;
	Point start;  // might be unused...
	Point end;
	bool out_of_bounds(Point point)
	{
		return out_of_bounds(point.x, point.y);
	}
	bool out_of_bounds(int32_t x, int32_t y) 
	{
		return (x < 0) || (y < 0) || (x >= size_x) || (y >= size_y);
	}
};

Map parse_input(const std::string& filename)
{
	auto file = std::ifstream(filename);
	std::stringstream contents;
	contents << file.rdbuf();
	std::vector<int32_t> layout;
	for (const auto c : contents.str()) {
		if (c == '\n') continue;
		const char num[]{ c, '\0' };
		layout.emplace_back(std::stoi(num));
	}
	auto raw_contents = dstr::split(dstr::strip(contents.str()), "\n");
	size_t size_x = raw_contents[0].size();
	size_t size_y = raw_contents.size();
	return Map(layout, size_x, size_y);
}

std::optional<std::chrono::duration<float>> run_2021_day_15(const std::string& filename)
{
	auto start_time = std::chrono::system_clock::now();
	auto map = parse_input(filename);
	auto part1_start = std::chrono::system_clock::now();
	std::cout << fmt::format("Part 1: {}\n", map.find_path());
	auto part2_start = std::chrono::system_clock::now();
	map.grow(5, 5);
	std::cout << fmt::format("Part 2: {}\n", map.find_path());
	auto end_time = std::chrono::system_clock::now();

	typedef std::chrono::duration<float> time;
	std::cout << "Elapsed Time:\n";
	std::cout << fmt::format("Parsing: {:.03} ms\n", time(part1_start - start_time).count() * 1000);
	std::cout << fmt::format("Part 1: {:.03} ms\n", time(part2_start - part1_start).count() * 1000);
	std::cout << fmt::format("Part 2: {:.03} ms\n", time(end_time - part2_start).count() * 1000);
	time elapsed_time = (end_time - start_time);
	std::cout << fmt::format("Total: {:.03} ms\n", elapsed_time.count() * 1000);
	return std::make_optional(elapsed_time);

	return elapsed_time;
}