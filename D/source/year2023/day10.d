module year2023.day10;

import std.stdio;
import std.string;
import std.algorithm;
import std.exception;
import std.conv;
import std.array;
import std.container;
import core.time;

import input;
import utility;

enum Tile 
{
    Verticle,
    Horizontal,
    N_to_E,
    N_to_W,
    S_to_W,
    S_to_E,
    Unknown,
    Empty,
}

enum NORTH = Point!int(0, -1);
enum SOUTH = Point!int(0, 1);
enum EAST = Point!int(1, 0);
enum WEST = Point!int(-1, 0);

Tile get_tile(char c)
{
    Tile[char] tile_dict = [
        '-': Tile.Horizontal,
        '|': Tile.Verticle,
        '.': Tile.Empty,
        'L': Tile.N_to_E,
        'J': Tile.N_to_W,
        '7': Tile.S_to_W,
        'F': Tile.S_to_E,
        'S': Tile.Unknown
    ];
    auto ptr = c in tile_dict;
    enforce(ptr !is null, format("Bad character in input: %s", c));
    return *ptr;
}

struct Layout
{
    Grid2D!Tile grid;
    Point!int start;

    // Get the locations of neighboring tiles.
    // A tile is only considered to be a neighbor if it is attached.
    Point!int[] get_neighbors(Point!int tile_coords)
    {
        if (!grid.in_bounds(tile_coords)) return [];
        Point!int[] neighbors;
        final switch(grid[tile_coords]) {
        case Tile.Verticle:
            neighbors = [NORTH, SOUTH];
            break;
        case Tile.Horizontal:
            neighbors = [EAST, WEST];
            break;
        case Tile.N_to_E:
            neighbors = [NORTH, EAST];
            break;
        case Tile.N_to_W:
            neighbors = [NORTH, WEST];
            break;
        case Tile.S_to_W:
            neighbors = [SOUTH, WEST];
            break;
        case Tile.S_to_E:
            neighbors = [SOUTH, EAST];
            break;
        case Tile.Empty:
        case Tile.Unknown:
            break;
        }
        return neighbors.map!(a => a + tile_coords).array;
    }

   void identify_start() 
    {
        bool attached(Point!int dir)
        {
            // Check if the Start point is one of this tile's neighbors.
            // A tile is only considered a neighbor if it's attached.
            auto n = get_neighbors(start + dir);
            foreach (attachment; n) {
                if (attachment == start) return true;
            }
            return false;
        }
        // We determine which attachments the starting point has...
        bool attached_N = attached(NORTH);
        bool attached_S = attached(SOUTH);
        bool attached_W = attached(WEST);
        bool attached_E = attached(EAST);
        assert(attached_N + attached_S + attached_W + attached_E == 2, "Expected exactly two attachments to start.");
        // ...then we rule out which ones don't work.
        Tile[] possible = [Tile.Horizontal, Tile.Verticle, Tile.N_to_E, Tile.N_to_W, Tile.S_to_W, Tile.S_to_E];
        if (!attached_N) {
            possible = possible.filter!(a => (a != Tile.Verticle) && (a != Tile.N_to_E) && (a != Tile.N_to_W)).array;
        }
        if (!attached_S) {
            possible = possible.filter!(a => (a != Tile.Verticle) && (a != Tile.S_to_E) && (a != Tile.S_to_W)).array;
        }
        if (!attached_W) {
            possible = possible.filter!(a => (a != Tile.Horizontal) && (a != Tile.N_to_W) && (a != Tile.S_to_W)).array;
        }
        if (!attached_E) {
            possible = possible.filter!(a => (a != Tile.Horizontal) && (a != Tile.N_to_E) && (a != Tile.S_to_E)).array;
        }
        // ...which should leave us with only one remaining possibility.
        assert(possible.length == 1);
        grid[start] = possible[0];
    }
}

Layout parse_input()
{
    auto file = File(get_input_path(2023, 10));
    string line;
    int sx = 0;
    int y = 0;
    Tile[] grid;
    Point!int start = Point!int(-1, -1);
    while ((line = file.readln.strip) !is null) {
        if (sx == 0) sx = line.length.to!int;
        enforce(sx == line.length.to!int, "Bad input!");
        foreach (x, c; line) {
            Tile t = c.get_tile;
            if (t == Tile.Unknown) {
                start = Point!int(x.to!int, y);
            }
            grid ~= t;
        }
        y += 1;
    }
    enforce(start != Point!int(-1, -1), "Couldn't find starting point.");
    return Layout(new Grid2D!Tile(Point!int(sx, y), grid), start);
}

struct TileInfo
{
    Point!int location;
    int score;
}

struct Part1Return
{
    int pt1_solution;  // The number we actually want from Part 1.
    Grid2D!int scores;  // We already calculated these in Part 1 and they're helpful for Part 2.
}

