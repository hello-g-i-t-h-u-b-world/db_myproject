# service/scroll_service.py
import random
from repository.duckdb.connection import get_connection

def get_available_scrolls():
    """DB에 등록된 모든 주문서 목록을 가져옵니다."""
    with get_connection() as conn:
        return conn.execute("""
            SELECT m.item_id, m.item_name, d.success_rate, d.add_str, d.add_attack, m.price
            FROM item_master m
            JOIN scroll_detail d ON m.item_id = d.item_id
            WHERE m.item_type = '주문서'
            ORDER BY m.item_id
        """).fetchall()

def get_equipment_scroll_status(user_equipment_id: int):
    """장비의 주문서 강화 관련 현재 스탯(STR, 공격력, 남은 슬롯)을 가져옵니다."""
    with get_connection() as conn:
        row = conn.execute("""
            SELECT bonus_str, bonus_attack, upgrade_slot_left
            FROM user_equipment
            WHERE user_equipment_id = ?
        """, [user_equipment_id]).fetchone()
        return row if row else (0, 0, 7)

def use_scroll(user_equipment_id: int, item_id: int) -> tuple[bool, str]:
    """선택한 주문서를 장비에 사용하고 결과를 DB에 저장합니다. (성공여부, 메시지 반환)"""
    with get_connection() as conn:
        # 1. 장비의 현재 상태 및 남은 업그레이드 횟수 검증
        eq_row = conn.execute("""
            SELECT bonus_str, bonus_attack, upgrade_slot_left 
            FROM user_equipment 
            WHERE user_equipment_id = ?
        """, [user_equipment_id]).fetchone()
        
        if not eq_row:
            return False, "장비 정보를 찾을 수 없습니다."
            
        current_str, current_att, slots_left = eq_row
        if slots_left <= 0:
            return False, "업그레이드 가능한 횟수가 없습니다!"

        # 2. 주문서 스펙 정보 가져오기
        scroll_row = conn.execute("""
            SELECT m.item_name, d.success_rate, d.add_str, d.add_attack 
            FROM scroll_detail d
            JOIN item_master m ON d.item_id = m.item_id
            WHERE d.item_id = ?
        """, [item_id]).fetchone()
        
        if not scroll_row:
            return False, "주문서 정보를 찾을 수 없습니다."
            
        item_name, success_rate, add_str, add_attack = scroll_row
        
        # 3. 강화 성공/실패 주사위 굴리기
        is_success = random.random() < success_rate
        new_slots = slots_left - 1  # 성공/실패 여부 관계없이 슬롯 1 감소
        
        if is_success:
            new_str = current_str + add_str
            new_att = current_att + add_attack
            msg = f"✨ 주문서 강화 성공!\n[{item_name}] 효과가 적용되었습니다.\n(STR +{add_str}, 공격력 +{add_attack})"
        else:
            new_str = current_str
            new_att = current_att
            msg = f"❌ 주문서 강화 실패...\n[{item_name}]의 효과가 나타나지 않았습니다."
            
        # 4. 계산된 결과를 DB에 반영
        conn.execute("""
            UPDATE user_equipment
            SET bonus_str = ?, bonus_attack = ?, upgrade_slot_left = ?
            WHERE user_equipment_id = ?
        """, [new_str, new_att, new_slots, user_equipment_id])
        
        return is_success, msg