# service/potential_service.py
import random
from repository import equipment_potential_repo, user_equipment_repo, cube_upgrade_repo


def roll_option(options: list) -> int:
    option_ids = [row[0] for row in options]
    weights = [row[1] for row in options]
    return random.choices(option_ids, weights=weights, k=1)[0]


def get_option_pool(equipment_type: str, grade: str, line_no: int) -> list:
    return equipment_potential_repo.get_option_pool_with_prob(equipment_type, grade, line_no)


def generate_potential(equipment_type: str, grade: str) -> list[int]:
    line1 = roll_option(get_option_pool(equipment_type, grade, 1))
    line2 = roll_option(get_option_pool(equipment_type, grade, 2))
    line3 = roll_option(get_option_pool(equipment_type, grade, 3))
    return [line1, line2, line3]


def generate_potential_for_equipment(user_equipment_id: int, grade: str) -> None:
    equipment_type = user_equipment_repo.get_equipment_type(user_equipment_id)
    options = generate_potential(equipment_type, grade)
    equipment_potential_repo.delete_potentials(user_equipment_id)
    for line_no, option_id in enumerate(options, start=1):
        equipment_potential_repo.insert_potential(user_equipment_id, line_no, option_id)


# ============================================================
# 시뮬레이터 UI 연동 서비스 로직
# ============================================================

def get_equipment_details(user_equipment_id: int) -> tuple[str, str]:
    """장비 이름과 현재 잠재 등급을 반환합니다."""
    name, grade, _ = user_equipment_repo.get_details(user_equipment_id)
    return name, grade


def get_current_potential_effects(user_equipment_id: int) -> list[str]:
    """현재 장비의 잠재능력 효과 텍스트 3줄을 반환합니다."""
    return equipment_potential_repo.get_current_potential_effects(user_equipment_id)


_GRADE_UP = {'Rare': 'Epic', 'Epic': 'Unique'}


def use_cube(user_equipment_id: int, item_id: int = 201) -> tuple[str, bool]:
    """
    큐브를 사용하고 등급 상승 여부를 판정한 뒤 새 잠재능력을 부여합니다.
    사용 기록은 simulation_usage_log에 자동 저장됩니다.
    """
    from service.stats_service import log_item_usage

    name, current_grade, equipment_type = user_equipment_repo.get_details(user_equipment_id)
    next_grade = current_grade
    is_tiered_up = False

    tier_up_rate = cube_upgrade_repo.get_upgrade_prob(item_id, current_grade)
    if tier_up_rate > 0 and random.random() < tier_up_rate:
        next_grade = _GRADE_UP[current_grade]
        is_tiered_up = True
        user_equipment_repo.update_grade(user_equipment_id, next_grade)

    generate_potential_for_equipment(user_equipment_id, next_grade)

    # 사용 로그 기록
    log_item_usage(user_equipment_id, item_id)

    return next_grade, is_tiered_up


def get_equipment_image_id(user_equipment_id: int) -> int:
    """user_equipment_id로 equipment_id(이미지 파일명 번호)를 반환합니다."""
    return user_equipment_repo.get_equipment_id(user_equipment_id)
