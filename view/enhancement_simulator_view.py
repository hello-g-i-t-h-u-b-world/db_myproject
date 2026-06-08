import flet as ft
from service.potential_service import use_cube, get_equipment_details, get_current_potential_effects, get_equipment_image_id
from service.scroll_service import get_available_scrolls, get_equipment_scroll_status, use_scroll


def cube_simulator_view(page: ft.Page, user_equipment_id: int) -> ft.Container:
    # 장비 이미지 (assets/{equipment_id}.png)
    eq_image_id = get_equipment_image_id(user_equipment_id)

    equipment_image = ft.Image(src=f"{eq_image_id}.png", width=80, height=80)


    GRADE_COLORS = {
        "Rare": ft.Colors.BLUE_400,
        "Epic": ft.Colors.PURPLE_400,
        "Unique": ft.Colors.AMBER_500,
    }

    # ── 공통 헤더 컴포넌트 ────────────────────────────────────────────────
    title_text = ft.Text(size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
    grade_text = ft.Text(size=16, weight=ft.FontWeight.BOLD)
    stats_text = ft.Text(size=13, color=ft.Colors.GREY_400)
    slots_text = ft.Text(size=13, weight=ft.FontWeight.W_600)

    # ── 탭 1: 큐브 컴포넌트 ──────────────────────────────────────────────
    potential_lines = ft.Column(spacing=8, alignment=ft.MainAxisAlignment.CENTER)

    # ── 탭 2: 주문서 컴포넌트 ────────────────────────────────────────────
    scrolls = get_available_scrolls()
    # 현재 선택된 주문서 ID (첫 번째가 기본 선택)
    selected_scroll_id: list[int | None] = [scrolls[0][0] if scrolls else None]

    # ── 통합 UI 갱신 함수 ─────────────────────────────────────────────────
    def refresh_ui(can_update: bool = True) -> None:
        eq_name, current_grade = get_equipment_details(user_equipment_id)
        effects = get_current_potential_effects(user_equipment_id)
        b_str, b_attack, s_left = get_equipment_scroll_status(user_equipment_id)

        title_text.value = eq_name
        grade_text.value = f"[ {current_grade} ]"
        grade_text.color = GRADE_COLORS.get(current_grade, ft.Colors.WHITE)
        stats_text.value = f"STR +{b_str} | 공격력 +{b_attack}"
        slots_text.value = f"남은 업그레이드 가능 횟수: {s_left}회"

        if s_left == 0:
            slots_text.color = ft.Colors.RED_400
            scroll_button.disabled = True
        else:
            slots_text.color = ft.Colors.GREEN_400
            scroll_button.disabled = False

        # 등급별 외곽 테두리 색
        BORDER_COLOR = {
            "Rare":   ft.Colors.BLUE_400,
            "Epic":   ft.Colors.PURPLE_400,
            "Unique": ft.Colors.AMBER_500,
        }
        border_color = BORDER_COLOR.get(current_grade, ft.Colors.GREY_700)

        # 줄 1~3을 개별 컨테이너로 쌓고, 전체를 테두리 박스 하나로 감싼다
        line_rows = []
        for i, effect in enumerate(effects, start=1):
            line_rows.append(
                ft.Text(
                    f"줄 {i}: {effect}",
                    size=15,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.W_500,
                )
            )
            if i < len(effects):
                line_rows.append(
                    ft.Divider(height=1, color=ft.Colors.GREY_800)
                )

        potential_lines.controls.clear()
        potential_lines.controls.append(
            ft.Container(
                content=ft.Column(line_rows, spacing=10),
                bgcolor=ft.Colors.GREY_900,
                padding=14,
                border_radius=10,
                border=ft.Border(
                    left=ft.BorderSide(2, border_color),
                    right=ft.BorderSide(2, border_color),
                    top=ft.BorderSide(2, border_color),
                    bottom=ft.BorderSide(2, border_color),
                ),
            )
        )

        if can_update:
            page.update()

    # ── 큐브 사용 이벤트 ─────────────────────────────────────────────────
    def on_cube_click(e) -> None:
        cube_button.disabled = True
        page.update()

        next_grade, is_tiered_up = use_cube(user_equipment_id)
        refresh_ui(can_update=False)

        if is_tiered_up:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    f"🎉 등급 상승!! → [ {next_grade} ]",
                    color=ft.Colors.BLACK,
                    weight=ft.FontWeight.BOLD,
                ),
                bgcolor=ft.Colors.AMBER_400,
            )
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("큐브 조율 완료.", color=ft.Colors.WHITE)
            )
        page.snack_bar.open = True
        cube_button.disabled = False
        page.update()

    # ── 주문서 사용 이벤트 ───────────────────────────────────────────────
    def on_scroll_click(e) -> None:
        if selected_scroll_id[0] is None:
            return

        scroll_button.disabled = True
        page.update()

        selected_item_id = selected_scroll_id[0]
        success, result_msg = use_scroll(user_equipment_id, selected_item_id)
        refresh_ui(can_update=False)

        page.snack_bar = ft.SnackBar(
            content=ft.Text(result_msg, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.GREEN_700 if success else ft.Colors.RED_700,
        )
        page.snack_bar.open = True
        scroll_button.disabled = False
        page.update()

    # ── 결과 조회 화면 이동 ──────────────────────────────────────────────
    def go_to_stats(e) -> None:
        from view.stats_view import stats_view
        page.clean()
        page.add(stats_view(page, user_equipment_id))

    # ── 버튼 선언 ─────────────────────────────────────────────────────────
    cube_button = ft.Button(
        content=ft.Row(
            [
                ft.Image(src="미라클큐브.png", width=28, height=28),
                ft.Text(
                    "미라클 큐브 사용",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    size=15,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            tight=True,
        ),
        bgcolor=ft.Colors.RED_ACCENT_400,
        on_click=on_cube_click,
        height=48,
    )

    scroll_button = ft.Button(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.FLASHLIGHT_ON, color=ft.Colors.WHITE),
                ft.Text(
                    "주문서 사용",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    size=15,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        ),
        bgcolor=ft.Colors.BLUE_ACCENT_400,
        on_click=on_scroll_click,
        height=48,
    )

    stats_button = ft.Button(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.BAR_CHART, color=ft.Colors.WHITE),
                ft.Text(
                    "시뮬레이션 결과 조회",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    size=15,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        ),
        bgcolor=ft.Colors.TEAL_700,
        on_click=go_to_stats,
        height=48,
    )

    def go_back(e) -> None:
        from view.select_equipment_view import select_equipment_view
        page.clean()
        page.add(select_equipment_view(page))

    # ── 탭 컨텐츠 ────────────────────────────────────────────────────────
    cube_tab_content = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "장비 잠재능력",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_300,
                ),
                potential_lines,
                ft.Container(height=8),
                cube_button,
            ],
            spacing=12,
        ),
        padding=14,
    )

    # ── 주문서 카드 리스트 빌드 ─────────────────────────────────────────
    def build_scroll_cards() -> ft.Column:
        cards = []

        for sid, sname, srate, sstr, satt, sprice in scrolls:
            is_selected = (sid == selected_scroll_id[0])
            stat_text = []
            if(sstr > 0):
                stat_text.append(f"STR + {sstr}")
            if(satt > 0):
                stat_text.append(f"공격력 + {satt}")
            
            stat_info = " | ".join(stat_text)

            card = ft.Container(
                content=ft.Row(
                    [
                        ft.Image(src=f"{sid}.png", width=36, height=36),
                        ft.Column(
                            [
                                ft.Text(sname, size=13, color=ft.Colors.WHITE, weight=ft.FontWeight.W_600),
                                ft.Text(
                                    f"성공률 {int(srate * 100)}%  | {stat_info} | {sprice:,} 메소",
                                    size=11,
                                    color=ft.Colors.GREY_400,
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE,
                            color=ft.Colors.TEAL_400 if is_selected else ft.Colors.TRANSPARENT,
                            size=20,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=ft.Colors.TEAL_900 if is_selected else ft.Colors.GREY_800,
                border_radius=10,
                padding=ft.Padding(left=12, right=12, top=10, bottom=10),
                border=ft.Border(
                    left=ft.BorderSide(2, ft.Colors.TEAL_400 if is_selected else ft.Colors.TRANSPARENT),
                    right=ft.BorderSide(0, ft.Colors.TRANSPARENT),
                    top=ft.BorderSide(0, ft.Colors.TRANSPARENT),
                    bottom=ft.BorderSide(0, ft.Colors.TRANSPARENT),
                ),
                on_click=lambda e, s=sid: on_scroll_selected(s),
                ink=True,
                data=sid,
            )
            cards.append(card)
        return ft.Column(cards, spacing=8)

    scroll_cards_container = ft.ListView(
        controls=[build_scroll_cards()],
        expand=True,
        spacing=0,
    )

    def on_scroll_selected(sid: int) -> None:
        selected_scroll_id[0] = sid
        scroll_cards_container.controls = [build_scroll_cards()]
        page.update()

    scroll_tab_content = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "주문서 선택",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_300,
                ),
                ft.Container(
                    content=scroll_cards_container,
                    height=200,
                ),
                ft.Container(height=4),
                scroll_button,
            ],
            spacing=12,
        ),
        padding=14,
    )

    tab_content_container = ft.Container(content=cube_tab_content, expand=True)

    # ── 커스텀 탭 바 ─────────────────────────────────────────────────────
    cube_tab_text = ft.Text("큐브 돌리기", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    scroll_tab_text = ft.Text("주문서 작하기", color=ft.Colors.GREY_400, weight=ft.FontWeight.NORMAL)

    cube_icon = ft.Icon(ft.Icons.LAYERS, color=ft.Colors.WHITE)
    scroll_icon = ft.Icon(ft.Icons.FLASHLIGHT_ON, color=ft.Colors.GREY_400)

    tab_cube_btn = ft.Container(
        content=ft.Row(
            [cube_icon, cube_tab_text],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.GREY_800,
        padding=12,
        border_radius=8,
        expand=True,
    )

    tab_scroll_btn = ft.Container(
        content=ft.Row(
            [scroll_icon, scroll_tab_text],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.GREY_900,
        padding=12,
        border_radius=8,
        expand=True,
    )

    def switch_to_cube(e) -> None:
        tab_cube_btn.bgcolor = ft.Colors.GREY_800
        tab_scroll_btn.bgcolor = ft.Colors.GREY_900
        cube_tab_text.color = ft.Colors.WHITE
        cube_tab_text.weight = ft.FontWeight.BOLD
        scroll_tab_text.color = ft.Colors.GREY_400
        scroll_tab_text.weight = ft.FontWeight.NORMAL
        cube_icon.color = ft.Colors.WHITE
        scroll_icon.color = ft.Colors.GREY_400
        tab_content_container.content = cube_tab_content
        page.update()

    def switch_to_scroll(e) -> None:
        tab_cube_btn.bgcolor = ft.Colors.GREY_900
        tab_scroll_btn.bgcolor = ft.Colors.GREY_800
        cube_tab_text.color = ft.Colors.GREY_400
        cube_tab_text.weight = ft.FontWeight.NORMAL
        scroll_tab_text.color = ft.Colors.WHITE
        scroll_tab_text.weight = ft.FontWeight.BOLD
        cube_icon.color = ft.Colors.GREY_400
        scroll_icon.color = ft.Colors.WHITE
        tab_content_container.content = scroll_tab_content
        page.update()

    tab_cube_btn.on_click = switch_to_cube
    tab_scroll_btn.on_click = switch_to_scroll

    custom_tab_bar = ft.Row(
        controls=[tab_cube_btn, tab_scroll_btn],
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # 초기 데이터 세팅
    refresh_ui(can_update=False)

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back),
                        ft.Text(
                            "강화 시뮬레이터",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                    ]
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    equipment_image,
                                    ft.Column(
                                        [
                                            title_text,
                                            ft.Row(
                                                [grade_text, stats_text],
                                                spacing=8,
                                            ),
                                            slots_text,
                                        ],
                                        spacing=2,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                ],
                                spacing=12,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    alignment=ft.Alignment(0, 0),
                    padding=6,
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_800),
                custom_tab_bar,
                tab_content_container,
                ft.Divider(height=1, color=ft.Colors.GREY_800),
                ft.Container(
                    content=stats_button,
                    padding=ft.Padding(left=14, right=14, top=8, bottom=8),
                ),
            ]
        ),
        expand=True,
    )