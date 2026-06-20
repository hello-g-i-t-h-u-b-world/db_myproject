from repository.interfaces import UserEquipmentRepository
from repository.duckdb.connection import get_connection
from typing import Tuple, Any

class DuckDBUserEquipmentRepository(UserEquipmentRepository):
    def insert(self, equipment_id: int, initial_grade: str = "Rare") -> int:
        with get_connection() as conn:
            # DuckDB 시퀀스 대용 MAX+1 처리
            max_id_row = conn.execute("SELECT COALESCE(MAX(user_equipment_id), 0) + 1 FROM user_equipment").fetchone()
            new_id = max_id_row[0]

            # 스키마 컬럼 정합성 반영 (current_stat=0, upgrade_slot_left=7 기본 세팅)
            conn.execute("""
                INSERT INTO user_equipment
                (user_equipment_id, equipment_id, current_stat, upgrade_slot_left, potential_grade)
                VALUES (?, ?, 0, 7, ?)
            """, [new_id, equipment_id, initial_grade])
            return new_id

    def get_equipment_type(self, user_equipment_id: int) -> str:
        with get_connection() as conn:
            row = conn.execute("""
                SELECT m.equipment_type
                FROM user_equipment u
                JOIN equipment_master m ON u.equipment_id = m.equipment_id
                WHERE u.user_equipment_id = ?
            """, [user_equipment_id]).fetchone()
            return row[0] if row else None

    def get_details(self, user_equipment_id: int) -> Tuple[str, str, str]:
        with get_connection() as conn:
            row = conn.execute("""
                SELECT m.equipment_name, u.potential_grade, m.equipment_type
                FROM user_equipment u
                JOIN equipment_master m ON u.equipment_id = m.equipment_id
                WHERE u.user_equipment_id = ?
            """, [user_equipment_id]).fetchone()
            return row if row else ("Unknown", "Rare", "무기")

    def update_grade(self, user_equipment_id: int, new_grade: str) -> None:
        with get_connection() as conn:
            conn.execute("""
                UPDATE user_equipment
                SET potential_grade = ?
                WHERE user_equipment_id = ?
            """, [new_grade, user_equipment_id])

    def get_equipment_id(self, user_equipment_id: int) -> int:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT equipment_id FROM user_equipment WHERE user_equipment_id = ?",
                [user_equipment_id]
            ).fetchone()
        return row[0] if row else 0

    def get_all_user_equipments(self) -> list[dict]:
        """모든 유저 장비를 조회합니다."""
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT
                    u.user_equipment_id,
                    u.equipment_id,
                    m.equipment_name,
                    m.equipment_type,
                    u.potential_grade,
                    u.bonus_str,
                    u.bonus_attack,
                    u.upgrade_slot_left
                FROM user_equipment u
                JOIN equipment_master m ON u.equipment_id = m.equipment_id
                ORDER BY u.user_equipment_id DESC
            """).fetchall()

        return [
            {
                "user_equipment_id": r[0],
                "equipment_id": r[1],
                "equipment_name": r[2],
                "equipment_type": r[3],
                "potential_grade": r[4],
                "bonus_str": r[5] or 0,
                "bonus_attack": r[6] or 0,
                "upgrade_slot_left": r[7],
            }
            for r in rows
        ]
