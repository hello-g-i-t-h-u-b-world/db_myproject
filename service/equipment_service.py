from repository import user_equipment_repo
from service.potential_service import generate_potential_for_equipment

def create_user_equipment(equipment_id):
    # 유저 장비 기본 테이블 인서트 후 고유 ID 반환 받기
    new_user_eq_id = user_equipment_repo.insert(equipment_id, "Rare")
    
    # 생성된 장비에 첫 기본 잠재옵션(Rare 등급) 부여
    generate_potential_for_equipment(new_user_eq_id, "Rare")
    
    return new_user_eq_id