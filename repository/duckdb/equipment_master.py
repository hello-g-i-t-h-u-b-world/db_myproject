from repository.interfaces import EquipmentMasterRepository
from repository.duckdb.connection import get_connection
from typing import List, Tuple

class DuckDBEquipmentMasterRepository(EquipmentMasterRepository):
    def get_all(self) -> List[Tuple[int, str, str]]:
        with get_connection() as conn:
            return conn.execute("""
                SELECT equipment_id, equipment_name, equipment_type 
                FROM equipment_master
            """).fetchall()