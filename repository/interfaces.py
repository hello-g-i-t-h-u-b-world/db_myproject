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

class PotentialRepository(ABC):
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
        """모든 주문서 목록(아이템ID, 이름, 성공확률, 추가STR, 추가공격력, 가격)을 가져옵니다."""
        pass

    @abstractmethod
    def get_scroll_by_id(self, item_id: int) -> Tuple[str, float, int, int]:
        """특정 주문서의 상세 정보(이름, 성공확률, 추가STR, 추가공격력)를 가져옵니다."""
        pass

    @abstractmethod
    def get_equipment_scroll_status(self, user_equipment_id: int) -> Tuple[int, int, int]:
        """장비의 현재 주문서 강화 상태(bonus_str, bonus_attack, upgrade_slot_left)를 조회합니다."""
        pass

    @abstractmethod
    def update_equipment_scroll_status(self, user_equipment_id: int, bonus_str: int, bonus_attack: int, upgrade_slot_left: int) -> None:
        """장비의 주문서 강화 스탯 및 남은 슬롯 상태를 DB에 저장합니다."""
        pass