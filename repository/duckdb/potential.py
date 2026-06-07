from repository.interfaces import PotentialRepository
from repository.duckdb.connection import get_connection
from typing import List, Tuple

class DuckDBPotentialRepository(PotentialRepository):
    def get_option_pool_with_prob(self, equipment_type: str, grade: str, line_no: int) -> List[Tuple[int, float]]:
        # 등급별 안전한 option_id 범위 규칙 규칙 적용
        if grade == "Rare":
            option_range = (3001, 3015)
        elif grade == "Epic":
            option_range = (3001, 5011)
        elif grade == "Unique":
            option_range = (5001, 6011)
        else:
            raise ValueError(f"잘못된 등급입니다: {grade}")

        with get_connection() as conn:
            return conn.execute("""
                SELECT option_id, probability
                FROM potential_option_probability
                WHERE line_no = ?
                AND option_id BETWEEN ? AND ?
            """, [line_no, option_range[0], option_range[1]]).fetchall()

    # 💡 [핵심 추가] 현재 장비의 잠재능력 옵션 문자열(Effect) 리스트를 가져오는 함수
    def get_current_potential_effects(self, user_equipment_id: int) -> List[str]:
        with get_connection() as conn:
            # 장비 잠재능력 테이블과 옵션 마스터(풀) 테이블을 JOIN하여 효과 텍스트를 정렬해 가져옵니다.
            rows = conn.execute("""
                SELECT p.option_effect
                FROM equipment_potential ep
                JOIN potential_option_pool p ON ep.option_id = p.option_id
                WHERE ep.user_equipment_id = ?
                ORDER BY ep.line_no
            """, [user_equipment_id]).fetchall()
            
            # 튜플 리스트 [('STR +6%',), ('DEX +3%',)]를 문자열 리스트 ['STR +6%', 'DEX +3%']로 변환
            return [row[0] for row in rows]

    def delete_potentials(self, user_equipment_id: int) -> None:
        with get_connection() as conn:
            conn.execute("DELETE FROM equipment_potential WHERE user_equipment_id = ?", [user_equipment_id])

    def insert_potential(self, user_equipment_id: int, line_no: int, option_id: int) -> None:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO equipment_potential (user_equipment_id, line_no, option_id)
                VALUES (?, ?, ?)
            """, [user_equipment_id, line_no, option_id])