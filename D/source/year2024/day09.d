module year2024.day09;

import std.stdio;
import std.stdint;
import std.conv;
import std.string;
import std.algorithm;
import std.container;
import std.array;
import core.time;

import input;

// don't want conflicts with the actual File stuff.
struct DataFile
{
    int id;
    int size;
}

DataFile[] parse_input()
{
    bool is_file = true;
    int id = 0;
    DataFile[] files;
    foreach (c; get_input(2024, 9).strip)
    {
        if (c != '0') 
        {
            if (is_file)
            {
                files ~= DataFile(id++, (c ^ 0x30).to!int);
            }
            else
            {
                files ~= DataFile(-1, (c ^ 0x30).to!int);
            }
        }
        is_file = !is_file;
    }
    return files;
}

struct Disk
{
    int[] data;
    size_t[] free;
}

Disk files_list_to_disk(DataFile[] files)
{
    Disk disk;
    disk.data.reserve(files.map!(a => a.size).sum);
    disk.free.reserve(files.filter!(a => a.id < 0).map!(a => a.size).sum);
    size_t i = 0;
    foreach (file; files)
    {
        for (size_t block = 0; block < file.size; ++block, ++i)
        {
            disk.data ~= file.id;
            if (file.id < 0) disk.free ~= i;
        }
    }
    return disk;
}

void compact_disk(ref Disk disk)
{
    int j = 0;
    for (int i = disk.data.length.to!int - 1; j < disk.free.length && i > disk.free[j]; --i)
    {
        if (disk.data[i] < 0) continue;
        disk.data[disk.free[j++]] = disk.data[i];
        disk.data[i] = -1;
    }
}

uint64_t get_checksum(int[] data)
{
    uint64_t checksum = 0;
    foreach (i, block; data)
    {
        if (block >= 0)
        {
            checksum += i.to!uint64_t * block;
        }
    }
    return checksum;
}

uint64_t part_1(DataFile[] files)
{
    // writeln(files.to_string);
    Disk disk = files.files_list_to_disk;
    disk.compact_disk;
    return disk.data.get_checksum;
}

struct DataFilePt2
{
    int id;
    int size;
    size_t pos;
}

struct DiskPt2
{
    DataFilePt2[] files;
    size_t[][9] free;
}

DiskPt2 files_list_to_disk_pt2(DataFile[] files)
{
    DiskPt2 disk;
    size_t i = 0;
    foreach (file; files)
    {
        assert(file.size <= 9);
        if (file.id < 0)
        {
            // Since i increases, these will happen to be sorted, which is what we want.
            disk.free[file.size - 1] ~= i;
        }
        else
        {
            disk.files ~= DataFilePt2(file.id, file.size, i);
        }
        i += file.size;
    }
    disk.files.sort!("a.id > b.id");
    return disk;
}


int[] compact_disk_pt2(DiskPt2 disk, size_t disk_size)
{
    int[] data;
    data.length = disk_size;
    data[] = -1;
    DataFilePt2[] files_2;
    for (size_t i = 0; i < disk.files.length; ++i)
    {
        auto file = disk.files[i];
        auto best_pos_candidate = file.pos;
        size_t best_pos_candidate_i;
        for (size_t free_size = file.size - 1; free_size < disk.free.length; ++free_size)
        {
            if (disk.free[free_size].length > 0)
            {
                auto pos_candidate = disk.free[free_size][0];
                if (pos_candidate < best_pos_candidate) 
                {
                    best_pos_candidate = pos_candidate;
                    best_pos_candidate_i = free_size;
                }
            }
        }
        files_2 ~= DataFilePt2(file.id, file.size, best_pos_candidate);
        if (best_pos_candidate < file.pos)
        {
            disk.free[best_pos_candidate_i] = disk.free[best_pos_candidate_i][1..$];
            auto best_pos_candidate_size = best_pos_candidate_i + 1;
            assert(best_pos_candidate_size >= file.size);
            auto free_size = best_pos_candidate_size - file.size;
            if (free_size > 0)
            {
                disk.free[free_size - 1] ~= best_pos_candidate + file.size;
                disk.free[free_size - 1].sort;
            }
        }
    }
    files_2.sort!("a.pos < b.pos");
    size_t i = 0;
    foreach(file; files_2)
    {
        i = file.pos;
        for (size_t block = 0; block < file.size; ++block)
        {
            data[i++] = file.id;
        }
    }
    return data;
}

uint64_t part_2(DataFile[] files)
{
    size_t disk_size = files.map!(a => a.size).sum;
    auto disk = files.files_list_to_disk_pt2;
    auto data = compact_disk_pt2(disk, disk_size);
    return data.get_checksum;
}

bool run_2024_day09()
{
    auto start_time = MonoTime.currTime;
    auto input = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(input);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(input);
    auto end_time = MonoTime.currTime;
    writefln("Checksum (part 1): %s", pt1_solution);
    writefln("Checksum (part 2): %s", pt2_solution);
    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);
    return true;
}
