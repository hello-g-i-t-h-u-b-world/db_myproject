import duckdb

DB_PATH = "data/maple_planet.db"

def get_connection():
    return duckdb.connect(DB_PATH)