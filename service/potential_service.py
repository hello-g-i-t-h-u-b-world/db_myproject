# service/potential_service.py
import random
from repository import potential_repo, user_equipment_repo

def roll_option(options):
    option_ids = [row[0] for row in options]
    weights = [row[1] for row in options]
    return random.choices(option_ids, weights=weights, k=1)[0]

# 옵션 풀 조회
def get_option_pool(equipment_type, grade, line_no):
    # 💡 [레포지토리 적용] potential_repo 구현체 호출
    return potential_repo.get_option_pool_with_prob(equipment_type, grade, line_no)

# 잠재능력 3줄 생성
def generate_potential(equipment_type, grade):
    line1 = roll_option(get_option_pool(equipment_type, grade, 1))
    line2 = roll_option(get_option_pool(equipment_type, grade, 2))
    line3 = roll_option(get_option_pool(equipment_type, grade, 3))
    return [line1, line2, line3]

# 특정 장비에 새로운 잠재 부여 및 DB 저장
def generate_potential_for_equipment(user_equipment_id, grade):
    # 1. 유저 장비 ID로 장비 타입('무기', '방어구' 등) 가져오기
    equipment_type = user_equipment_repo.get_equipment_type(user_equipment_id)
    
    # 2. 장비 타입과 등급에 맞는 랜덤 옵션 ID 3개 주사위 굴리기
    options = generate_potential(equipment_type, grade)

    # 3. 💡 [레포지토리 적용] 기존 잠재 기록 삭제
    potential_repo.delete_potentials(user_equipment_id)

    # 4. 💡 [레포지토리 적용] 정렬 순서(line_no)대로 새로운 잠재 데이터 삽입
    for line_no, option_id in enumerate(options, start=1):
        potential_repo.insert_potential(user_equipment_id, line_no, option_id)

# ====================================================================
# 시뮬레이터 UI 연동 서비스 로직
# ====================================================================

def get_equipment_details(user_equipment_id: int) -> tuple[str, str]:
    """유저 장비 ID로 장비 이름과 현재 잠재 등급을 조회합니다."""
    # 💡 [레포지토리 적용] user_equipment_repo.get_details는 (이름, 등급, 타입)을 줍니다.
    name, grade, _ = user_equipment_repo.get_details(user_equipment_id)
    return name, grade

def get_current_potential_effects(user_equipment_id: int) -> list[str]:
    """현재 장비가 가진 잠재능력 효과 텍스트 3줄을 가져옵니다."""
    # 💡 [레포지토리 적용] potential_repo의 구현체 함수 활용
    return potential_repo.get_current_potential_effects(user_equipment_id)

def use_cube(user_equipment_id: int, item_id: int = 2001) -> tuple[str, bool]:
    """큐브 사용 및 등업 확률 계산 후 새로운 잠재능력을 부여합니다."""
    # 1. 현재 정보 조회
    name, current_grade, equipment_type = user_equipment_repo.get_details(user_equipment_id)
    next_grade = current_grade
    is_tiered_up = False
    
    # 2. 등업 확률 테이블(cube_upgrade_prob) 조회
    # (큐브 전용 마스터 테이블은 아직 별도 레포지토리가 없으므로 내부용 connection을 사용해 직접 조회합니다)
    from repository.duckdb.connection import get_connection
    with get_connection() as conn:
        prob_row = conn.execute("""
            SELECT next_grade, tier_up_rate 
            FROM cube_upgrade_prob 
            WHERE item_id = ? AND current_grade = ?
        """, [item_id, current_grade]).fetchone()
    
    # 3. 확률 계산 및 등급 업데이트
    if prob_row:
        target_grade, tier_up_rate = prob_row[0], prob_row[1]
        if random.random() < tier_up_rate:
            next_grade = target_grade
            is_tiered_up = True
            
            # 💡 [레포지토리 적용] 등급 상승 시 레포지토리를 통해 등급 데이터 변경
            user_equipment_repo.update_grade(user_equipment_id, next_grade)
            
    # 4. 새 등급에 맞춰 옵션 재설정 및 저장
    generate_potential_for_equipment(user_equipment_id, next_grade)
    
    return next_grade, is_tiered_up