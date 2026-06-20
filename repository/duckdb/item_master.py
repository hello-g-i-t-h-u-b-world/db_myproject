from repository.interfaces import ItemMasterRepository
from repository.duckdb.connection import get_connection
from typing import List, Tuple

class DuckDBItemMasterRepository(ItemMasterRepository):
    def get_item_by_id(self, item_id: int) -> Tuple[str, str, int]:
        """아이템 정보를 조회합니다."""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT item_name, item_type, price
                FROM item_master
                WHERE item_id = ?
            """, [item_id]).fetchone()
            return row if row else None

    def get_items_by_type(self, item_type: str) -> List[Tuple[int, str, int]]:
        """아이템 타입별 아이템을 조회합니다."""
        with get_connection() as conn:
            return conn.execute("""
                SELECT item_id, item_name, price
                FROM item_master
                WHERE item_type = ?
                ORDER BY item_id
            """, [item_type]).fetchall()

    def get_image_path(self, item_id: int) -> str | None:
        """아이템 이미지 경로를 조회합니다."""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT image_path FROM item_master WHERE item_id = ?
            """, [item_id]).fetchone()
            return row[0] if row else None
