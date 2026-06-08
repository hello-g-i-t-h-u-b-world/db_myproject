from repository.interfaces import ScrollDetailRepository
from repository.duckdb.connection import get_connection
from typing import List, Tuple

class DuckDBScrollDetailRepository(ScrollDetailRepository):
    def get_all_scrolls(self) -> List[Tuple[int, str, float, int, int, int]]:
        """일반 주문서 목록을 반환합니다."""
        with get_connection() as conn:
            return conn.execute("""
                SELECT m.item_id, m.item_name, d.success_rate, d.add_str, d.add_attack, m.price
                FROM item_master m
                JOIN scroll_detail d ON m.item_id = d.item_id
                WHERE m.item_type = '주문서'
                ORDER BY m.item_id
            """).fetchall()

    def get_equipment_scroll_status(self, user_equipment_id: int) -> Tuple[int, int, int]:
        """장비의 주문서 강화 상태를 반환합니다."""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT bonus_str, bonus_attack, upgrade_slot_left
                FROM user_equipment
                WHERE user_equipment_id = ?
            """, [user_equipment_id]).fetchone()
            return row if row else (0, 0, 7)

    def update_equipment_scroll_status(self, user_equipment_id: int, bonus_str: int, bonus_attack: int, upgrade_slot_left: int) -> None:
        """장비의 주문서 강화 상태를 업데이트합니다."""
        with get_connection() as conn:
            conn.execute("""
                UPDATE user_equipment
                SET bonus_str = ?, bonus_attack = ?, upgrade_slot_left = ?
                WHERE user_equipment_id = ?
            """, [bonus_str, bonus_attack, upgrade_slot_left, user_equipment_id])

    def get_scroll_info_by_id(self, item_id: int) -> Tuple[str, float, int, int]:
        """주문서 정보(이름, 성공율, add_str, add_attack)를 조회합니다."""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT m.item_name, d.success_rate, d.add_str, d.add_attack
                FROM item_master m
                JOIN scroll_detail d ON m.item_id = d.item_id
                WHERE m.item_id = ?
            """, [item_id]).fetchone()
            return row if row else None
