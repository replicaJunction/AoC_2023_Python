"""Day 2: Cube Conundrum

https://adventofcode.com/2023/day/2
"""

from dataclasses import dataclass
import logging
import re
from typing import Any, Sequence, TextIO
import click

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Bag:
    red: int
    green: int
    blue: int

    @property
    def power(self) -> int:
        return self.red * self.green * self.blue

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Bag):
            raise ValueError(f"Cannot compare a Bag to a {type(other)}")
        return self.red < other.red and self.green < other.green and self.blue < other.blue

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, Bag):
            raise ValueError(f"Cannot compare a Bag to a {type(other)}")
        return self.red <= other.red and self.green <= other.green and self.blue <= other.blue


@dataclass(frozen=True)
class Game:
    index: int
    bags: list[Bag]

    def is_possible_with(self, bag: Bag) -> bool:
        return all([x <= bag for x in self.bags])

RE_RED = re.compile(pattern=r"(\d+) red", flags=re.IGNORECASE)
RE_GREEN = re.compile(pattern=r"(\d+) green", flags=re.IGNORECASE)
RE_BLUE = re.compile(pattern=r"(\d+) blue", flags=re.IGNORECASE)

def parse_bag(pull: str) -> Bag:
    red_match = RE_RED.search(pull)
    red = int(red_match.group(1)) if red_match else 0

    green_match = RE_GREEN.search(pull)
    green = int(green_match.group(1)) if green_match else 0

    blue_match = RE_BLUE.search(pull)
    blue = int(blue_match.group(1)) if blue_match else 0

    logger.debug("Pull: [%s]; red=%s, green=%s, blue=%s", pull, red, green, blue)

    return Bag(red=red, green=green, blue=blue)


def parse_line(line: str) -> Game:
    logger.debug("Parsing line: [%s]", line)
    game, pulls = line.split(":", maxsplit=2)
    match = re.search(pattern=r"Game (\d+)", string=game, flags=re.IGNORECASE)
    if not match:
        raise RuntimeError(f"Could not parse the game index from the text {line}")

    index = int(match.group(1))
    bags = [parse_bag(x) for x in pulls.split(";")]

    logger.debug("Line [%s]: index=%s, bags=%s", line, index, bags)
    return Game(index=index, bags=bags)

def get_minimum_viable_bag(game: Game) -> Bag:
    result = Bag(
        red=max(x.red for x in game.bags),
        green=max(x.green for x in game.bags),
        blue=max(x.blue for x in game.bags),
    )
    logger.debug("get_minimum_viable_bag: result bag [%s] for Game [%s]", result, game)
    return result


def solve_day2_part1(bag: Bag, text_lines: Sequence[str]) -> int:
    games = [parse_line(x.strip()) for x in text_lines if x.strip()]
    logger.debug("solve_day2_part1: all games: %s", games)

    possible_game_ids = [x.index for x in games if x.is_possible_with(bag)]
    logger.info("solve_day2_part1: possible games: %s", possible_game_ids)

    result = sum(possible_game_ids)
    logger.info("solve_day2_part1: solution=%s", result)
    return result

def solve_day2_part2(text_lines: Sequence[str]) -> int:
    games = [parse_line(x.strip()) for x in text_lines if x.strip()]
    logger.debug("solve_day2_part1: all games: %s", games)

    viable_bags = [get_minimum_viable_bag(x) for x in games]
    powers = [x.power for x in viable_bags]
    logger.info("Powers of viable bags: %s", powers)
    result = sum(powers)
    logger.info("Result: %s", result)
    result = sum(powers)

    return result


# Boilerplate for CLI handling

SAMPLE_INPUT = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".splitlines()

@click.group
def cli():
    pass

@cli.command
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose logging. Pass multiple times for extra verbosity.",
)
def sample1(verbose: int):
    log_level = logging.DEBUG if verbose >= 2 else logging.INFO if verbose == 1 else logging.WARNING
    logging.basicConfig(level=log_level)

    expected_result = 8

    sample_bag = Bag(red=12, green=13, blue=14)
    actual_result = solve_day2_part1(bag=sample_bag, text_lines=SAMPLE_INPUT)

    print("Day 2 part 1 sample: expected:", expected_result, "; actual:", actual_result)

@cli.command
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose logging. Pass multiple times for extra verbosity.",
)
def sample2(verbose: int):
    log_level = logging.DEBUG if verbose >= 2 else logging.INFO if verbose == 1 else logging.WARNING
    logging.basicConfig(level=log_level)

    expected_result = 2286

    actual_result = solve_day2_part2(text_lines=SAMPLE_INPUT)

    print("Day 2 part 2 sample: expected:", expected_result, "; actual:", actual_result)

@cli.command()
@click.option(
    "-i",
    "--input-file",
    type=click.File(mode="rt"),
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose logging. Pass multiple times for extra verbosity.",
)
def part1(input_file: TextIO, verbose: int) -> None:
    log_level = logging.DEBUG if verbose >= 2 else logging.INFO if verbose == 1 else logging.WARNING
    logging.basicConfig(level=log_level)

    puzzle_input = input_file.readlines()

    expected_bag = Bag(red=12, green=13, blue=14)
    puzzle_solution = solve_day2_part1(expected_bag, puzzle_input)
    print("Solution to Day 2 part 1:", puzzle_solution)

@cli.command()
@click.option(
    "-i",
    "--input-file",
    type=click.File(mode="rt"),
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose logging. Pass multiple times for extra verbosity.",
)
def part2(input_file: TextIO, verbose: int) -> None:
    log_level = logging.DEBUG if verbose >= 2 else logging.INFO if verbose == 1 else logging.WARNING
    logging.basicConfig(level=log_level)

    puzzle_input = input_file.readlines()

    puzzle_solution = solve_day2_part2(puzzle_input)
    print("Solution to Day 2 part 2:", puzzle_solution)


if __name__ == "__main__":
    cli()
