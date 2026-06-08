# view/saved_equipment_view.py
import flet as ft
from service.user_equipment_service import get_all_user_equipments

GRADE_COLORS = {
    "Rare": ft.Colors.BLUE_400,
    "Epic": ft.Colors.PURPLE_400,
    "Unique": ft.Colors.AMBER_500,
}

EQUIPMENT_IMAGES: dict[int, str] = {
    1: "1.png",
    2: "2.png",
    3: "3.png",
    4: "4.png",
    5: "5.png",
}


def saved_equipment_view(page: ft.Page) -> ft.Container:
    equipments = get_all_user_equipments()

    def on_select(user_equipment_id: int) -> None:
        from view.enhancement_simulator_view import cube_simulator_view
        page.clean()
        page.add(cube_simulator_view(page, user_equipment_id))

    def go_back(e) -> None:
        from view.select_equipment_view import select_equipment_view
        page.clean()
        page.add(select_equipment_view(page))

    # ── 장비 카드 목록 ─────────────────────────────────────────────────────
    cards: list[ft.Control] = []

    if not equipments:
        cards.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.INBOX_OUTLINED, size=48, color=ft.Colors.GREY_600),
                        ft.Text(
                            "저장된 장비가 없습니다.",
                            size=15,
                            color=ft.Colors.GREY_500,
                        ),
                        ft.Text(
                            "메인 화면에서 장비를 새로 생성해보세요.",
                            size=12,
                            color=ft.Colors.GREY_600,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                alignment=ft.Alignment(0, 0),
                padding=40,
            )
        )
    else:
        for eq in equipments:
            uid = eq["user_equipment_id"]
            eid = eq["equipment_id"]
            grade = eq["potential_grade"]
            grade_color = GRADE_COLORS.get(grade, ft.Colors.WHITE)

            img_src = EQUIPMENT_IMAGES.get(eid)
            icon_widget = (
                ft.Image(src=img_src, width=44, height=44)
                if img_src
                else ft.Icon(ft.Icons.SHIELD_OUTLINED, size=40, color=ft.Colors.GREY_400)
            )

            cards.append(
                ft.Container(
                    content=ft.Row(
                        [
                            icon_widget,
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                eq["equipment_name"],
                                                size=15,
                                                weight=ft.FontWeight.W_600,
                                                color=ft.Colors.WHITE,
                                            ),
                                            ft.Container(
                                                content=ft.Text(
                                                    grade,
                                                    size=11,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=grade_color,
                                                ),
                                                bgcolor=ft.Colors.GREY_900,
                                                padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                                                border_radius=20,
                                            ),
                                        ],
                                        spacing=8,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    ft.Text(
                                        f"{eq['equipment_type']}  |  STR +{eq['bonus_str']}  |  공격력 +{eq['bonus_attack']}",
                                        size=12,
                                        color=ft.Colors.GREY_400,
                                    ),
                                    ft.Text(
                                        f"업그레이드 {eq['upgrade_slot_left']}회 남음",
                                        size=12,
                                        color=(
                                            ft.Colors.GREEN_400
                                            if eq["upgrade_slot_left"] > 0
                                            else ft.Colors.RED_400
                                        ),
                                    ),
                                ],
                                spacing=3,
                                alignment=ft.MainAxisAlignment.CENTER,
                                expand=True,
                            ),
                            ft.Icon(
                                ft.Icons.CHEVRON_RIGHT,
                                color=ft.Colors.GREY_500,
                                size=20,
                            ),
                        ],
                        spacing=14,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=ft.Colors.GREY_800,
                    border_radius=10,
                    padding=ft.Padding(left=14, right=14, top=12, bottom=12),
                    on_click=lambda e, u=uid: on_select(u),
                    ink=True,
                )
            )

    # ── 전체 레이아웃 ─────────────────────────────────────────────────────
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=ft.Colors.WHITE,
                            tooltip="메인으로 돌아가기",
                            on_click=go_back,
                        ),
                        ft.Text(
                            "저장된 장비 불러오기",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                    spacing=4,
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_800),
                ft.Column(
                    cards,
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
            ],
            spacing=8,
            expand=True,
        ),
        padding=12,
        expand=True,
    )