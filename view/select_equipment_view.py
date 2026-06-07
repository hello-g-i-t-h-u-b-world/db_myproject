# view/select_equipment_view.py
import flet as ft
from repository import equipment_master_repo
from service.equipment_service import create_user_equipment
from view.cube_simulator_view import cube_simulator_view

def select_equipment_view(page: ft.Page):
    # 💡 [레포지토리 적용] 직접 sql을 실행하지 않고 마스터 레포지토리에서 데이터를 가져옵니다.
    # get_all() 결과 구조: [(equipment_id, equipment_name, equipment_type), ...]
    equipments = equipment_master_repo.get_all()

    # 장비 선택 버튼 클릭 시 발생하는 이벤트
    def on_equipment_selected(equipment_id):
        # 💡 [서비스 레이어 적용] 
        # 이제 ID 계산, 디폴트 스탯 인서트, 최초 잠재옵션(Rare) 부여는 
        # equipment_service.py의 create_user_equipment 가 전부 알아서 처리합니다!
        user_equipment_id = create_user_equipment(equipment_id)
        
        # 화면 깨끗이 비우고 시뮬레이터 화면 뷰 배치 및 전환
        page.clean()
        page.add(cube_simulator_view(page, user_equipment_id))

    controls = []
    for equipment_id, equipment_name, equipment_type in equipments:
        controls.append(
            ft.Button(
                content=ft.Text(value=equipment_name, size=15, weight=ft.FontWeight.W_500),
                on_click=lambda e, eid=equipment_id: on_equipment_selected(eid),
                width=250,
                height=45
            )
        )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("큐브를 돌릴 장비를 선택하세요", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                *controls
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
        ),
        alignment=ft.Alignment(0, 0),
        padding=30
    )