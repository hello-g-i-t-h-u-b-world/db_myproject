from abc import ABC, abstractmethod
from typing import List, Tuple

class EquipmentMasterRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Tuple[int, str, str]]: pass

class UserEquipmentRepository(ABC):
    @abstractmethod
    def insert(self, equipment_id: int, initial_grade: str = "Rare") -> int: pass
    @abstractmethod
    def get_equipment_type(self, user_equipment_id: int) -> str: pass
    @abstractmethod
    def get_details(self, user_equipment_id: int) -> Tuple[str, str, str]:
        """장비이름, 현재등급, 장비타입을 반환합니다."""
        pass
    @abstractmethod
    def update_grade(self, user_equipment_id: int, new_grade: str) -> None:
        """장비의 잠재 등급을 업데이트합니다."""
        pass
    @abstractmethod
    def get_equipment_id(self, user_equipment_id: int) -> int:
        """user_equipment_id로 equipment_id를 반환합니다."""
        pass
    @abstractmethod
    def get_all_user_equipments(self) -> list[dict]:
        """모든 유저 장비를 조회합니다."""
        pass

class EquipmentPotentialRepository(ABC):
    @abstractmethod
    def get_option_pool_with_prob(self, equipment_type: str, grade: str, line_no: int) -> List[Tuple[int, float]]: pass
    @abstractmethod
    def delete_potentials(self, user_equipment_id: int) -> None: pass
    @abstractmethod
    def insert_potential(self, user_equipment_id: int, line_no: int, option_id: int) -> None: pass
    @abstractmethod
    def get_current_potential_effects(self, user_equipment_id: int) -> List[str]:
        """현재 장비에 부여된 잠재능력 이펙트 문자열 3줄을 가져옵니다."""
        pass

class ScrollDetailRepository(ABC):
    @abstractmethod
    def get_all_scrolls(self) -> List[Tuple[int, str, float, int, int, int]]:
        """일반 주문서 목록(아이템ID, 이름, 성공확률, 추가STR, 추가공격력, 가격)을 가져옵니다."""
        pass

    @abstractmethod
    def get_equipment_scroll_status(self, user_equipment_id: int) -> Tuple[int, int, int]:
        """장비의 현재 주문서 강화 상태(bonus_str, bonus_attack, upgrade_slot_left)를 조회합니다."""
        pass

    @abstractmethod
    def update_equipment_scroll_status(self, user_equipment_id: int, bonus_str: int, bonus_attack: int, upgrade_slot_left: int) -> None:
        """장비의 주문서 강화 스탯 및 남은 슬롯 상태를 DB에 저장합니다."""
        pass

    @abstractmethod
    def get_scroll_info_by_id(self, item_id: int) -> Tuple[str, float, int, int]:
        """주문서 정보(이름, 성공율, add_str, add_attack)를 조회합니다."""
        pass

class ChaosScrollDetailRepository(ABC):
    @abstractmethod
    def get_all_chaos_scrolls(self) -> List[Tuple[int, str, float, int]]:
        """모든 혼돈 주문서 목록(아이템ID, 이름, 성공확률, 가격)을 가져옵니다."""
        pass

    @abstractmethod
    def get_chaos_scroll_info_by_id(self, item_id: int) -> Tuple[float, int, int]:
        """혼돈의 주문서 정보(성공율, min, max)를 조회합니다."""
        pass


class CubeUpgradeProbRepository(ABC):
    @abstractmethod
    def get_upgrade_prob(self, item_id: int, current_grade: str) -> Tuple[str, float]:
        """큐브의 다음 등급과 확률을 반환합니다. (next_grade, tier_up_rate)"""
        pass

class SimulationUsageLogRepository(ABC):
    @abstractmethod
    def log_item_usage(self, user_equipment_id: int, item_id: int) -> None:
        """아이템 사용 횟수를 기록합니다."""
        pass
    @abstractmethod
    def get_usage_logs(self, user_equipment_id: int) -> list:
        """사용 기록을 조회합니다."""
        pass

class SimulationResultRepository(ABC):
    @abstractmethod
    def get_simulation_result(self, user_equipment_id: int) -> dict:
        """시뮬레이션 결과를 조회합니다."""
        pass

class PotentialOptionPoolRepository(ABC):
    @abstractmethod
    def get_option_by_id(self, option_id: int) -> Tuple[int, str, str]:
        """option_id로 옵션 정보를 조회합니다. (option_id, grade, effect)"""
        pass
    @abstractmethod
    def get_options_by_grade(self, grade: str) -> List[Tuple[int, str]]:
        """등급별 모든 옵션을 조회합니다. (option_id, effect)"""
        pass

class ItemMasterRepository(ABC):
    @abstractmethod
    def get_item_by_id(self, item_id: int) -> Tuple[str, str, int]:
        """아이템 정보를 조회합니다. (name, type, price)"""
        pass
    @abstractmethod
    def get_items_by_type(self, item_type: str) -> List[Tuple[int, str, int]]:
        """아이템 타입별 아이템을 조회합니다. (item_id, name, price)"""
        pass

class EquipmentPotentialRuleRepository(ABC):
    @abstractmethod
    def get_valid_options_for_equipment(self, equipment_type: str) -> List[int]:
        """장비 타입에 유효한 옵션 ID 목록을 조회합니다."""
        pass
