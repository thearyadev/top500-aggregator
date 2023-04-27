from rich import print
import leaderboards
import heroes
import pyautogui as pg


answers = {
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
        ["Doomfist", "Blank2", "Blank2"],
    ],
}


def main():
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0

    for image, heroes in answers.items():
        result: list[leaderboards.LeaderboardEntry] = leaderboards.parse(
                image_path=f"./assets/test_leaderboard_images/{image}",
                assets_path="./assets/hero_images",
                temp_directory="temp",
                region=leaderboards.Region.AMERICAS,  # doesnt matter
                role=leaderboards.Role.DAMAGE,  # doesnt matter
            )
        
        for entry, answer in zip(result, heroes):
            single_entry_hero: list[str] = [str(i) for i in entry.heroes]
            if single_entry_hero != answer: # on fail
                print(f"[red]FAIL[/red] {image} {single_entry_hero} != {answer}")
                failed_tests += 1
            else:
                print(f"[green]PASS[/green] {image} {single_entry_hero} == {answer}")
                passed_tests += 1
            total_tests += 1
    
    print("\n\n")
    print(f"Total tests: {total_tests}")
    print(f"Passed tests: {passed_tests}")
    print(f"Failed tests: {failed_tests}")

        
        





if __name__ == "__main__":
    main()
