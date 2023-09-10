import json

import flet as ft


def main(page: ft.Page):
    def add_selection(event: ft.ControlEvent):
        selections.append(event.control.text)
        selections_display.value = ""

        overflow_count = 0
        for selection in selections:
            if overflow_count == 3:
                selections_display.value += "\n"
                overflow_count = 0
            selections_display.value += f"{selection}, "
            overflow_count += 1

        if len(selections) == 30:
            print(
                json.dumps(
                    {
                        "answers": [
                            selections[i : i + 3] for i in range(0, len(selections), 3)
                        ]
                    }
                )
            )
            selections.clear()
            selections_display.value = ""

        page.update()

    page.title = "Manual Classifier"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 50
    page.update()
    selections: list[str] = []

    heroes_grid = ft.GridView(
        expand=False,
        runs_count=15,
        max_extent=100,
        child_aspect_ratio=1.5,
        spacing=10,
        run_spacing=10,
    )
    page.add(heroes_grid)

    heroes = [
        "D.Va",
        "Doomfist",
        "Junker Queen",
        "Orisa",
        "Ramattra",
        "Reinhardt",
        "Sigma",
        "Winston",
        "Wrecking Ball",
        "Zarya",
        "SPACE",
        "Ashe",
        "Bastion",
        "Cassidy",
        "Echo",
        "Genji",
        "Hanzo",
        "Junkrat",
        "Mei",
        "Pharah",
        "Reaper",
        "Sojourn",
        "Soldier 76",
        "Sombra",
        "Symmetra",
        "Torbjorn",
        "Tracer",
        "Widowmaker",
        "SPACE",
        "Ana",
        "Baptiste",
        "Brigitte",
        "Lucio",
        "Mercy",
        "Moira",
        "Zenyatta",
        "Kiriko",
        "LifeWeaver" "SPACE",
        "Blank",
    ]
    for hero in heroes:
        if hero == "SPACE":
            heroes_grid.controls.append(ft.IconButton(icon=ft.icons.STAR))
            heroes_grid.controls.append(ft.IconButton(icon=ft.icons.STAR))
            heroes_grid.controls.append(ft.IconButton(icon=ft.icons.STAR))
            heroes_grid.controls.append(ft.IconButton(icon=ft.icons.STAR))
            heroes_grid.controls.append(ft.IconButton(icon=ft.icons.STAR))
            heroes_grid.controls.append(ft.IconButton(icon=ft.icons.STAR))
            heroes_grid.controls.append(ft.IconButton(icon=ft.icons.STAR))
            heroes_grid.controls.append(ft.IconButton(icon=ft.icons.STAR))
            heroes_grid.controls.append(ft.IconButton(icon=ft.icons.STAR))
            continue
        heroes_grid.controls.append(ft.FilledButton(text=hero, on_click=add_selection))
    page.update()
    selections_display = ft.Text("No Selections Yet")
    page.add(selections_display)


ft.app(target=main)
