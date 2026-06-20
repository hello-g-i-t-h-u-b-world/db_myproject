from db import get_connection

conn = get_connection()

# ==================================================
# equipment_master
# ==================================================

conn.execute("""
CREATE TABLE IF NOT EXISTS equipment_master (
    equipment_id INTEGER PRIMARY KEY,
    equipment_name VARCHAR NOT NULL,
    equipment_type VARCHAR NOT NULL,
    image_path VARCHAR
)
""")
conn.execute("ALTER TABLE equipment_master ADD COLUMN IF NOT EXISTS image_path VARCHAR")

# ==================================================
# user_equipment
# ==================================================

conn.execute("""
CREATE TABLE IF NOT EXISTS user_equipment (
    user_equipment_id INTEGER PRIMARY KEY,

    equipment_id INTEGER NOT NULL,
    
    current_stat INTEGER NOT NULL,

    bonus_str INTEGER DEFAULT 0,
    bonus_attack INTEGER DEFAULT 0,

    upgrade_slot_left INTEGER NOT NULL,

    potential_grade VARCHAR NOT NULL,

    FOREIGN KEY (equipment_id)
        REFERENCES equipment_master(equipment_id),

    CHECK (
        potential_grade IN ('Rare','Epic','Unique')
    )
)
""")

# ==================================================
# potential_option_pool
# ==================================================

conn.execute("""
CREATE TABLE IF NOT EXISTS potential_option_pool (
    option_id INTEGER PRIMARY KEY,
    grade VARCHAR NOT NULL,

    option_effect VARCHAR NOT NULL,

    CHECK (
        grade IN ('Rare','Epic','Unique')
    )
)
""")

# ==================================================
# equipment_potential
# ==================================================

conn.execute("""
CREATE TABLE IF NOT EXISTS equipment_potential (
    user_equipment_id INTEGER NOT NULL,

    line_no INTEGER NOT NULL,

    option_id INTEGER NOT NULL,

    PRIMARY KEY (
        user_equipment_id,
        line_no
    ),

    FOREIGN KEY (user_equipment_id)
        REFERENCES user_equipment(user_equipment_id),

    FOREIGN KEY (option_id)
        REFERENCES potential_option_pool(option_id),

    CHECK (
        line_no BETWEEN 1 AND 3
    )
)
""")

# ==================================================
# item_master  (자식 테이블 먼저 DROP 후 부모 DROP)
# ==================================================
conn.execute("DROP TABLE IF EXISTS simulation_usage_log;")
conn.execute("DROP TABLE IF EXISTS cube_upgrade_prob;")
conn.execute("DROP TABLE IF EXISTS chaos_scroll_detail;")
conn.execute("DROP TABLE IF EXISTS scroll_detail;")
conn.execute("DROP TABLE IF EXISTS item_master;")

conn.execute("""
CREATE TABLE IF NOT EXISTS item_master (
    item_id INTEGER PRIMARY KEY,

    item_name VARCHAR NOT NULL,

    item_type VARCHAR NOT NULL,

    price BIGINT NOT NULL,

    image_path VARCHAR,

    CHECK (
        item_type IN ('주문서','혼돈주문서','큐브')
    )
)
""")
conn.execute("ALTER TABLE item_master ADD COLUMN IF NOT EXISTS image_path VARCHAR")

# ==================================================
# scroll_detail
# ==================================================
conn.execute("""
CREATE TABLE IF NOT EXISTS scroll_detail (
    item_id INTEGER PRIMARY KEY,

    success_rate DOUBLE NOT NULL,

    add_str INTEGER DEFAULT 0,

    add_attack INTEGER DEFAULT 0,

    FOREIGN KEY (item_id)
        REFERENCES item_master(item_id)
)
""")

# ==================================================
# chaos_scroll_detail
# ==================================================
conn.execute("""
CREATE TABLE IF NOT EXISTS chaos_scroll_detail (
    item_id      INTEGER PRIMARY KEY,
    success_rate DOUBLE  NOT NULL,
    chaos_min    INTEGER NOT NULL,
    chaos_max    INTEGER NOT NULL,

    FOREIGN KEY (item_id)
        REFERENCES item_master(item_id)
)
""")


