from repository.interfaces import CubeUpgradeProbRepository
from repository.duckdb.connection import get_connection

class DuckDBCubeUpgradeProbRepository(CubeUpgradeProbRepository):
    def get_upgrade_prob(self, item_id: int, current_grade: str) -> float:
        """큐브의 등급 상승 확률을 반환합니다. 해당 행이 없으면 0.0을 반환합니다."""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT tier_up_rate
                FROM cube_upgrade_prob
                WHERE item_id = ? AND current_grade = ?
            """, [item_id, current_grade]).fetchone()
            return row[0] if row else 0.0
