# repository/__init__.py
import os
from repository.duckdb.equipment_master import DuckDBEquipmentMasterRepository
from repository.duckdb.user_equipment import DuckDBUserEquipmentRepository
from repository.duckdb.potential import DuckDBPotentialRepository
from repository.duckdb.scroll import DuckDBScrollDetailRepository

# 환경 변수나 기본값으로 duckdb 설정
DB_TYPE = os.getenv("DB_TYPE", "duckdb")

if DB_TYPE == "duckdb":
    # 이 부분에서 인스턴스를 생성하여 외부에서 import 할 수 있게 만듭니다.
    equipment_master_repo = DuckDBEquipmentMasterRepository()
    user_equipment_repo = DuckDBUserEquipmentRepository()
    potential_repo = DuckDBPotentialRepository()
    scroll_repo = DuckDBScrollDetailRepository()
else:
    raise ValueError(f"지원하지 않는 DB_TYPE 입니다: {DB_TYPE}")