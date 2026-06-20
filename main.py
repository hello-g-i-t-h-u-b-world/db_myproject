import flet as ft
from view.select_equipment_view import select_equipment_view


def main(page: ft.Page) -> None:
    page.title = "메이플플래닛 강화 시뮬레이터"
    page.window.width = 450
    page.window.height = 750
    page.bgcolor = ft.Colors.GREY_900
    page.theme_mode = ft.ThemeMode.DARK

    page.add(select_equipment_view(page))


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")