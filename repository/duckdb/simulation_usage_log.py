from repository.interfaces import SimulationUsageLogRepository, SimulationResultRepository
from repository.duckdb.connection import get_connection

class DuckDBSimulationUsageLogRepository(SimulationUsageLogRepository):
    def log_item_usage(self, user_equipment_id: int, item_id: int) -> None:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO simulation_usage_log (user_equipment_id, item_id, use_count)
                VALUES (?, ?, 1)
                ON CONFLICT (user_equipment_id, item_id)
                DO UPDATE SET use_count = simulation_usage_log.use_count + 1
            """, [user_equipment_id, item_id])

    def get_usage_logs(self, user_equipment_id: int) -> list:
        with get_connection() as conn:
            return conn.execute("""
                SELECT im.item_name, im.item_type, sl.use_count,
                       im.price, (sl.use_count * im.price) AS total_cost
                FROM simulation_usage_log sl
                JOIN item_master im ON sl.item_id = im.item_id
                WHERE sl.user_equipment_id = ?
                ORDER BY im.item_type, im.item_id
            """, [user_equipment_id]).fetchall()

class DuckDBSimulationResultRepository(SimulationResultRepository):
    def get_simulation_result(self, user_equipment_id: int) -> dict:
        with get_connection() as conn:
            # 1. 장비 기본 정보
            eq_row = conn.execute("""
                SELECT m.equipment_name, u.bonus_str, u.bonus_attack,
                       u.upgrade_slot_left, u.potential_grade
                FROM user_equipment u
                JOIN equipment_master m ON u.equipment_id = m.equipment_id
                WHERE u.user_equipment_id = ?
            """, [user_equipment_id]).fetchone()

            if not eq_row:
                return {}

            equipment_name, bonus_str, bonus_attack, slot_left, grade = eq_row

            # 2. 잠재능력 3줄
            effects = conn.execute("""
                SELECT p.option_effect
                FROM equipment_potential ep
                JOIN potential_option_pool p ON ep.option_id = p.option_id
                WHERE ep.user_equipment_id = ?
                ORDER BY ep.line_no
            """, [user_equipment_id]).fetchall()
            potential_effects = [row[0] for row in effects]

            # 3. 사용 기록 (주문서 + 큐브)
            logs = conn.execute("""
                SELECT im.item_name, im.item_type, sl.use_count,
                       im.price, (sl.use_count * im.price) AS total_cost
                FROM simulation_usage_log sl
                JOIN item_master im ON sl.item_id = im.item_id
                WHERE sl.user_equipment_id = ?
                ORDER BY im.item_type, im.item_id
            """, [user_equipment_id]).fetchall()

            # 4. 총 사용 메소
            total_row = conn.execute("""
                SELECT COALESCE(SUM(sl.use_count * im.price), 0)
                FROM simulation_usage_log sl
                JOIN item_master im ON sl.item_id = im.item_id
                WHERE sl.user_equipment_id = ?
            """, [user_equipment_id]).fetchone()
            total_meso = int(total_row[0]) if total_row else 0

        return {
            "equipment_name": equipment_name,
            "bonus_str": bonus_str or 0,
            "bonus_attack": bonus_attack or 0,
            "upgrade_slot_left": slot_left,
            "potential_grade": grade,
            "potential_effects": potential_effects,
            "usage_logs": logs,
            "total_meso": total_meso,
        }
