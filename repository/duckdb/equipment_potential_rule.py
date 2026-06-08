from repository.interfaces import EquipmentPotentialRuleRepository
from repository.duckdb.connection import get_connection
from typing import List

class DuckDBEquipmentPotentialRuleRepository(EquipmentPotentialRuleRepository):
    def get_valid_options_for_equipment(self, equipment_type: str) -> List[int]:
        """장비 타입에 유효한 옵션 ID 목록을 조회합니다."""
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT option_id
                FROM equipment_potential_rule
                WHERE equipment_type = ?
                ORDER BY option_id
            """, [equipment_type]).fetchall()
            return [row[0] for row in rows]
