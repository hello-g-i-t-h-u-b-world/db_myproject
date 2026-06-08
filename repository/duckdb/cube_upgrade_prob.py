from repository.interfaces import CubeUpgradeProbRepository
from repository.duckdb.connection import get_connection
from typing import Tuple

class DuckDBCubeUpgradeProbRepository(CubeUpgradeProbRepository):
    def get_upgrade_prob(self, item_id: int, current_grade: str) -> Tuple[str, float]:
        """큐브의 다음 등급과 확률을 반환합니다."""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT next_grade, tier_up_rate
                FROM cube_upgrade_prob
                WHERE item_id = ? AND current_grade = ?
            """, [item_id, current_grade]).fetchone()
            return row if row else (None, 0.0)
