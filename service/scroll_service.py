# service/scroll_service.py
import random
from repository import scroll_repo, chaos_scroll_repo, item_master_repo


def get_available_scrolls() -> list:
    """
    DB에 등록된 모든 주문서(일반 + 혼돈) 목록을 반환합니다.
    반환: [(item_id, item_name, success_rate, add_str, add_attack, price), ...]
    혼돈 주문서는 add_str=0, add_attack=0으로 패딩합니다.
    """
    normal_scrolls = scroll_repo.get_all_scrolls()

    # 혼돈 주문서를 동일한 구조로 변환 (add_str, add_attack = 0)
    chaos_scrolls = chaos_scroll_repo.get_all_chaos_scrolls()
    chaos_scrolls_padded = [(item_id, name, rate, 0, 0, price) for item_id, name, rate, price in chaos_scrolls]

    return normal_scrolls + chaos_scrolls_padded


def get_equipment_scroll_status(user_equipment_id: int) -> tuple[int, int, int]:
    """장비의 주문서 강화 상태 (bonus_str, bonus_attack, upgrade_slot_left)를 반환합니다."""
    return scroll_repo.get_equipment_scroll_status(user_equipment_id)


def use_scroll(user_equipment_id: int, item_id: int) -> tuple[bool, str]:
    """
    주문서를 사용하고 결과를 DB에 저장합니다.
    item_type이 '혼돈주문서'면 chaos_scroll_detail 로직을 적용합니다.
    사용 기록은 simulation_usage_log에 자동 저장됩니다.
    반환: (성공여부, 메시지)
    """
    from service.stats_service import log_item_usage

    current_str, current_att, slots_left = scroll_repo.get_equipment_scroll_status(user_equipment_id)

    if slots_left <= 0:
        return False, "업그레이드 가능한 횟수가 없습니다!"

    item_info = item_master_repo.get_item_by_id(item_id)
    if not item_info:
        return False, "주문서 정보를 찾을 수 없습니다."

    item_name, item_type, _ = item_info
    is_success = False
    new_str = current_str
    new_att = current_att
    msg = ""

    # ── 혼돈의 주문서 ────────────────────────────────────────────────
    if item_type == '혼돈주문서':
        chaos_row = chaos_scroll_repo.get_chaos_scroll_info_by_id(item_id)

        if not chaos_row:
            return False, "혼돈 주문서 정보를 찾을 수 없습니다."

        success_rate, chaos_min, chaos_max = chaos_row
        is_success = random.random() < success_rate

        if is_success:
            delta_str = random.randint(chaos_min, chaos_max)
            delta_att = random.randint(chaos_min, chaos_max)
            new_str = current_str + delta_str
            new_att = current_att + delta_att

            sign_str = "+" if delta_str >= 0 else ""
            sign_att = "+" if delta_att >= 0 else ""
            msg = (
                f"🌀 혼돈의 주문서 성공!\n"
                f"STR {sign_str}{delta_str} ({current_str} → {new_str})\n"
                f"공격력 {sign_att}{delta_att} ({current_att} → {new_att})"
            )
        else:
            msg = f"❌ 혼돈의 주문서 실패...\n효과가 나타나지 않았습니다."

    # ── 일반 주문서 ──────────────────────────────────────────────────
    else:
        scroll_row = scroll_repo.get_scroll_info_by_id(item_id)

        if not scroll_row:
            return False, "주문서 정보를 찾을 수 없습니다."

        success_rate, add_str, add_attack = scroll_row[1], scroll_row[2], scroll_row[3]
        is_success = random.random() < success_rate

        if is_success:
            new_str = current_str + add_str
            new_att = current_att + add_attack
            msg = (
                f"✨ 주문서 강화 성공!\n"
                f"[{item_name}] 효과 적용 (STR +{add_str}, 공격력 +{add_attack})"
            )
        else:
            msg = f"❌ 주문서 강화 실패...\n[{item_name}]의 효과가 나타나지 않았습니다."

    # 결과 DB 저장
    new_slots = slots_left - 1
    scroll_repo.update_equipment_scroll_status(user_equipment_id, new_str, new_att, new_slots)

    log_item_usage(user_equipment_id, item_id)
    return is_success, msg
