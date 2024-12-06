module directions;

public import utility;

enum Point!int NORTH = Point!int(0, -1);
enum Point!int EAST = Point!int(1, 0);
enum Point!int SOUTH = Point!int(0, 1);
enum Point!int WEST = Point!int(-1, 0);

enum Point!int[4] DIRECTIONS = [NORTH, EAST, SOUTH, WEST];
// Reserved for later.
// enum Point!int[8] DIRECTIONS_8 = [NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST];