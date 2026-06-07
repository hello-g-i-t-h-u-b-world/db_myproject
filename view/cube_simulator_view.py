# view/cube_simulator_view.py
import flet as ft
from service.potential_service import use_cube, get_equipment_details, get_current_potential_effects
from service.scroll_service import get_available_scrolls, get_equipment_scroll_status, use_scroll

def cube_simulator_view(page: ft.Page, user_equipment_id: int):
    GRADE_COLORS = {
        "Rare": ft.Colors.BLUE_400,
        "Epic": ft.Colors.PURPLE_400,
        "Unique": ft.Colors.AMBER_500
    }

    # --- 공통 상단 헤더 컴포넌트 ---
    title_text = ft.Text(size=24, weight=ft.FontWeight.BOLD)
    grade_text = ft.Text(size=18, weight=ft.FontWeight.BOLD)
    stats_text = ft.Text(size=15, color=ft.Colors.GREY_400)
    slots_text = ft.Text(size=15, weight=ft.FontWeight.W_600)
    
    # --- 탭 1: 큐브 컴포넌트 ---
    potential_lines = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    
    # --- 탭 2: 주문서 컴포넌트 ---
    scroll_dropdown = ft.Dropdown(width=320, label="강화에 사용할 주문서 선택")

    # DB의 주문서 데이터를 드롭다운에 채워넣기
    scrolls = get_available_scrolls()
    for sid, sname, srate, sstr, satt, sprice in scrolls:
        scroll_dropdown.options.append(
            ft.dropdown.Option(key=str(sid), text=f"{sname} ({int(srate*100)}%)")
        )
    if scrolls:
        scroll_dropdown.value = str(scrolls[0][0])  # 기본값 첫 번째 주문서 지정

    # --- 통합 UI 갱신 함수 ---
    def refresh_ui(can_update=True):
        # 1. 백엔드 서비스로부터 최신 정보 동기화
        eq_name, current_grade = get_equipment_details(user_equipment_id)
        effects = get_current_potential_effects(user_equipment_id)
        b_str, b_attack, s_left = get_equipment_scroll_status(user_equipment_id)
        
        # 2. 공통 스탯 헤더 갱신
        title_text.value = eq_name
        grade_text.value = f"[{current_grade}]"
        grade_text.color = GRADE_COLORS.get(current_grade, ft.Colors.WHITE)
        stats_text.value = f"추가 스탯: STR +{b_str} | 공격력 +{b_attack}"
        
        slots_text.value = f"남은 업그레이드 가능 횟수: {s_left}회"
        if s_left == 0:
            slots_text.color = ft.Colors.RED_400
            scroll_button.disabled = True
        else:
            slots_text.color = ft.Colors.GREEN_400
            scroll_button.disabled = False
            
        # 3. 큐브 잠재능력 3줄 갱신
        potential_lines.controls.clear()
        for i, effect in enumerate(effects, start=1):
            potential_lines.controls.append(
                ft.Container(
                    content=ft.Text(f"줄 {i}: {effect}", size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
                    bgcolor=ft.Colors.GREY_900,
                    padding=12,
                    border_radius=8,
                    alignment=ft.Alignment.CENTER_LEFT
                )
            )
        
        if can_update:
            page.update()

    # --- 큐브 사용 클릭 이벤트 ---
    def on_cube_click(e):
        cube_button.disabled = True
        page.update()
        
        next_grade, is_tiered_up = use_cube(user_equipment_id)
        refresh_ui(can_update=False)
        
        if is_tiered_up:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"🎉 등급 상승!! -> [{next_grade}]", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.AMBER_400
            )
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("큐브 조율 완료."))
            page.snack_bar.open = True
            
        cube_button.disabled = False
        page.update()

    # --- 주문서 사용 클릭 이벤트 ---
    def on_scroll_click(e):
        if not scroll_dropdown.value:
            return
            
        scroll_button.disabled = True
        page.update()
        
        selected_item_id = int(scroll_dropdown.value)
        success, result_msg = use_scroll(user_equipment_id, selected_item_id)
        
        # UI 지표 실시간 갱신
        refresh_ui(can_update=False)
        
        # 성공/실패 여부에 따라 다른 색상의 스낵바 알림 제공
        page.snack_bar = ft.SnackBar(
            content=ft.Text(result_msg, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.GREEN_700 if success else ft.Colors.RED_700
        )
        page.snack_bar.open = True
        
        scroll_button.disabled = False
        page.update()

    # --- 컴포넌트 선언 배치 ---
    # 최신 Flet 스펙에 맞추어 content 내부 구조로 정의했습니다.
    cube_button = ft.Button(
        content=ft.Row([
            ft.Icon(ft.Icons.REPLAY_CIRCLE_FILLED_OUTLINED, color=ft.Colors.WHITE),
            ft.Text("미라클 큐브 사용", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=16),
        ], alignment=ft.MainAxisAlignment.CENTER, tight=True),
        bgcolor=ft.Colors.RED_ACCENT_400,
        on_click=on_cube_click,
        height=50,
    )

    scroll_button = ft.Button(
        content=ft.Row([
            ft.Icon(ft.Icons.FLASHLIGHT_ON, color=ft.Colors.WHITE),
            ft.Text("주문서 사용 (작하기)", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=16),
        ], alignment=ft.MainAxisAlignment.CENTER, tight=True),
        bgcolor=ft.Colors.BLUE_ACCENT_400,
        on_click=on_scroll_click,
        height=50,
    )

    def go_back(e):
        from view.select_equipment_view import select_equipment_view
        page.clean()
        page.add(select_equipment_view(page))

    # 데이터 초기 세팅
    refresh_ui(can_update=False)

    # --- 레이아웃 조립 ---
    cube_tab_content = ft.Container(
        content=ft.Column([
            ft.Text("장비 잠재능력", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300),
            potential_lines,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            cube_button
        ], spacing=15),
        padding=15
    )

    scroll_tab_content = ft.Container(
        content=ft.Column([
            ft.Text("상점 주문서 강화", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300),
            scroll_dropdown,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            scroll_button
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=15
    )

    # 본문 영역 컨테이너 (초기값: 큐브 돌리기 화면)
    tab_content_container = ft.Container(content=cube_tab_content, expand=True)

    # 💡 [핵심 교정] 에러가 원천 불가능한 Container 탭바 구조 설계
    # Flet 버전 패치에 영향받는 text 인자를 완전히 배제했습니다.
    cube_tab_text = ft.Text("큐브 돌리기", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    scroll_tab_text = ft.Text("주문서 작하기", color=ft.Colors.GREY_400, weight=ft.FontWeight.NORMAL)

    tab_cube_btn = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.LAYERS, color=ft.Colors.WHITE), cube_tab_text], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=ft.Colors.GREY_800,
        padding=12,
        border_radius=8,
        expand=True,
    )
    
    tab_scroll_btn = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.FLASHLIGHT_ON, color=ft.Colors.GREY_400), scroll_tab_text], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=ft.Colors.GREY_900,
        padding=12,
        border_radius=8,
        expand=True,
    )

    def switch_to_cube(e):
        tab_cube_btn.bgcolor = ft.Colors.GREY_800
        tab_scroll_btn.bgcolor = ft.Colors.GREY_900
        cube_tab_text.color = ft.Colors.WHITE
        cube_tab_text.weight = ft.FontWeight.BOLD
        scroll_tab_text.color = ft.Colors.GREY_400
        scroll_tab_text.weight = ft.FontWeight.NORMAL
        tab_cube_btn.content.controls[0].color = ft.Colors.WHITE
        tab_scroll_btn.content.controls[0].color = ft.Colors.GREY_400
        tab_content_container.content = cube_tab_content
        page.update()

    def switch_to_scroll(e):
        tab_cube_btn.bgcolor = ft.Colors.GREY_900
        tab_scroll_btn.bgcolor = ft.Colors.GREY_800
        cube_tab_text.color = ft.Colors.GREY_400
        cube_tab_text.weight = ft.FontWeight.NORMAL
        scroll_tab_text.color = ft.Colors.WHITE
        scroll_tab_text.weight = ft.FontWeight.BOLD
        tab_cube_btn.content.controls[0].color = ft.Colors.GREY_400
        tab_scroll_btn.content.controls[0].color = ft.Colors.WHITE
        tab_content_container.content = scroll_tab_content
        page.update()

    tab_cube_btn.on_click = switch_to_cube
    tab_scroll_btn.on_click = switch_to_scroll

    # 커스텀 탭 바 구성
    custom_tab_bar = ft.Row(
        controls=[tab_cube_btn, tab_scroll_btn],
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER
    )

    return ft.Container(
        content=ft.Column([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back),
            ft.Container(
                content=ft.Column([
                    title_text,
                    ft.Row([grade_text, stats_text], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    slots_text,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
                alignment=ft.Alignment(0, 0),
                padding=5
            ),
            ft.Divider(height=1, color=ft.Colors.GREY_800),
            custom_tab_bar,
            tab_content_container,
        ]),
        expand=True
    )