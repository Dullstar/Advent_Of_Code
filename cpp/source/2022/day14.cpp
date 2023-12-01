#pragma once  // wtf why does this silence the linker error, this isn't an include file!
#include <optional>
#include <string>
#include <iostream>
#include <fmt/format.h>
#include <vector>
#include "../days.h"
#include <dstr/string.h>
#include <sstream>
#include <fstream>
#include <unordered_set>
#include <limits>
#include <tuple>

struct Point 
{
	int x;
	int y;
	Point(int _x, int _y) : x(_x), y(_y) {}
	Point operator+(const Point& other) const { return Point(x + other.x, y + other.y); }
	bool operator==(const Point& other) const { return x == other.x && y == other.y; }
};

template <> struct fmt::formatter<Point> {
	constexpr auto parse(format_parse_context& ctx) -> decltype(ctx.begin()) {
		return ctx.end(); // just ignore anything in there...
	}
	template <typename FormatContext>
	auto format(const Point& pt, FormatContext& ctx) const -> decltype(ctx.out()) {
		return fmt::format_to(ctx.out(), "Point({},{})", pt.x, pt.y);
	};
};

template<>
struct std::hash<Point>
{
	std::size_t operator()(const Point& pt) const noexcept
	{
		// return (pt.y << 16 | pt.x);
		return pt.x * pt.y;
	}
};

enum class Tile
{
	Empty, Tile, Sand
};

class Layout
{
public:
	Layout(Point _size, std::vector<Tile>& _layout)
		: size(_size), layout(std::move(_layout))
	{
		layout.resize(size.x * size.y, Tile::Empty);
	}

	bool drop_sand(const Point& spawner) 
	{
		Point sand = spawner;
		auto try_move = [&](const Point& sand_pos) {
			for (const auto& dir : sand_movement_priorities) {
				auto new_sand = sand_pos + dir;
				if (new_sand.x < 0 || new_sand.x >= size.x || new_sand.y < 0 || new_sand.y >= size.y) {
					return std::optional<drop_result>();
				}
				// wait, does it REALLY want that?
				if (operator[](new_sand) == Tile::Empty) {
					return std::make_optional<drop_result>(true, new_sand);
				}
			}
			return std::make_optional<drop_result>(false, sand_pos);
		};
		while (true) {
			// std::cout << "Are we stuck here?";
			const auto sand_drop_res = try_move(sand);
			if (sand_drop_res.has_value()) {
				if (!sand_drop_res.value().moved) { 
					operator[](sand_drop_res.value().sand_location) = Tile::Sand;
					if (sand_drop_res.value().sand_location == spawner) {
						return false;
					}
					return true;
				}
				sand = sand_drop_res.value().sand_location;
			}
			else {
				return false;
			}
		}
	}

	void print() 
	{
		int x = 0;
		std::stringstream buffer;
		buffer << fmt::format("Layout {}x{}\n", size.x, size.y);
		for (const auto& tile : layout) {
			switch (tile) {
			case Tile::Empty:
				buffer << ".";
				break;
			case Tile::Tile:
				buffer << "#";
				break;
			case Tile::Sand:
				buffer << "o";
				break;
			}
			x += 1;
			if (x == size.x) {
				buffer << "\n";
				x = 0;
			}
		}
		// std::cout << buffer.str();
		auto out = std::ofstream("output.txt");
		out << buffer.str();
	}

	int fill(const Point& spawner) {
		int pieces = 0;
		while (drop_sand(spawner)) {
			pieces += 1;
		}
		return pieces;
	}
	const Tile& operator[](const Point& pt) const { return layout[pt.y * size.x + pt.x]; }
	Tile& operator[](const Point& pt) { return layout[pt.y * size.x + pt.x]; }
private:
	Point size;
	std::vector<Tile> layout;
	const Point sand_movement_priorities[3] = { Point(0, 1), Point(-1, 1), Point(1, 1) };
	struct drop_result 
	{
		bool moved;
		Point sand_location;
		drop_result(bool _moved, const Point& _sand_location)
			: moved(_moved), sand_location(_sand_location) {}
	};
};

class InfiniteLayout
{
public:
	InfiniteLayout(std::unordered_set<Point> _tiles, int max_y)
		: tiles(std::move(_tiles)), infinite_floor_y(max_y + 1) {}

	bool drop_sand(const Point& spawner)
	{
		Point sand = spawner;
		auto try_move = [&](const Point& sand_pos) {
			for (const auto& dir : sand_movement_priorities) {
				auto new_sand = sand_pos + dir;
				// wait, does it REALLY want that?
				if (operator[](new_sand) == Tile::Empty) {
					return drop_result(true, new_sand);
				}
			}
			return drop_result(false, sand_pos);
		};
		while (true) {
			const auto sand_drop_res = try_move(sand);
			if (!sand_drop_res.moved) {
				tiles.emplace(Point(sand_drop_res.sand_location));
				if (sand_drop_res.sand_location == spawner) return false;
				return true;
			}
			sand = sand_drop_res.sand_location;
		}
	}