# ==================================================
# cube_upgrade_prob
# ==================================================
conn.execute("""
CREATE TABLE IF NOT EXISTS cube_upgrade_prob (
    item_id INTEGER NOT NULL,

    current_grade VARCHAR NOT NULL,

    tier_up_rate DOUBLE NOT NULL,

    PRIMARY KEY (
        item_id,
        current_grade
    ),

    FOREIGN KEY (item_id)
        REFERENCES item_master(item_id)
)
""")

# ==================================================
# equipment_potential_rule
# ==================================================
conn.execute("""
DROP TABLE IF EXISTS equipment_potential_rule;
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS equipment_potential_rule (
    equipment_type VARCHAR NOT NULL,

    option_id INTEGER NOT NULL,

    PRIMARY KEY (
        equipment_type,
        option_id
    ),

    FOREIGN KEY (option_id)
        REFERENCES potential_option_pool(option_id)
)
""")

# ==================================================
# potential_option_probability
# ==================================================

conn.execute("""
CREATE TABLE IF NOT EXISTS potential_option_probability (
    option_id INTEGER NOT NULL,

    line_no INTEGER NOT NULL,

    probability DOUBLE NOT NULL,

    PRIMARY KEY (
        option_id,
        line_no
    ),

    FOREIGN KEY (option_id)
        REFERENCES potential_option_pool(option_id)
);
""")

# ==================================================
# simulation_usage_log
# ==================================================

conn.execute("""
CREATE TABLE IF NOT EXISTS simulation_usage_log (
    user_equipment_id INTEGER NOT NULL,

    item_id INTEGER NOT NULL,

    use_count INTEGER DEFAULT 0,

    PRIMARY KEY (
        user_equipment_id,
        item_id
    ),

    FOREIGN KEY (user_equipment_id)
        REFERENCES user_equipment(user_equipment_id),

    FOREIGN KEY (item_id)
        REFERENCES item_master(item_id)
)
""")

# ==================================================
# 초기 데이터
# ==================================================

# 장비

conn.execute("""
INSERT OR IGNORE INTO equipment_master VALUES
(1, '알카드노의 망토', '망토', '1.png'),
(2, '리버스 니플하임', '무기', '2.png'),
(3, '자쿰의 투구', '모자', '3.png'),
(4, '하프 이어링', '귀고리', '4.png'),
(5, '혼테일의 목걸이', '펜던트', '5.png')
""")

# 기존 행에 image_path 없으면 업데이트
conn.execute("UPDATE equipment_master SET image_path = '1.png' WHERE equipment_id = 1 AND image_path IS NULL")
conn.execute("UPDATE equipment_master SET image_path = '2.png' WHERE equipment_id = 2 AND image_path IS NULL")
conn.execute("UPDATE equipment_master SET image_path = '3.png' WHERE equipment_id = 3 AND image_path IS NULL")
conn.execute("UPDATE equipment_master SET image_path = '4.png' WHERE equipment_id = 4 AND image_path IS NULL")
conn.execute("UPDATE equipment_master SET image_path = '5.png' WHERE equipment_id = 5 AND image_path IS NULL")

# 주문서

conn.execute("""
INSERT OR IGNORE INTO item_master VALUES
(101, '망토 힘 주문서 60%', '주문서', 104588, '101.png'),
(102, '망토 힘 주문서 10%', '주문서', 98000, '102.png'),

(103, '두손검 공격력 주문서 100%', '주문서', 79294, '103.png'),
(104, '두손검 공격력 주문서 60%', '주문서', 319055, '104.png'),
(105, '두손검 공격력 주문서 10%', '주문서', 1587530, '105.png')
""")

# 기존 행 image_path 업데이트
for _id in [101, 102, 103, 104, 105]:
    conn.execute(f"UPDATE item_master SET image_path = '{_id}.png' WHERE item_id = {_id} AND image_path IS NULL")

# id, 확률, +STR, +공격력
conn.execute("""
INSERT OR IGNORE INTO scroll_detail VALUES
(101, 0.6, 2, 0),
(102, 0.1, 3, 0),

(103, 1, 0, 1),
(104, 0.6, 1, 2),
(105, 0.1, 3, 5)
""")

