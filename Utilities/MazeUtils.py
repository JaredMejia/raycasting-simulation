#!/usr/bin/env python

"""
You can use this file as a command line script, or as a library.

Example of computing the percent a location is through the maze:

    python MazeUtils.py ../Worlds/maze.txt --percent 1.5 7.5

Same thing when using this as a library

    import sys
    sys.append("Path/to/this/directory/")
    from MazeUtils import read_maze_file, percent_through_maze

    maze, _, _, maze_directions, _ = read_maze_file(maze_filepath)
    start_x, start_y, _ = maze_directions[0]
    end_x, end_y, _ = maze_directions[-1]

    x = location_reached_by_network_or_person.x
    y = location_reached_by_network_or_person.y

    p = percent_through_maze(maze, x, y, start_x, start_y, end_x, end_y)
"""

from argparse import ArgumentParser
from math import inf
from typing import List, Tuple


def read_maze_file(
    filepath: str,
) -> Tuple[List[List[int]], int, int, List[Tuple[int, int, str]], List[str]]:
    """Read a maze file and return values

    Args:
        filepath (str): path to a maze file

    Returns:
        Tuple[List[List[int]]: a maze
        int: maze width
        int: maze height
        List[Tuple[int, int, str]]: turn by turn directions
        List[str]]: texture names
    """
    with open(filepath, "r") as maze_file:
        num_textures = int(maze_file.readline())
        texture_names = [maze_file.readline() for _ in range(num_textures)]
        maze_x_dim, maze_y_dim = [int(dim) for dim in maze_file.readline().split()]
        maze = [
            [int(cell) for cell in maze_file.readline().split()]
            for _ in range(maze_y_dim)
        ]
        maze_directions = [
            (int(line.split()[0]), int(line.split()[1]), line.split()[2])
            for line in maze_file.readlines()
        ]

    return list(reversed(maze)), maze_x_dim, maze_y_dim, maze_directions, texture_names


def bfs_dist_maze(maze: List[List[int]], x1: int, y1: int, x2: int, y2: int) -> float:
    """Compute the number of hops from (x1,y1) to (x2,y2).

    Args:
        maze (List[List[int]]): A grid based maze
        x1 (int): starting x location
        y1 (int): starting y location
        x2 (int): ending x location
        y2 (int): ending y location

    Returns:
        float: The number of hops from start to end returned as a float
    """

    queue = [(x1, y1)]
    visited = {(x1, y1)}
    distances = {(x1, y1): 0}

    while queue:

        x_min = 0
        x_max = len(maze[0]) - 1
        y_min = 0
        y_max = len(maze) - 1

        x, y = queue.pop(0)

        if x == x2 and y == y2:
            return distances[(x, y)]

        # Check up and down
        if y + 1 <= y_max and maze[y + 1][x] == 0 and (x, y + 1) not in visited:
            visited.add((x, y + 1))
            queue.append((x, y + 1))
            distances[(x, y + 1)] = distances[(x, y)] + 1
        if y_min <= y - 1 and maze[y - 1][x] == 0 and (x, y - 1) not in visited:
            visited.add((x, y - 1))
            queue.append((x, y - 1))
            distances[(x, y - 1)] = distances[(x, y)] + 1

        # Check right and left
        if x + 1 <= x_max and maze[y][x + 1] == 0 and (x + 1, y) not in visited:
            visited.add((x + 1, y))
            queue.append((x + 1, y))
            distances[(x + 1, y)] = distances[(x, y)] + 1
        if x_min <= x - 1 and maze[y][x - 1] == 0 and (x - 1, y) not in visited:
            visited.add((x - 1, y))
            queue.append((x - 1, y))
            distances[(x - 1, y)] = distances[(x, y)] + 1

        if len(queue) > 10:
            break

    return inf


def percent_through_maze(
    maze, x: int, y: int, x_start: int, y_start: int, x_end: int, y_end: int,
) -> float:
    """Compute distance traveled along optimal path through maze.

    Args:
        maze ([type]): a maze
        x (float): current x location
        y (float): current y location
        x_start (float): starting x location
        y_start (float): starting y location
        x_end (float): ending x location
        y_end (float): ending y location

    Returns:
        float: percent traveled through maze
    """

    dist_start_to_current = bfs_dist_maze(maze, x_start, y_start, x, y)
    dist_start_to_end = bfs_dist_maze(maze, x_start, y_start, x_end, y_end)

    # TODO: verify that we are actually on the path?

    return (dist_start_to_current / dist_start_to_end) * 100


def main():
    arg_parser = ArgumentParser("Run a maze utility")
    arg_parser.add_argument("maze_filepath", help="Path to a maze file.")
    arg_parser.add_argument(
        "--percent",
        nargs=2,
        metavar=("x", "y"),
        type=float,
        help="Compute maze completion percentage.",
    )

    args = arg_parser.parse_args()

    if args.percent:
        x, y = args.percent
        maze, _, _, maze_directions, _ = read_maze_file(args.maze_filepath)
        start_x, start_y, _ = maze_directions[0]
        end_x, end_y, _ = maze_directions[-1]

        print(
            percent_through_maze(maze, int(x), int(y), start_x, start_y, end_x, end_y)
        )


if __name__ == "__main__":
    main()