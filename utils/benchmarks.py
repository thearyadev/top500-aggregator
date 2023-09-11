import sys

sys.path.append("./")  # used to import from root directory
import json
import os

# import pyautogui as pg
from rich import print

import heroes as HeroComparisonClass
import leaderboards


def show_result(
    result: str,
    test_name: str,
    expected: list[str],
    predicted: list[str],
) -> None:
    """Prints a result in a pretty way

    Args:
        result (str): The result
        expected (str): The expected result
    """
    if result == "PASS":
        print(
            f"[green]PASS[/green] [blue]{test_name}[/blue]\n\t{expected} == {predicted}"
        )
    else:
        incorrect_indicies: list[int] = list()
        for index, (e, p) in enumerate(zip(expected, predicted)):
            if e != p:
                incorrect_indicies.append(index)

        for index in incorrect_indicies:
            predicted[index] = f"[red]{predicted[index]}[/red]"

        print(f"[red]FAIL[/red] [blue]{test_name}[/blue]\n\t{expected} != {predicted}")


def load_answers(tests_path: str) -> dict[str, list[list[str]]]:
    """Loads answers from a file

    Args:
        tests_path (str): Path to the file

    Returns:
        dict[str, list[list[str]]]: Dictionary of answers
    """
    answers: dict[str, list[list[str]]] = {}
    tests = os.listdir(tests_path)
    for testdir in tests:
        test_path = os.path.join(tests_path, testdir)
        with open(os.path.join(test_path, "key.json"), "r") as file:
            answers[testdir] = json.load(file)["answers"]
    return answers


def filter_blanks(hero_array: list[str]) -> list[str]:
    """Converts all Blank2 instances in an array to Blank

    Args:
        hero_array (list[str]): Array of heroes (as string)

    Returns:
        list[str]: Array of heroes as string, without blank2
    """
    for index, hero in enumerate(hero_array):
        if hero == "Blank2":
            hero_array[index] = "Blank"
    return hero_array


def main():
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0

    answers = load_answers("./assets/test_leaderboard_images")
    heroes_present: set[str] = set()
    for image, heroes in answers.items():  # iter answer key-value pairs
        result: list[
            leaderboards.LeaderboardEntry
        ] = leaderboards.parse(  # parse leaderboard
            image_path=f"./assets/test_leaderboard_images/{image}/LB-IMG.png",
            assets_path="./assets/hero_images",
            region=leaderboards.Region.AMERICAS,  # doesnt matter
            role=leaderboards.Role.DAMAGE,  # doesnt matter
            model_name="thearyadev-2023-08-25",
        )

        for entry, answer in zip(result, heroes):  # validate results
            single_entry_hero_predicted: list[str] = filter_blanks(
                [str(i) for i in entry.heroes]
            )
            if single_entry_hero_predicted != answer:  # on fail
                show_result(
                    result="FAIL",
                    test_name=image,
                    expected=answer,
                    predicted=single_entry_hero_predicted,
                )
                failed_tests += 1
            else:
                show_result(
                    result="PASS",
                    test_name=image,
                    expected=answer,
                    predicted=single_entry_hero_predicted,
                )
                passed_tests += 1
            heroes_present.update(answer)
            total_tests += 1

    print("\n\n")
    # display results
    print(f"Total tests: {total_tests}")
    print(f"Passed tests: {passed_tests}")
    print(f"Failed tests: {failed_tests}")
    print(f"[yellow bold]Success rate: {round(passed_tests / total_tests * 100, 2)}%")
    if len(heroes_present) == 0:
        print(
            f"Heroes not present in answer set: {heroes_present.symmetric_difference(set(HeroComparisonClass.Heroes('./assets/hero_images').hero_labels.values()))}"
        )


if __name__ == "__main__":
    import time

    start = time.perf_counter()
    main()
    print(f"Time taken: {time.perf_counter() - start} seconds")