# 혼돈의 주문서
conn.execute("""
INSERT OR IGNORE INTO item_master VALUES
(106, '혼돈의 주문서 60%', '혼돈주문서', 1824509, '106.png')
""")
conn.execute("UPDATE item_master SET image_path = '106.png' WHERE item_id = 106 AND image_path IS NULL")

conn.execute("""
INSERT OR IGNORE INTO chaos_scroll_detail VALUES
(106, 0.6, -5, 5)
""")

# 큐브

conn.execute("""
INSERT OR IGNORE INTO item_master VALUES
(201, '미라클 큐브', '큐브', 500000, '미라클큐브.png')
""")
conn.execute("UPDATE item_master SET image_path = '미라클큐브.png' WHERE item_id = 201 AND image_path IS NULL")

conn.execute("""
INSERT OR IGNORE INTO cube_upgrade_prob VALUES

(201, 'Rare', 0.06),
(201, 'Epic', 0.018);
""")

# 잠재옵션

conn.execute("""
INSERT OR IGNORE INTO potential_option_pool VALUES

(1001, 'Rare', '총 데미지: +3%'),
(1002, 'Rare', 'STR: +12'),
(1003, 'Rare', 'DEX: +12'),
(1004, 'Rare', 'INT: +12'),
(1005, 'Rare', 'LUK: +12'),
(1006, 'Rare', '공격력: +12'),
(1007, 'Rare', '마력: +12'),
(1008, 'Rare', 'STR: +3%'),
(1009, 'Rare', 'DEX: +3%'),
(1010, 'Rare', 'INT: +3%'),
(1011, 'Rare', 'LUK: +3%'),
(1012, 'Rare', '공격력: +3%'),
(1013, 'Rare', '마력: +3%'),
(1014, 'Rare', '크리티컬 확률: +4%'),
(1015, 'Rare', '올스텟: +5'),
(1016, 'Rare', '공격 시 몬스터의 방어율 15% 무시'),   
(1017, 'Rare', 'STR: +6'),
(1018, 'Rare', 'DEX: +6'),          
(1019, 'Rare', 'INT: +6'),          
(1020, 'Rare', 'LUK: +6'),          
(1021, 'Rare', '공격력: +6'),          
(1022, 'Rare', '마력: +6'),                 

(2001, 'Epic', 'MaxHP : +6%'),
(2002, 'Epic', 'MaxMP : +6%'),
(2003, 'Epic', '총 데미지 : +6%'),
(2004, 'Epic', 'STR : +14'),
(2005, 'Epic', 'DEX : +14'),
(2006, 'Epic', 'INT : +14'),
(2007, 'Epic', 'LUK : +14'),
(2008, 'Epic', '공격력 : +14'),
(2009, 'Epic', '마력 : +14'),
(2010, 'Epic', 'STR : +6%'),
(2011, 'Epic', 'DEX : +6%'),
(2012, 'Epic', 'INT : +6%'),
(2013, 'Epic', 'LUK : +6%'),
(2014, 'Epic', '공격력 : +6%'),
(2015, 'Epic', '마력 : +6%'),
(2016, 'Epic', '크리티컬 확률 : +8%'),
(2017, 'Epic', '올스탯 : +3%'),
(2018, 'Epic', '총 데미지 : +3%'),
(2019, 'Epic', 'STR : +12'),
(2020, 'Epic', 'DEX : +12'),
(2021, 'Epic', 'INT : +12'),
(2022, 'Epic', 'LUK : +12'),
(2023, 'Epic', '공격력 : +12'),
(2024, 'Epic', '마력 : +12'),
(2025, 'Epic', 'STR : +3%'),
(2026, 'Epic', 'DEX : +3%'),
(2027, 'Epic', 'INT : +3%'),
(2028, 'Epic', 'LUK : +3%'),
(2029, 'Epic', '공격력 : +3%'),
(2030, 'Epic', '마력 : +3%'),
(2031, 'Epic', '크리티컬 확률 : +4%'),
(2032, 'Epic', '올스탯 : +5'),
(2033, 'Epic', '공격 시 몬스터의 방어율 15% 무시'),

(3001, 'Rare', 'MaxHP : +3%'),
(3002, 'Rare', 'MaxMP : +3%'),
(3003, 'Rare', 'STR : +12'),
(3004, 'Rare', 'DEX : +12'),
(3005, 'Rare', 'INT : +12'),
(3006, 'Rare', 'LUK : +12'),
(3007, 'Rare', 'STR : +3%'),
(3008, 'Rare', 'DEX : +3%'),
(3009, 'Rare', 'INT : +3%'),
(3010, 'Rare', 'LUK : +3%'),
(3011, 'Rare', '올스탯 : +5'),
(3012, 'Rare', 'STR : +6'),
(3013, 'Rare', 'DEX : +6'),
(3014, 'Rare', 'INT : +6'),
(3015, 'Rare', 'LUK : +6'),

(4001, 'Unique', '보스 공격 시 데미지 : +20%'),
(4002, 'Unique', '보스 공격 시 데미지 : +30%'),
(4003, 'Unique', 'STR : +16'),
(4004, 'Unique', 'DEX : +16'),
(4005, 'Unique', 'INT : +16'),
(4006, 'Unique', 'LUK : +16'),
(4007, 'Unique', '공격력 : +16'),
(4008, 'Unique', '마력 : +16'),
(4009, 'Unique', 'STR : +9%'),
(4010, 'Unique', 'DEX : +9%'),
(4011, 'Unique', 'INT : +9%'),
(4012, 'Unique', 'LUK : +9%'),
(4013, 'Unique', '공격력 : +9%'),
(4014, 'Unique', '마력 : +9%'),
(4015, 'Unique', '크리티컬 확률 : +9%'),
(4016, 'Unique', '올스탯 : +6%'),
(4017, 'Unique', '공격 시 몬스터의 방어율 30% 무시'),
(4018, 'Unique', 'MaxHP : +6%'),
(4019, 'Unique', 'MaxMP : +6%'),
(4020, 'Unique', '총 데미지 : +6%'),
(4021, 'Unique', 'STR : +14'),
(4022, 'Unique', 'DEX : +14'),
(4023, 'Unique', 'INT : +14'),
(4024, 'Unique', 'LUK : +14'),
(4025, 'Unique', '공격력 : +14'),
(4026, 'Unique', '마력 : +14'),
(4027, 'Unique', 'STR : +6%'),
(4028, 'Unique', 'DEX : +6%'),
(4029, 'Unique', 'INT : +6%'),
(4030, 'Unique', 'LUK : +6%'),
(4031, 'Unique', '공격력 : +6%'),
(4032, 'Unique', '마력 : +6%'),
(4033, 'Unique', '크리티컬 확률 : +8%'),
(4034, 'Unique', '올스탯 : +3%'),
(4035, 'Unique', '공격 시 몬스터의 방어율 15% 무시'),
(4036, 'Unique', '총 데미지 : +9%'),

(5001, 'Epic', 'MaxHP : +6%'),
(5002, 'Epic', 'MaxMP : +6%'),
(5003, 'Epic', 'STR : +14'),
(5004, 'Epic', 'DEX : +14'),
(5005, 'Epic', 'INT : +14'),
(5006, 'Epic', 'LUK : +14'),
(5007, 'Epic', 'STR : +6%'),
(5008, 'Epic', 'DEX : +6%'),
(5009, 'Epic', 'INT : +6%'),
(5010, 'Epic', 'LUK : +6%'),
(5011, 'Epic', '올스탯 : +3%'),

(6001, 'Unique', 'MaxHP : +9%'),
(6002, 'Unique', 'MaxMP : +9%'),
(6003, 'Unique', 'STR : +16'),
(6004, 'Unique', 'DEX : +16'),
(6005, 'Unique', 'INT : +16'),
(6006, 'Unique', 'LUK : +16'),
(6007, 'Unique', 'STR : +9%'),
(6008, 'Unique', 'DEX : +9%'),
(6009, 'Unique', 'INT : +9%'),
(6010, 'Unique', 'LUK : +9%'),
(6011, 'Unique', '올스탯 : +6%');
""")

