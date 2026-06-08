# view/stats_view.py
import flet as ft
from service.stats_service import get_simulation_result
from service.potential_service import get_equipment_image_id

GRADE_COLORS = {
    "Rare": ft.Colors.BLUE_400,
    "Epic": ft.Colors.PURPLE_400,
    "Unique": ft.Colors.AMBER_500,
}

GRADE_BG = {
    "Rare": ft.Colors.BLUE_900,
    "Epic": ft.Colors.PURPLE_900,
    "Unique": ft.Colors.AMBER_900,
}


def stats_view(page: ft.Page, user_equipment_id: int) -> ft.Container:
    result = get_simulation_result(user_equipment_id)

    if not result:
        return ft.Container(
            content=ft.Text("장비 정보를 불러올 수 없습니다.", color=ft.Colors.RED_400),
            padding=20,
        )

    eq_image_id = get_equipment_image_id(user_equipment_id)
    equipment_image = ft.Image(
        src=f"{eq_image_id}.png",
        width=44,
        height=44,
    )

    grade = result["potential_grade"]
    grade_color = GRADE_COLORS.get(grade, ft.Colors.WHITE)
    grade_bg = GRADE_BG.get(grade, ft.Colors.GREY_900)

    # ── 헤더: 장비명 + 기본 스탯 ──────────────────────────────────────────
    header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        equipment_image,
                        ft.Text(
                            result["equipment_name"],
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(
                    f"누적 STR 증가 : +{result['bonus_str']}",
                    size=14,
                    color=ft.Colors.GREY_300,
                ),
                ft.Text(
                    f"누적 공격력 증가 : +{result['bonus_attack']}",
                    size=14,
                    color=ft.Colors.GREY_300,
                ),
                ft.Text(
                    f"남은 업그레이드 횟수 : [{result['upgrade_slot_left']}]",
                    size=14,
                    color=(
                        ft.Colors.GREEN_400
                        if result["upgrade_slot_left"] > 0
                        else ft.Colors.RED_400
                    ),
                ),
                ft.Row(
                    [
                        ft.Text("현재 잠재 등급 : ", size=14, color=ft.Colors.GREY_300),
                        ft.Text(
                            f"[ {grade} ]",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=grade_color,
                        ),
                    ]
                ),
            ],
            spacing=4,
        ),
        padding=ft.Padding(left=16, right=16, top=12, bottom=12),
        bgcolor=ft.Colors.GREY_900,
        border_radius=10,
    )

    # ── 잠재 옵션 3줄 ──────────────────────────────────────────────────────
    potential_rows = []
    for i, effect in enumerate(result["potential_effects"], start=1):
        potential_rows.append(
            ft.Container(
                content=ft.Text(
                    f"{i}줄 : {effect}",
                    size=15,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.W_500,
                ),
                bgcolor=grade_bg,
                padding=ft.Padding(left=14, right=14, top=10, bottom=10),
                border_radius=6,
            )
        )

    potential_section = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "잠재 옵션",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_200,
                ),
                ft.Column(potential_rows, spacing=6),
            ],
            spacing=8,
        ),
        padding=ft.Padding(left=16, right=16, top=12, bottom=12),
        bgcolor=ft.Colors.GREY_900,
        border_radius=10,
    )

    # ── 사용 기록 테이블 ───────────────────────────────────────────────────
    def make_row(cells: list[str], is_header: bool = False) -> ft.Row:
        color = ft.Colors.GREY_400 if is_header else ft.Colors.WHITE
        weight = ft.FontWeight.BOLD if is_header else ft.FontWeight.W_400
        return ft.Row(
            [
                ft.Container(
                    ft.Text(cells[0], size=13, color=color, weight=weight),
                    expand=3,
                ),
                ft.Container(
                    ft.Text(
                        cells[1],
                        size=13,
                        color=color,
                        weight=weight,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    expand=2,
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(
                    ft.Text(
                        cells[2],
                        size=13,
                        color=color,
                        weight=weight,
                        text_align=ft.TextAlign.RIGHT,
                    ),
                    expand=3,
                    alignment=ft.Alignment(1, 0),
                ),
            ],
            spacing=0,
        )

    log_rows: list[ft.Control] = [
        make_row(["아이템 명", "사용 횟수", "비용"], is_header=True),
        ft.Divider(height=1, color=ft.Colors.GREY_700),
    ]

    if result["usage_logs"]:
        for item_name, item_type, use_count, unit_price, total_cost in result["usage_logs"]:
            bg = ft.Colors.BLUE_900 if item_type == "주문서" else ft.Colors.GREY_800
            log_rows.append(
                ft.Container(
                    content=make_row([
                        item_name,
                        str(use_count),
                        f"{total_cost:,}",
                    ]),
                    bgcolor=bg,
                    padding=ft.Padding(left=10, right=10, top=8, bottom=8),
                    border_radius=6,
                )
            )
    else:
        log_rows.append(
            ft.Text("사용 기록 없음", size=13, color=ft.Colors.GREY_500)
        )

    usage_section = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "사용 기록",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_200,
                ),
                ft.Column(log_rows, spacing=5),
            ],
            spacing=8,
        ),
        padding=ft.Padding(left=16, right=16, top=12, bottom=12),
        bgcolor=ft.Colors.GREY_900,
        border_radius=10,
    )

    # ── 총 사용 비용 ───────────────────────────────────────────────────────
    total_section = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "총 사용 비용",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_200,
                ),
                ft.Row(
                    [
                        ft.Text(
                            f"{result['total_meso']:,}",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.AMBER_400,
                        ),
                        ft.Text(" 메소", size=18, color=ft.Colors.GREY_300),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
            ],
            spacing=6,
        ),
        padding=ft.Padding(left=16, right=16, top=14, bottom=14),
        bgcolor=ft.Colors.GREY_900,
        border_radius=10,
    )

    # ── 돌아가기 (좌상단 아이콘 버튼 → 메인 화면) ────────────────────────
    def go_back(e):
        from view.select_equipment_view import select_equipment_view
        page.clean()
        page.add(select_equipment_view(page))

    # ── 전체 레이아웃 조립 ─────────────────────────────────────────────────
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
                            "시뮬레이션 결과 조회",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                    spacing=4,
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_800),
                ft.Column(
                    [
                        header,
                        potential_section,
                        usage_section,
                        total_section,
                    ],
                    spacing=12,
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