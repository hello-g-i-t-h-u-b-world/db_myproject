from repository.interfaces import ChaosScrollDetailRepository
from repository.duckdb.connection import get_connection
from typing import List, Tuple

class DuckDBChaosScrollDetailRepository(ChaosScrollDetailRepository):
    def get_all_chaos_scrolls(self) -> List[Tuple[int, str, float, int]]:
        """모든 혼돈 주문서 목록을 반환합니다."""
        with get_connection() as conn:
            return conn.execute("""
                SELECT m.item_id, m.item_name, d.success_rate, m.price
                FROM item_master m
                JOIN chaos_scroll_detail d ON m.item_id = d.item_id
                WHERE m.item_type = '혼돈주문서'
                ORDER BY m.item_id
            """).fetchall()

    def get_chaos_scroll_info_by_id(self, item_id: int) -> Tuple[float, int, int]:
        """혼돈의 주문서 정보(성공율, min, max)를 조회합니다."""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT success_rate, chaos_min, chaos_max
                FROM chaos_scroll_detail
                WHERE item_id = ?
            """, [item_id]).fetchone()
            return row if row else None