# 부위 별 잠재옵션 (무기)
conn.execute("""
INSERT OR IGNORE INTO equipment_potential_rule
SELECT '무기', option_id
FROM potential_option_pool
WHERE option_id BETWEEN 1001 AND 1022;
""")
conn.execute("""
INSERT OR IGNORE INTO equipment_potential_rule
SELECT '무기', option_id
FROM potential_option_pool
WHERE option_id BETWEEN 2001 AND 2018;
""")
conn.execute("""
INSERT OR IGNORE INTO equipment_potential_rule
SELECT '무기', option_id
FROM potential_option_pool
WHERE option_id BETWEEN 4001 AND 4036;
""")

armor_types = [
    "모자",
    "팬던트",
    "귀고리",
    "망토"
]

for equipment_type in armor_types:
    for option_id in range(3001, 3016):
        conn.execute(
            "INSERT OR IGNORE INTO equipment_potential_rule VALUES (?, ?)",
            [equipment_type, option_id]
        )

for equipment_type in armor_types:
    for option_id in range(5001, 5012):
        conn.execute(
            "INSERT OR IGNORE INTO equipment_potential_rule VALUES (?, ?)",
            [equipment_type, option_id]
        )

for equipment_type in armor_types:
    for option_id in range(6001, 6012):
        conn.execute(
            "INSERT OR IGNORE INTO equipment_potential_rule VALUES (?, ?)",
            [equipment_type, option_id]
        )

