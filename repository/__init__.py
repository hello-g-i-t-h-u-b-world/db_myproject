# repository/__init__.py
import os
from repository.duckdb.equipment_master import DuckDBEquipmentMasterRepository
from repository.duckdb.user_equipment import DuckDBUserEquipmentRepository
from repository.duckdb.equipment_potential import DuckDBEquipmentPotentialRepository
from repository.duckdb.scroll_detail import DuckDBScrollDetailRepository
from repository.duckdb.chaos_scroll_detail import DuckDBChaosScrollDetailRepository
from repository.duckdb.cube_upgrade_prob import DuckDBCubeUpgradeProbRepository
from repository.duckdb.simulation_usage_log import DuckDBSimulationUsageLogRepository, DuckDBSimulationResultRepository
from repository.duckdb.potential_option_pool import DuckDBPotentialOptionPoolRepository
from repository.duckdb.item_master import DuckDBItemMasterRepository
from repository.duckdb.equipment_potential_rule import DuckDBEquipmentPotentialRuleRepository

# 환경 변수나 기본값으로 duckdb 설정
DB_TYPE = os.getenv("DB_TYPE", "duckdb")

if DB_TYPE == "duckdb":
    # 이 부분에서 인스턴스를 생성하여 외부에서 import 할 수 있게 만듭니다.
    equipment_master_repo = DuckDBEquipmentMasterRepository()
    user_equipment_repo = DuckDBUserEquipmentRepository()
    equipment_potential_repo = DuckDBEquipmentPotentialRepository()
    scroll_repo = DuckDBScrollDetailRepository()
    chaos_scroll_repo = DuckDBChaosScrollDetailRepository()
    cube_upgrade_repo = DuckDBCubeUpgradeProbRepository()
    simulation_usage_log_repo = DuckDBSimulationUsageLogRepository()
    simulation_result_repo = DuckDBSimulationResultRepository()
    potential_option_pool_repo = DuckDBPotentialOptionPoolRepository()
    item_master_repo = DuckDBItemMasterRepository()
    equipment_potential_rule_repo = DuckDBEquipmentPotentialRuleRepository()
else:
    raise ValueError(f"지원하지 않는 DB_TYPE 입니다: {DB_TYPE}")


