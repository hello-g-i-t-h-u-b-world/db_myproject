from repository.interfaces import PotentialOptionPoolRepository
from repository.duckdb.connection import get_connection
from typing import List, Tuple

class DuckDBPotentialOptionPoolRepository(PotentialOptionPoolRepository):
    def get_option_by_id(self, option_id: int) -> Tuple[int, str, str]:
        """option_id로 옵션 정보를 조회합니다."""
        with get_connection() as conn:
            row = conn.execute("""
                SELECT option_id, grade, option_effect
                FROM potential_option_pool
                WHERE option_id = ?
            """, [option_id]).fetchone()
            return row if row else None

    def get_options_by_grade(self, grade: str) -> List[Tuple[int, str]]:
        """등급별 모든 옵션을 조회합니다."""
        with get_connection() as conn:
            return conn.execute("""
                SELECT option_id, option_effect
                FROM potential_option_pool
                WHERE grade = ?
                ORDER BY option_id
            """, [grade]).fetchall()
