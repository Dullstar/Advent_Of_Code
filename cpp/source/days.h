#pragma once
#include <string>
#include <optional>
#include <chrono>
#include <functional>
#include <array>

constexpr int32_t MIN_YEAR = 2015;
constexpr int32_t MAX_YEAR = 2023;

void run_day(int32_t year, int32_t day, std::string_view input_dir);

// bool run_2023_day_17(const std::string& filename);