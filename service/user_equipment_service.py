# service/user_equipment_service.py
from repository import user_equipment_repo


def get_all_user_equipments() -> list[dict]:
    """
    DB에 저장된 모든 유저 장비를 조회합니다.
    반환: [{ user_equipment_id, equipment_id, equipment_name, equipment_type,
    potential_grade, bonus_str, bonus_attack, upgrade_slot_left }, ...]
    """
    return user_equipment_repo.get_all_user_equipments()