	 void print()
	 {
		 std::stringstream buffer;
		int max_x = 0;
		int min_x = std::numeric_limits<int>::max();
		for (const auto& tile : tiles) {
			if (tile.x > max_x) max_x = tile.x;
			if (tile.x < min_x) min_x = tile.x;
		}
		for (int y = 0; y <= infinite_floor_y; ++y) {
			for (int x = min_x; x <= max_x; ++x) {
				switch (operator[](Point(x, y))) {
				case Tile::Empty:
					buffer << ".";
					break;
				case Tile::Tile:
					buffer << "#";
					break;
				case Tile::Sand:
					buffer << "o";
					break;
				}
			}
			buffer << "\n";
		}
		// std::cout << buffer.str();
		auto out = std::ofstream("output.txt");
		out << buffer.str();
	 }

	int fill(const Point& spawner) {
		int pieces = 0;
		do {
			pieces += 1;
			if (pieces > 25555) {
				print();
				throw (std::runtime_error("Bad"));
			}
		} while (drop_sand(spawner));
		return pieces;
	}
	Tile operator[](Point pt) const 
	{ 
		if (pt.y == infinite_floor_y) return Tile::Tile;
		if (auto search = tiles.find(pt); search != tiles.end()) {
			return Tile::Tile;  // i.e. the tile
		}
		return Tile::Empty;
	}
private:
	std::unordered_set<Point> tiles;
	int infinite_floor_y;
	const Point sand_movement_priorities[3] = { Point(0, 1), Point(-1, 1), Point(1, 1) };
	struct drop_result
	{
		bool moved;
		Point sand_location;
		drop_result(bool _moved, const Point& _sand_location)
			: moved(_moved), sand_location(_sand_location) {}
	};
};



auto parse_input(const std::string& filename)
{
	int max_x = 0;
	int max_y = 0;
	int min_x = std::numeric_limits<int>::max();
	auto tiles = std::unordered_set<Point>();
	auto fill_tiles = [&](const Point& first, const Point& second) {
		if (first.x == second.x) {
			for (int y = std::min(first.y, second.y); y <= std::max(first.y, second.y); ++y) {
				tiles.emplace(Point(first.x, y));
			}
		}
		else if (first.y == second.y) {
			for (int x = std::min(first.x, second.x); x <= std::max(first.x, second.x); ++x) {
				tiles.emplace(Point(x, first.y));
			}
		}
	};
	auto file = std::ifstream(filename);
	std::stringstream contents;
	contents << file.rdbuf();
	auto lines = dstr::split(dstr::strip(contents.str()), "\n");
	for (const auto& line : lines) {
		auto last_point = std::optional<Point>();
		auto pairs = dstr::split(line, " -> ");
		for (const auto& pair : pairs) {
			auto nums = dstr::split(pair, ",");
			auto point = Point(std::stoi(nums.at(0)), std::stoi(nums.at(1)));
			if (point.x < min_x) min_x = point.x;
			if (point.x > max_x) max_x = point.x;
			if (point.y > max_y) max_y = point.y;
			if (last_point.has_value()) {
				fill_tiles(last_point.value(), point);
			}
			last_point = point;
		}
	}
	max_x += 1;
	max_y += 1;  // accounts for some off-by-one issues
	auto size_x = max_x - min_x;
	auto layout = Layout(Point(size_x, max_y), std::vector<Tile>());
	auto layout2 = Layout(Point(1000, max_y + 2), std::vector<Tile>());
	for (const auto& tile : tiles) {
		layout[tile + Point(-min_x, 0)] = Tile::Tile;
		if (tile.x < 0 || tile.x >= 1000) throw std::runtime_error("Bad.");
		layout2[tile] = Tile::Tile;
	}
	for (int x = 0; x < 1000; ++x) {
		layout2[Point(x, max_y + 1)] = Tile::Tile;
	}
	auto spawner = Point(500 - min_x, 0);
	auto inf_spawner = Point(500, 0);
	auto inf_layout = InfiniteLayout(tiles, max_y);
	return std::tuple(layout, spawner, inf_spawner, inf_layout);
}

// This should be called run_2022_day_14 but the linker didn't like it. Must investigate;
// it FEELS like a linker bug but realistically it's very unlikely I found one:
// it caused the linker to get confused somehow with run_2015_day_14.
// Could I possibly have a misconception about what names are allowed/considered unique?
std::optional<std::chrono::duration<float>> broken_name(const std::string& filename)
{
	auto start_time = std::chrono::system_clock::now();
	auto input_tuple = parse_input(filename);
	auto& [cave, spawner, inf_spawner, inf_cave] = input_tuple;
	auto part1_start = std::chrono::system_clock::now();
	// cave.print();
	auto p1 = cave.fill(spawner);
	std::cout << fmt::format("Part 1: {} sand units dispensed\n", p1);
	auto part2_start = std::chrono::system_clock::now();
	inf_cave.print();
	auto p2 = inf_cave.fill(inf_spawner) + 1;
	auto end_time = std::chrono::system_clock::now();
	std::cout << fmt::format("Part 2: {} sand units dispensed\n", p2);

	typedef std::chrono::duration<float> time;
	std::cout << "Elapsed Time:\n";
	std::cout << fmt::format("Parsing: {:.03f} ms\n", time(part1_start - start_time).count() * 1000);
	std::cout << fmt::format("Part 1: {:.03f} ms\n", time(part2_start - part1_start).count() * 1000);
	std::cout << fmt::format("Part 2: {:.03f} ms\n", time(end_time - part2_start).count() * 1000);
	time elapsed_time = (end_time - start_time);
	std::cout << fmt::format("Total: {:.03f} ms\n", elapsed_time.count() * 1000);
	return std::make_optional(elapsed_time);
}