Part1Return part_1(ref Layout layout)
{
    DList!TileInfo queue;
    layout.identify_start;  // We need to know which tiles the start is actually attached to.
    queue.insertBack(TileInfo(layout.start, 0));
    auto scores = new Grid2D!int(layout.grid.size, -1);
    while (!queue.empty) {
        auto t = queue.front;
        // -1 means we haven't visited the tile yet (we don't want to backtrack after all).
        // t.score + 1 will be the score for this tile; if the score that's already there is
        // higher, we found a faster way to get there, so we need to update the score
        if (scores[t.location] < 0 || scores[t.location] > t.score + 1) {
            scores[t.location] = t.score;
            foreach(neighbor; layout.get_neighbors(t.location)) {
                queue.insertBack(TileInfo(neighbor, t.score + 1));
            }
        } 
        queue.removeFront;
    }
    // Note that we don't visit every tile. All tiles that aren't part of the loop will
    // still carry a score of -1, while all tiles that are part of it have a score >= 0.
    return Part1Return(scores.layout.maxElement, scores);
}

enum TileP2
{
    Obstacle,
    Inside,
    Outside,
    Unknown,  // An outside or inside tile that has yet to be identified.
    PendingIdentification  // An unknown tile that we've started working to identify.
}

// Tile replacement definitions for use when "inflating" the layout.
TileP2[9] pt2_substitutions(Tile tile, int score) 
{
    // If the tile is not part of the loop, it doesn't matter what's on it,
    // so just return an empty 3x3 tile.
    if (score == -1) return [
        TileP2.Unknown, TileP2.Unknown, TileP2.Unknown,
        TileP2.Unknown, TileP2.Unknown, TileP2.Unknown,
        TileP2.Unknown, TileP2.Unknown, TileP2.Unknown
    ];
    switch (tile) {
    case Tile.Horizontal:
        return [
            TileP2.Unknown, TileP2.Unknown, TileP2.Unknown,
            TileP2.Obstacle, TileP2.Obstacle, TileP2.Obstacle,
            TileP2.Unknown, TileP2.Unknown, TileP2.Unknown
        ];
    case Tile.Verticle:
        return [
            TileP2.Unknown, TileP2.Obstacle, TileP2.Unknown,
            TileP2.Unknown, TileP2.Obstacle, TileP2.Unknown,
            TileP2.Unknown, TileP2.Obstacle, TileP2.Unknown
        ];
    case Tile.N_to_E:
        return [
            TileP2.Unknown, TileP2.Obstacle, TileP2.Unknown,
            TileP2.Unknown, TileP2.Obstacle, TileP2.Obstacle,
            TileP2.Unknown, TileP2.Unknown, TileP2.Unknown
        ];
    case Tile.N_to_W:
        return [
            TileP2.Unknown, TileP2.Obstacle, TileP2.Unknown,
            TileP2.Obstacle, TileP2.Obstacle, TileP2.Unknown,
            TileP2.Unknown, TileP2.Unknown, TileP2.Unknown
        ];
    case Tile.S_to_E:
        return [
            TileP2.Unknown, TileP2.Unknown, TileP2.Unknown,
            TileP2.Unknown, TileP2.Obstacle, TileP2.Obstacle,
            TileP2.Unknown, TileP2.Obstacle, TileP2.Unknown
        ];
    case Tile.S_to_W:
        return [
            TileP2.Unknown, TileP2.Unknown, TileP2.Unknown,
            TileP2.Obstacle, TileP2.Obstacle, TileP2.Unknown,
            TileP2.Unknown, TileP2.Obstacle, TileP2.Unknown
        ];
    default:
        assert(0);
    }
}

// Offsets to convert the coordinates in the regular-size layout
// to the 9 corresponding tiles in the inflated-size layout.
// Note that the regular-size coordinates must be multipled by 3 first.
static const Point!int[9] pt2_offsets = [
    Point!int(0, 0), Point!int(1, 0), Point!int(2, 0),
    Point!int(0, 1), Point!int(1, 1), Point!int(2, 1),
    Point!int(0, 2), Point!int(1, 2), Point!int(2, 2)
];

// Essentially zooms in on the layout by replacing the tiles representing connections
// to a 3x3 tile where each element is either solid (TileP2.Obstacle) or non-solid
// (TileP2.Unknown, called such because it has yet to be ID'd as either Outside or Inside)
// This will form gaps where the connections don't block access to the outside,
// thus allowing us to simply "flood fill" the tiles to see if they're connected to outside.
Grid2D!TileP2 inflate_grid(const ref Grid2D!Tile tiles, const ref Grid2D!int scores)
{
    auto grid = new Grid2D!TileP2(Point!int(tiles.size.x * 3, tiles.size.y * 3));
    for (int y = 0; y < scores.size.y; ++y) {
        for (int x = 0; x < scores.size.x; ++x) {
            auto pt = Point!int(x, y);
            // Note: Here, since it's not important, for simplicity we discard whatever pipe
            // that are not part of the loop (happens in the call to pt2_substitutions).
            // That way we don't have to worry about edge cases like e.g. a section of tiles
            // that is outside the loop and thus should be identified as outside, but is blocked
            // from the layout edge (used to detect outside tiles) by random non-loop junk.
            TileP2[9] tile_subs = pt2_substitutions(tiles[pt], scores[pt]);
            auto adj_pt = Point!int(x * 3, y * 3);
            for (size_t i = 0; i < tile_subs.length; ++i) {
                grid[adj_pt + pt2_offsets[i]] = tile_subs[i];
            }
        }
    }
    return grid;
}

