"""Day 1: Trebuchet?!

https://adventofcode.com/2023/day/1
"""

import logging
from pprint import pprint
from typing import TextIO

import click

SAMPLE_PUZZLE_INPUT_PART_1 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

SAMPLE_PUZZLE_SOLUTION_PART_1 = 142

SAMPLE_PUZZLE_INPUT_PART_2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

SAMPLE_PUZZLE_SOLUTION_PART_2 = 281

# Since we'll be parsing by the first and last digit, it's okay if there
# are some extra characters. Handling it this way will prevent edge
# cases where the words overlap, such as "eighthree" instead of
# "eightthree".
# Credit to this post:
# https://old.reddit.com/r/adventofcode/comments/1884fpl/2023_day_1for_those_who_stuck_on_part_2/

DIGIT_REPLACEMENTS: list[tuple[str, str]] = [
    ("one", "o1e"),
    ("two", "t2o"),
    ("three", "t3e"),
    ("four", "f4r"),
    ("five", "f5e"),
    ("six", "s6x"),
    ("seven", "s7n"),
    ("eight", "e8t"),
    ("nine", "n9e"),
]

logger = logging.getLogger(__name__)


def is_int(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def get_first_digit(line: str) -> str:
    for char in line:
        try:
            int(char)
            return char
        except ValueError:
            continue
    raise ValueError(f"Could not find a valid digit in the string {line}")


def fix_spelled_words(line: str) -> str:
    for i in range(len(line)):
        for word, digit in DIGIT_REPLACEMENTS:
            target = line[i:i+len(word)]
            if target == word:
                logger.debug("Line %s hit a replacement at index %s: %s", line, i, word)
                new_line = line.replace(word, digit)
                return fix_spelled_words(new_line)

    return line

    # result = line[:]
    # for word, digit in DIGIT_REPLACEMENTS:
    #     result = result.replace(word, digit)
    return result


def get_first_digit_or_word(line: str) -> str:
    return get_first_digit(fix_spelled_words(line))


def get_calibration_value(line: str) -> int:
    first_digit = get_first_digit(line)
    last_digit = get_first_digit(line[::-1])
    calibration_value = int(first_digit + last_digit)
    logger.debug(
        "get_calibration_value: line=[%s], first_digit=%s, last_digit=%s, calibration_value=%s",
        line,
        first_digit,
        last_digit,
        calibration_value,
    )
    return calibration_value


def get_calibration_value_with_words(line: str) -> int:
    # first_digit = get_first_digit_or_word(line)
    # last_digit = get_first_digit_or_word(line[::-1])
    # logger.debug(
    #     "get_calibration_value: line=[%s], first_digit=%s, last_digit=%s",
    #     line,
    #     first_digit,
    #     last_digit,
    # )
    # return int(first_digit + last_digit)
    result = get_calibration_value(fix_spelled_words(line))
    logger.info("Line: [%s]; result: [%s]", line, result)
    # input("Press Enter")
    return result


def solve_day1_part1(puzzle_input: str) -> int:
    values = [get_calibration_value(line) for line in puzzle_input.splitlines() if line]
    result = sum(values)
    logger.debug("solve_day1_part1: solution=%s", result)
    return result


def solve_day1_part2(puzzle_input: str) -> int:
    values = [
        get_calibration_value_with_words(line)
        for line in puzzle_input.splitlines()
        if line
    ]
    result = sum(values)
    logger.debug("solve_day1_part2: values=%s", values)
    logger.info("solve_day1_part2: solution=%s", result)
    return result


@click.command()
@click.option(
    "-i",
    "--input-file",
    type=click.File(mode="rt"),
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose logging",
)
def main(input_file: TextIO, verbose: bool):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    sample_solution_part_1 = solve_day1_part1(SAMPLE_PUZZLE_INPUT_PART_1)
    assert sample_solution_part_1 == SAMPLE_PUZZLE_SOLUTION_PART_1

    sample_solution_part_2 = solve_day1_part2(SAMPLE_PUZZLE_INPUT_PART_2)
    assert sample_solution_part_2 == SAMPLE_PUZZLE_SOLUTION_PART_2

    puzzle_input = input_file.read()
    puzzle_solution = solve_day1_part1(puzzle_input)
    print("Solution to Day 1 part 1:")
    pprint(puzzle_solution)

    part_two_solution = solve_day1_part2(puzzle_input)
    print("Solution to Day 1 part 2:")
    pprint(part_two_solution)


if __name__ == "__main__":
    main()
