#include <chrono>
#include <stdexcept>
#include <sstream>
#include <optional>
#include <fmt/format.h>
#include <iostream>
#include "days.h"

std::array<std::function<bool(std::string)>, 25> days_2023 = {
	nullptr, // 1
	nullptr, // 2
	nullptr, // 3
	nullptr, // 4
	nullptr, // 5
	nullptr, // 6
	nullptr, // 7
	nullptr, // 8
	nullptr, // 9
	nullptr, // 10
	nullptr, // 11
	nullptr, // 12
	nullptr, // 13
	nullptr, // 14
	nullptr, // 15
	nullptr, // 16
	nullptr, // 17
	nullptr, // 18
	nullptr, // 19
	nullptr, // 20
	nullptr, // 21
	nullptr, // 22
	nullptr, // 23
	nullptr, // 24
	nullptr, // 25
};

void run_day(int32_t year, int32_t day, std::string_view input_dir)
{
	std::string filename = fmt::format("{}/{}/day{:02d}.txt", input_dir, year, day);

	std::cout << fmt::format("\n{} Day {}\n", year, day);
	std::function<bool(std::string)> day_main;
	switch (year)
	{
	case 2023:
		day_main = days_2023.at(day - 1);
	}
	if (day_main) day_main(filename);
	else std::cout << "Not implemented yet.\n";
	return;
}
