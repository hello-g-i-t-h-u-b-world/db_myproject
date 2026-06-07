import flet as ft
from view.select_equipment_view import select_equipment_view

def main(page: ft.Page):
    page.title = "메이플 큐브 시뮬레이터"
    page.window_width = 450
    page.window_height = 700
    
    # 초기 화면 로드
    page.add(select_equipment_view(page))

if __name__ == "__main__":
    ft.run(main)