#include <vector>
#include <cstring>
#include <fstream>
#include <filesystem>
#include <iostream>
#include <fmt/format.h>

constexpr int32_t MIN_YEAR = 2015;
constexpr int32_t MAX_YEAR = 2021;

struct DayToRun
{
	int32_t year;
	int32_t day;
};

void generate_all_days_for_year(int32_t year, std::vector<DayToRun>& to_run)
{
	for (int32_t day = 1; day <= 25; ++day) {
		to_run.emplace_back(DayToRun{ year, day });
	}
}

void generate_all_days(std::vector<DayToRun>& to_run) {
	for (int32_t year = MIN_YEAR; year <= MAX_YEAR; ++year) {
		generate_all_days_for_year(year, to_run);
	}
}

struct Options
{
	std::vector<DayToRun> to_run;
	bool make_report = false;
};

void print_help()
{
	std::string filename = "args.txt";
	auto file = std::ifstream(filename);
	if (!file.is_open()) {
		std::cout << fmt::format("Couldn't open file: {}\n", filename);
		std::cout << "Is the working directory correct?\n";
		std::cout << fmt::format("\tWorking directory: {}\n", std::filesystem::current_path().u8string());
	}
	std::cout << file.rdbuf() << "\n";
	exit(EXIT_SUCCESS);
}

Options interpret_args(int argc, char** argv)
{
	int32_t year = -1;
	Options options;
	for (int i = 1; i < argc; ++i) {

	}

	return options;
}

void find_cpp_base_dir(char* executable_arg)
{
	std::cout << "Hello\n";
	if (!std::filesystem::exists("../inputs")) {
		auto executable_path = std::filesystem::canonical(std::filesystem::absolute(executable_arg));
		std::cout << executable_path << "\n";
		std::cout << executable_path.parent_path().parent_path() << "\n";
		std::filesystem::current_path(executable_path.parent_path().parent_path());
		if (!std::filesystem::exists("../inputs")) {
			std::cerr << "Couldn't find input directory. Expected to find it at: "
				<< executable_path.parent_path().parent_path().parent_path().append("inputs") << "\n";
		}
	}
}

int main(int argc, char** argv)
{
	if (argc == 1) {
		std::cout << "Error: missing required command line arguments.\n"
			<< "\tRun with --help for arguments.\n";
		return EXIT_SUCCESS;
	}
	std::cout << argv[0] << "\n";
	find_cpp_base_dir(argv[0]);
	print_help();
}
