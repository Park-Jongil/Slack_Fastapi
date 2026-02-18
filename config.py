import os

class Settings:
    def __init__(self):
        # 환경변수에서 읽거나 기본값 사용
        self.database_url = os.getenv(
            "DATABASE_URL", 
            "postgresql://postgres:1331@localhost:5432/postgres"
        )

def get_settings():
    return Settings()
