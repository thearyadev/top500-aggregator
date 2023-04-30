import pyautogui as pg
from rich import print

import heroes
import leaderboards

answers = {  # 3 leaderboard images; manually identified.
    "DAMAGE_S4_P1_AMERICAS.png": [
        ["Pharah", "Echo", "Mei"],
        ["Tracer", "Echo", "Hanzo"],
        ["Tracer", "Sombra", "Hanzo"],
        ["Tracer", "Echo", "Genji"],
        ["Tracer", "Ashe", "Sombra"],
        ["Tracer", "Widowmaker", "Ashe"],
        ["Bastion", "Tracer", "Widowmaker"],
        ["Tracer", "Hanzo", "Cassidy"],
        ["Sombra", "Tracer", "Ashe"],
        ["Cassidy", "Widowmaker", "Tracer"],
    ],
    "SUPPORT_S4_P1_AMERICAS.png": [
        ["Zenyatta", "Brigitte", "Ana"],
        ["Kiriko", "Zenyatta", "Ana"],
        ["Ana", "Kiriko", "Zenyatta"],
        ["Ana", "Kiriko", "Zenyatta"],
        ["Kiriko", "Lucio", "Zenyatta"],
        ["Brigitte", "Kiriko", "Ana"],
        ["Moira", "Brigitte", "Zenyatta"],
        ["Ana", "Kiriko", "Zenyatta"],
        ["Ana", "Brigitte", "Zenyatta"],
        ["Ana", "Zenyatta", "Baptiste"],
    ],
    "TANK_S4_P1_AMERICAS.png": [
        ["Winston", "Doomfist", "Sigma"],
        ["D.Va", "Sigma", "Zarya"],
        ["Ramattra", "Winston", "D.Va"],
        ["Ramattra", "Wrecking Ball", "Winston"],
        ["Winston", "Wrecking Ball", "Sigma"],
        ["Winston", "Ramattra", "Sigma"],
        ["Winston", "Ramattra", "Sigma"],
        ["D.Va", "Sigma", "Winston"],
        ["Winston", "D.Va", "Doomfist"],
        ["Doomfist", "Blank", "Blank"],
    ],
    "SUPPORT_S4_P44_AMERICAS.png": [
        ["Ana", "Brigitte", "Moira"],
        ["Ana", "Kiriko", "Zenyatta"],
        ["Ana", "Lucio", "Brigitte"],
        ["Ana", "Brigitte", "Kiriko"],
        ["Mercy", "Kiriko", "Ana"],
        ["Lucio", "Zenyatta", "Baptiste"],
        ["Mercy", "Brigitte", "LifeWeaver"],
        ["Ana", "Zenyatta", "Kiriko"],
        ["Mercy", "Kiriko", "Ana"],
        ["Moira", "Zenyatta", "Blank"]
    ], 
}


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

    for image, heroes in answers.items():  # iter answer key-value pairs
        result: list[
            leaderboards.LeaderboardEntry
        ] = leaderboards.parse(  # parse leaderboard
            image_path=f"./assets/test_leaderboard_images/{image}",
            assets_path="./assets/hero_images",
            region=leaderboards.Region.AMERICAS,  # doesnt matter
            role=leaderboards.Role.DAMAGE,  # doesnt matter
            model_path=r"models\thearyadev-2023-04-30\thearyadev-2023-04-30.model",
        )

        for entry, answer in zip(result, heroes):  # validate results
            single_entry_hero: list[str] = filter_blanks([str(i) for i in entry.heroes])
            if single_entry_hero != answer:  # on fail
                print(f"[red]FAIL[/red] {image} {single_entry_hero} != {answer}")
                failed_tests += 1
            else:
                print(f"[green]PASS[/green] {image} {single_entry_hero} == {answer}")
                passed_tests += 1
            total_tests += 1

    print("\n\n")
    # display results
    print(f"Total tests: {total_tests}")
    print(f"Passed tests: {passed_tests}")
    print(f"Failed tests: {failed_tests}")


if __name__ == "__main__":
    main()
