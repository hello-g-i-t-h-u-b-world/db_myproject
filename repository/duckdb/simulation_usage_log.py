# repository/duckdb/simulation_usage_log.py
from repository.duckdb.connection import get_connection


class DuckDBSimulationUsageLogRepository:
    def log_item_usage(self, user_equipment_id: int, item_id: int) -> None:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO simulation_usage_log (user_equipment_id, item_id, use_count)
                VALUES (?, ?, 1)
                ON CONFLICT (user_equipment_id, item_id)
                DO UPDATE SET use_count = use_count + 1
            """, [user_equipment_id, item_id])

    def get_logs(self, user_equipment_id: int):
        with get_connection() as conn:
            return conn.execute("""
                SELECT item_id, use_count
                FROM simulation_usage_log
                WHERE user_equipment_id = ?
            """, [user_equipment_id]).fetchall()


class DuckDBSimulationResultRepository:
    def get_simulation_result(self, user_equipment_id: int) -> dict:
        return get_full_equipment_data(user_equipment_id)




def get_full_equipment_data(user_equipment_id: int) -> dict:
    """
    equipment_master, user_equipment, equipment_potential, potential_option_pool
    4개 테이블을 JOIN하여 장비 전체 데이터를 반환합니다.

    JOIN 결과:
    - user_equipment가 1행이고 equipment_potential이 3행이면
        아래 rows는 3행으로 반환됩니다.
    - 첫 번째 행에서 공통 정보(장비명, 등급 등)를 꺼내고,
        전체 행을 순회하면서 잠재능력 텍스트만 모읍니다.

    반환 예시:
    {
        "equipment_name": "하프 이어링",
        "equipment_type": "귀고리",
        "potential_grade": "Epic",
        "bonus_str": 4,
        "bonus_attack": 0,
        "upgrade_slot_left": 4,
        "potential_effects": ["STR +6%", "LUK +3%", "올스탯 +3%"],
    }
    """
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                m.equipment_name,
                m.equipment_type,
                u.potential_grade,
                u.bonus_str,
                u.bonus_attack,
                u.upgrade_slot_left,
                ep.line_no,
                p.option_effect

            FROM user_equipment u
            JOIN equipment_master m
                ON u.equipment_id = m.equipment_id
            LEFT JOIN equipment_potential ep
                ON u.user_equipment_id = ep.user_equipment_id
            LEFT JOIN potential_option_pool p
                ON ep.option_id = p.option_id

            WHERE u.user_equipment_id = ?
            ORDER BY ep.line_no
        """, [user_equipment_id]).fetchall()

    if not rows:
        return {}

    # 첫 번째 행에서 장비 공통 정보 추출
    first = rows[0]
    result = {
        "equipment_name":    first[0],
        "equipment_type":    first[1],
        "potential_grade":   first[2],
        "bonus_str":         first[3] or 0,
        "bonus_attack":      first[4] or 0,
        "upgrade_slot_left": first[5],
        "potential_effects": [row[7] for row in rows if row[7] is not None],
    }

    # 사용 기록 + 총 메소 계산
    with get_connection() as conn:
        log_rows = conn.execute("""
            SELECT
                i.item_name,
                i.item_type,
                l.use_count,
                i.price          AS unit_price,
                l.use_count * i.price AS total_cost
            FROM simulation_usage_log l
            JOIN item_master i ON l.item_id = i.item_id
            WHERE l.user_equipment_id = ?
            ORDER BY l.item_id
        """, [user_equipment_id]).fetchall()

    result["usage_logs"] = log_rows
    result["total_meso"] = sum(row[4] for row in log_rows)

    return result