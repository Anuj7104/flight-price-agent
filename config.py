import os

DB_CONFIG = {
    'host': os.getenv("DB_HOST", "localhost"),
    'user': os.getenv("DB_USER", "root"),
    'password': os.getenv("DB_PASSWORD", "yourpassword"),
    'database': os.getenv("DB_NAME", "flight_db")
}