conn.execute("""
INSERT OR IGNORE INTO potential_option_probability VALUES

-- 2001 MaxHP +6%
(2001,1,0.064516),
(2001,2,0.006452),
(2001,3,0.000645),

-- 2002 MaxMP +6%
(2002,1,0.064516),
(2002,2,0.006452),
(2002,3,0.000645),

-- 2003 총 데미지 +6%
(2003,1,0.064516),
(2003,2,0.006452),
(2003,3,0.000645),

-- 2004~2009 (+14 스탯, 공격력, 마력)
(2004,1,0.053763),(2004,2,0.005376),(2004,3,0.000538),
(2005,1,0.053763),(2005,2,0.005376),(2005,3,0.000538),
(2006,1,0.053763),(2006,2,0.005376),(2006,3,0.000538),
(2007,1,0.053763),(2007,2,0.005376),(2007,3,0.000538),
(2008,1,0.053763),(2008,2,0.005376),(2008,3,0.000538),
(2009,1,0.053763),(2009,2,0.005376),(2009,3,0.000538),

-- 2010~2015 (+6%)
(2010,1,0.053763),(2010,2,0.005376),(2010,3,0.000538),
(2011,1,0.053763),(2011,2,0.005376),(2011,3,0.000538),
(2012,1,0.053763),(2012,2,0.005376),(2012,3,0.000538),
(2013,1,0.053763),(2013,2,0.005376),(2013,3,0.000538),
(2014,1,0.053763),(2014,2,0.005376),(2014,3,0.000538),
(2015,1,0.053763),(2015,2,0.005376),(2015,3,0.000538),

-- 2016 크확 +8%
(2016,1,0.053763),
(2016,2,0.005376),
(2016,3,0.000538),

-- 2017 올스탯 +3%
(2017,1,0.053763),
(2017,2,0.005376),
(2017,3,0.000538),

-- 2018 총 데미지 +3%
(2018,2,0.066667),
(2018,3,0.073333),

-- 2019~2024 (+12)
(2019,2,0.055556),(2019,3,0.061111),
(2020,2,0.055556),(2020,3,0.061111),
(2021,2,0.055556),(2021,3,0.061111),
(2022,2,0.055556),(2022,3,0.061111),
(2023,2,0.055556),(2023,3,0.061111),
(2024,2,0.055556),(2024,3,0.061111),

-- 2025~2030 (+3%)
(2025,2,0.055556),(2025,3,0.061111),
(2026,2,0.055556),(2026,3,0.061111),
(2027,2,0.055556),(2027,3,0.061111),
(2028,2,0.055556),(2028,3,0.061111),
(2029,2,0.055556),(2029,3,0.061111),
(2030,2,0.055556),(2030,3,0.061111),

-- 2031 크확 +4%
(2031,2,0.055556),
(2031,3,0.061111),

-- 2032 올스탯 +5
(2032,2,0.055556),
(2032,3,0.061111),

-- 2033 방무 15%
(2033,1,0.053763),
(2033,2,0.060932),
(2033,3,0.061649),

-- 1줄

(3001,1,0.105263),
(3002,1,0.105263),

(3003,1,0.087719),
(3004,1,0.087719),
(3005,1,0.087719),
(3006,1,0.087719),

(3007,1,0.087719),
(3008,1,0.087719),
(3009,1,0.087719),
(3010,1,0.087719),

(3011,1,0.087719),

-- 2줄 일반 옵션

(3012,2,0.225000),
(3013,2,0.225000),
(3014,2,0.225000),
(3015,2,0.225000),

-- 2줄 레어 옵션

(3001,2,0.010526),
(3002,2,0.010526),

(3003,2,0.008772),
(3004,2,0.008772),
(3005,2,0.008772),
(3006,2,0.008772),

(3007,2,0.008772),
(3008,2,0.008772),
(3009,2,0.008772),
(3010,2,0.008772),

(3011,2,0.008772),

-- 3줄 일반 옵션

(3012,3,0.247500),
(3013,3,0.247500),
(3014,3,0.247500),
(3015,3,0.247500),

-- 3줄 레어 옵션

(3001,3,0.001053),
(3002,3,0.001053),

(3003,3,0.000877),
(3004,3,0.000877),
(3005,3,0.000877),
(3006,3,0.000877),

(3007,3,0.000877),
(3008,3,0.000877),
(3009,3,0.000877),
(3010,3,0.000877),

(3011,3,0.000877),

-- 1줄 전용 Unique 옵션
(4001,1,0.064516),
(4001,2,0.006452),
(4001,3,0.000645),

(4002,1,0.064516),
(4002,2,0.006452),
(4002,3,0.000645),

(4003,1,0.053763),
(4003,2,0.005376),
(4003,3,0.000538),

(4004,1,0.053763),
(4004,2,0.005376),
(4004,3,0.000538),

(4005,1,0.053763),
(4005,2,0.005376),
(4005,3,0.000538),

(4006,1,0.053763),
(4006,2,0.005376),
(4006,3,0.000538),

(4007,1,0.053763),
(4007,2,0.005376),
(4007,3,0.000538),

(4008,1,0.053763),
(4008,2,0.005376),
(4008,3,0.000538),

(4009,1,0.053763),
(4009,2,0.005376),
(4009,3,0.000538),

(4010,1,0.053763),
(4010,2,0.005376),
(4010,3,0.000538),

(4011,1,0.053763),
(4011,2,0.005376),
(4011,3,0.000538),

(4012,1,0.053763),
(4012,2,0.005376),
(4012,3,0.000538),

(4013,1,0.053763),
(4013,2,0.005376),
(4013,3,0.000538),

(4014,1,0.053763),
(4014,2,0.005376),
(4014,3,0.000538),

(4015,1,0.053763),
(4015,2,0.005376),
(4015,3,0.000538),

(4016,1,0.053763),
(4016,2,0.005376),
(4016,3,0.000538),

(4017,1,0.053763),
(4017,2,0.005376),
(4017,3,0.000538),

-- 2줄/3줄 일반 옵션

(4018,2,0.058065),(4018,3,0.063871),
(4019,2,0.058065),(4019,3,0.063871),
(4020,2,0.058065),(4020,3,0.063871),

(4021,2,0.048387),(4021,3,0.053226),
(4022,2,0.048387),(4022,3,0.053226),
(4023,2,0.048387),(4023,3,0.053226),
(4024,2,0.048387),(4024,3,0.053226),
(4025,2,0.048387),(4025,3,0.053226),
(4026,2,0.048387),(4026,3,0.053226),

(4027,2,0.048387),(4027,3,0.053226),
(4028,2,0.048387),(4028,3,0.053226),
(4029,2,0.048387),(4029,3,0.053226),
(4030,2,0.048387),(4030,3,0.053226),
(4031,2,0.048387),(4031,3,0.053226),
(4032,2,0.048387),(4032,3,0.053226),

(4033,2,0.048387),(4033,3,0.053226),
(4034,2,0.048387),(4034,3,0.053226),
(4035,2,0.048387),(4035,3,0.053226),

-- 총데미지 9%
(4036,2,0.006452),
(4036,3,0.000645),

-- 1줄

(5001,1,0.105263),
(5002,1,0.105263),

(5003,1,0.087719),
(5004,1,0.087719),
(5005,1,0.087719),
(5006,1,0.087719),

(5007,1,0.087719),
(5008,1,0.087719),
(5009,1,0.087719),
(5010,1,0.087719),

(5011,1,0.087719),

-- 2줄 하위 등급 옵션

(3001,2,0.094737),
(3002,2,0.094737),

(3003,2,0.078947),
(3004,2,0.078947),
(3005,2,0.078947),
(3006,2,0.078947),

(3007,2,0.078947),
(3008,2,0.078947),
(3009,2,0.078947),
(3010,2,0.078947),

(3011,2,0.078947),

-- 2줄 에픽 옵션

(5001,2,0.010526),
(5002,2,0.010526),

(5003,2,0.008772),
(5004,2,0.008772),
(5005,2,0.008772),
(5006,2,0.008772),

(5007,2,0.008772),
(5008,2,0.008772),
(5009,2,0.008772),
(5010,2,0.008772),

(5011,2,0.008772),

-- 3줄 하위 등급 옵션

(3001,3,0.104211),
(3002,3,0.104211),

(3003,3,0.086842),
(3004,3,0.086842),
(3005,3,0.086842),
(3006,3,0.086842),

(3007,3,0.086842),
(3008,3,0.086842),
(3009,3,0.086842),
(3010,3,0.086842),

(3011,3,0.086842),

-- 3줄 에픽 옵션

(5001,3,0.001053),
(5002,3,0.001053),

(5003,3,0.000877),
(5004,3,0.000877),
(5005,3,0.000877),
(5006,3,0.000877),

(5007,3,0.000877),
(5008,3,0.000877),
(5009,3,0.000877),
(5010,3,0.000877),

(5011,3,0.000877),

-- 1줄 Unique 옵션

(6001,1,0.105263),
(6002,1,0.105263),

(6003,1,0.087719),
(6004,1,0.087719),
(6005,1,0.087719),
(6006,1,0.087719),

(6007,1,0.087719),
(6008,1,0.087719),
(6009,1,0.087719),
(6010,1,0.087719),

(6011,1,0.087719),

-- 2줄 Epic 옵션

(5001,2,0.094737),
(5002,2,0.094737),

(5003,2,0.078947),
(5004,2,0.078947),
(5005,2,0.078947),
(5006,2,0.078947),

(5007,2,0.078947),
(5008,2,0.078947),
(5009,2,0.078947),
(5010,2,0.078947),

(5011,2,0.078947),

-- 2줄 Unique 옵션

(6001,2,0.010526),
(6002,2,0.010526),

(6003,2,0.008772),
(6004,2,0.008772),
(6005,2,0.008772),
(6006,2,0.008772),

(6007,2,0.008772),
(6008,2,0.008772),
(6009,2,0.008772),
(6010,2,0.008772),

(6011,2,0.008772),

-- 3줄 Epic 옵션

(5001,3,0.104211),
(5002,3,0.104211),

(5003,3,0.086842),
(5004,3,0.086842),
(5005,3,0.086842),
(5006,3,0.086842),

(5007,3,0.086842),
(5008,3,0.086842),
(5009,3,0.086842),
(5010,3,0.086842),

(5011,3,0.086842),

-- 3줄 Unique 옵션

(6001,3,0.001053),
(6002,3,0.001053),

(6003,3,0.000877),
(6004,3,0.000877),
(6005,3,0.000877),
(6006,3,0.000877),

(6007,3,0.000877),
(6008,3,0.000877),
(6009,3,0.000877),
(6010,3,0.000877),

(6011,3,0.000877);
""")

conn.close()

print("DB 초기화 완료")