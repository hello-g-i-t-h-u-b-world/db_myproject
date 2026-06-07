from repository.interfaces import ScrollDetailRepository
from repository.duckdb.connection import get_connection
from typing import List, Tuple

class DuckDBScrollDetailRepository(ScrollDetailRepository):
    def get_all_scrolls(self) -> List[Tuple[int, str, float, int, int, int]]:
        """모든 주문서 목록(아이템ID, 이름, 성공확률, 추가STR, 추가공격력, 가격)을 가져옵니다."""
        with get_connection() as conn:
            return conn.execute("""
                SELECT im.item_id, im.item_name, sd.success_rate, sd.add_str, sd.add_attack, im.price
                FROM item_master im
                JOIN scroll_detail sd ON im.item_id = sd.item_id
                WHERE im.item_type = '주문서'
                ORDER BY im.item_id
            """).fetchall()

    def get_scroll_by_id(self, item_id: int) -> Tuple[str, float, int, int]:
        """특정 주문서의 상세 정보(이름, 성공확률, 추가STR, 추가공격력)를 가져옵니다."""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT im.item_name, sd.success_rate, sd.add_str, sd.add_attack
                FROM item_master im
                JOIN scroll_detail sd ON im.item_id = sd.item_id
                WHERE im.item_id = ?
            """, [item_id]).fetchone()
            return row if row else ("Unknown Scroll", 0.0, 0, 0)

    def get_equipment_scroll_status(self, user_equipment_id: int) -> Tuple[int, int, int]:
        """장비의 현재 주문서 강화 상태(bonus_str, bonus_attack, upgrade_slot_left)를 조회합니다."""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT bonus_str, bonus_attack, upgrade_slot_left
                FROM user_equipment
                WHERE user_equipment_id = ?
            """, [user_equipment_id]).fetchone()
            # 데이터가 없을 경우 기본값(STR 0, 공 0, 슬롯 7) 반환
            return row if row else (0, 0, 7)

    def update_equipment_scroll_status(self, user_equipment_id: int, bonus_str: int, bonus_attack: int, upgrade_slot_left: int) -> None:
        """장비의 주문서 강화 스탯 및 남은 슬롯 상태를 DB에 저장합니다."""
        with get_connection() as conn:
            conn.execute("""
                UPDATE user_equipment
                SET bonus_str = ?, bonus_attack = ?, upgrade_slot_left = ?
                WHERE user_equipment_id = ?
            """, [bonus_str, bonus_attack, upgrade_slot_left, user_equipment_id])