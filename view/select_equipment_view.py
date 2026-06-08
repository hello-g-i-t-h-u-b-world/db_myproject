# view/select_equipment_view.py
import flet as ft
from repository import equipment_master_repo
from service.equipment_service import create_user_equipment
from view.enhancement_simulator_view import cube_simulator_view

EQUIPMENT_IMAGES: dict[int, str] = {
    1: "1.png",
    2: "2.png",
    3: "3.png",
    4: "4.png",
    5: "5.png",
}


def select_equipment_view(page: ft.Page) -> ft.Container:
    equipments = equipment_master_repo.get_all()

    def on_equipment_selected(equipment_id: int) -> None:
        user_equipment_id = create_user_equipment(equipment_id)
        page.clean()
        page.add(cube_simulator_view(page, user_equipment_id))

    def go_to_saved(e) -> None:
        from view.saved_equipment_view import saved_equipment_view
        page.clean()
        page.add(saved_equipment_view(page))

    # ── 새 장비 생성 카드 목록 ────────────────────────────────────────────
    new_equipment_cards: list[ft.Control] = []
    for equipment_id, equipment_name, equipment_type in equipments:
        img_src = EQUIPMENT_IMAGES.get(equipment_id)
        icon_widget = (
            ft.Image(src=img_src, width=40, height=40)
            if img_src
            else ft.Icon(ft.Icons.SHIELD_OUTLINED, size=36, color=ft.Colors.GREY_400)
        )

        new_equipment_cards.append(
            ft.Container(
                content=ft.Row(
                    [
                        icon_widget,
                        ft.Column(
                            [
                                ft.Text(
                                    equipment_name,
                                    size=15,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    equipment_type,
                                    size=12,
                                    color=ft.Colors.GREY_400,
                                ),
                            ],
                            spacing=2,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=ft.Padding(left=16, right=16, top=12, bottom=12),
                width=300,
                on_click=lambda e, eid=equipment_id: on_equipment_selected(eid),
                ink=True,
            )
        )

    # ── 기존 장비 불러오기 버튼 ───────────────────────────────────────────
    load_button = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.INVENTORY_2_OUTLINED, color=ft.Colors.TEAL_300, size=22),
                ft.Text(
                    "기존 장비 불러오기",
                    size=15,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.TEAL_300,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        bgcolor=ft.Colors.GREY_800,
        border_radius=10,
        padding=ft.Padding(left=16, right=16, top=14, bottom=14),
        width=300,
        border=ft.Border(left=ft.BorderSide(1, ft.Colors.TEAL_700), right=ft.BorderSide(1, ft.Colors.TEAL_700), top=ft.BorderSide(1, ft.Colors.TEAL_700), bottom=ft.BorderSide(1, ft.Colors.TEAL_700)),
        on_click=go_to_saved,
        ink=True,
    )

    # ── 전체 레이아웃 ─────────────────────────────────────────────────────
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Maple Planet",
                    size=14,
                    color=ft.Colors.TEAL_300,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Text(
                    "강화할 장비를 선택하세요",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Divider(height=4, color=ft.Colors.TRANSPARENT),
                ft.Text(
                    "새 장비 생성",
                    size=13,
                    color=ft.Colors.GREY_400,
                    weight=ft.FontWeight.W_500,
                ),
                *new_equipment_cards,
                ft.Divider(height=8, color=ft.Colors.GREY_800),
                load_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        ),
        alignment=ft.Alignment(0, 0),
        padding=30,
        expand=True,
    )