// NOTE: Modifies tiles in place, replacing Unknown tiles with either Outside or Inside
// depending on their location.
void identify_tiles(ref Grid2D!TileP2 tiles)
{
    static const Point!int[4] neighbors = [NORTH, SOUTH, EAST, WEST];

    void set_linked(const ref Point!int[] linked, TileP2 set_to) {
        foreach(pt; linked) {
            tiles[pt] = set_to;
        }
    }

    void identify_tile(Point!int point) 
    in (tiles[point] == TileP2.Unknown)
    {
        DList!(Point!int) queue;
        tiles[point] = TileP2.PendingIdentification;
        Point!int[] linked; // Array of tiles we end up visiting.
        queue.insertBack(point);
        bool found_world_edge = false;
        // This basically "flood fills" from the starting tile.
        while (!queue.empty) {
            auto pt = queue.front;
            linked ~= pt;
            foreach(neighbor; neighbors) {
                // If we can reach an out-of-bounds tile, that means this tile and the ones
                // attached to it are Outside tiles.
                if (!tiles.in_bounds(pt + neighbor)) found_world_edge = true;
                // We've either already queued/visited this tile, or it's a wall.
                else if (tiles[pt + neighbor] != TileP2.Unknown) continue;
                // Haven't visited it yet, so mark it pending and queue it up.
                else {
                    tiles[pt + neighbor] = TileP2.PendingIdentification;
                    queue.insertBack(pt + neighbor);
                }
            }
            queue.removeFront;
        }
        
        // It isn't actually necessary to explicitly identify Outside tiles;
        // they can safely be left marked as PendingIdentification.
        // However, my measurements indicate the runtime impact is negligible
        // and it's useful information for debugging purposes.
        set_linked(linked, (found_world_edge) ? TileP2.Outside : TileP2.Inside);
    }

    // "Flood fill" from any tile that we haven't identified yet.
    // We don't want to miss a spot that a previous flood fill couldn't reach!
    for (int y = 0; y < tiles.size.y; ++y) {
        for (int x = 0; x < tiles.size.x; ++x) {
            auto pt = Point!int(x, y);
            if (tiles[pt] != TileP2.Unknown) continue;
            identify_tile(pt);
        }
    }
}

// Now we convert back from the inflated tiles to the regular-size tiles, somewhat...
// We just need to know if it's inside, or anything else.
bool tile_is_inside(Point!int location, const ref Grid2D!TileP2 grid, const ref Grid2D!int scores)
{
    if (scores[location] >= 0) return false;  // Any tile that was part of the loop can't be an inside tile.
    // Since we filtered out non-loop tiles when we made the inflated grid,
    // all the tiles that aren't part of the loop will be either entirely inside or entirely outside, 
    // so we only need to examine one tile out of each 3x3 once we know it's not part of the loop.
    return (grid[Point!int(location.x * 3, location.y * 3)] == TileP2.Inside);
}

int count_inside_tiles(const ref Grid2D!TileP2 grid, const ref Grid2D!int scores)
{
    int total = 0;
    for (int y = 0; y < scores.size.y; ++y) {
        for (int x = 0; x < scores.size.x; ++x) {
            total += tile_is_inside(Point!int(x, y), grid, scores);
        }
    }
    return total;
}

int part_2(Grid2D!Tile raw_tiles, Grid2D!int scores)
{
    auto tiles = inflate_grid(raw_tiles, scores);  // See inflate_grid's comments for why this is done.
    tiles.identify_tiles;
    return count_inside_tiles(tiles, scores);
}

bool run_2023_day10()
{
    // Future Self Note: Not ideal for copy/pasting to start a new day due to the values returned by Part 1.
    auto start_time = MonoTime.currTime;
    auto layout = parse_input;
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(layout);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(layout.grid, pt1_solution.scores);
    auto end_time = MonoTime.currTime;

    writefln("Steps to furthest point (part 1): %s", pt1_solution.pt1_solution);
    writefln("Tiles enclosed by loop (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}

// No-longer-used pretty-printing function.
version (none) 
{
    void print_tileP2_grid(const ref Grid2D!TileP2 grid) 
    {
        writeln("Grid:");
        size_t i = 0;
        for (int y = 0; y < grid.size.y; ++y) {
            if (y % 3 == 0) write("\n");
            for (int x = 0; x < grid.size.x; ++x) {
                if (x % 3 == 0) write(" ");
                char c;
                final switch (grid[Point!int(x, y)]) {
                case TileP2.Inside:
                    c = 'I';
                    break;
                case TileP2.Outside:
                    c = 'O';
                    break;
                case TileP2.Obstacle:
                    c = '#';
                    break;
                case TileP2.Unknown:
                    c = '?';
                    break;
                case TileP2.PendingIdentification:
                    c = 'P';
                    break;
                }
                write(c);
            }
            write("\n");
        }
    }
}