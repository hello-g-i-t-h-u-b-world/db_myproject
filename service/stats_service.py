# service/stats_service.py
from repository import simulation_usage_log_repo, simulation_result_repo


def log_item_usage(user_equipment_id: int, item_id: int) -> None:
    """아이템 사용 횟수를 simulation_usage_log에 기록(없으면 INSERT, 있으면 UPDATE)합니다."""
    simulation_usage_log_repo.log_item_usage(user_equipment_id, item_id)


def get_simulation_result(user_equipment_id: int) -> dict:
    """
    시뮬레이션 결과 화면에 필요한 모든 데이터를 조회합니다.

    반환 구조:
    {
        "equipment_name": str,
        "bonus_str": int,
        "bonus_attack": int,
        "upgrade_slot_left": int,
        "potential_grade": str,
        "potential_effects": [str, str, str],
        "usage_logs": [(item_name, item_type, use_count, unit_price, total_cost), ...],
        "total_meso": int,
    }
    """
    return simulation_result_repo.get_simulation_result(user_equipment_id)
