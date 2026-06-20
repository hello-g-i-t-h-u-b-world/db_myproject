from repository import user_equipment_repo, equipment_master_repo, item_master_repo
from service.potential_service import generate_potential_for_equipment

def create_user_equipment(equipment_id):
    # 유저 장비 기본 테이블 인서트 후 고유 ID 반환 받기
    new_user_eq_id = user_equipment_repo.insert(equipment_id, "Rare")

    # 생성된 장비에 첫 기본 잠재옵션(Rare 등급) 부여
    generate_potential_for_equipment(new_user_eq_id, "Rare")

    return new_user_eq_id


def get_equipment_image_path(equipment_id: int) -> str | None:
    """장비 이미지 경로를 DB에서 조회합니다."""
    return equipment_master_repo.get_image_path(equipment_id)


def get_item_image_path(item_id: int) -> str | None:
    """아이템(주문서/큐브) 이미지 경로를 DB에서 조회합니다."""
    return item_master_repo.get_image_path(item_id)