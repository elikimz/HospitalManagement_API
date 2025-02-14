from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_name: str
    database_port: int

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.database_username}:"
            f"{self.database_password}@{self.database_hostname}:"
            f"{self.database_port}/{self.database_name}?sslmode=require"
        )

    class Config:
        env_file = ".env"  # Ensures dotenv is loaded

settings = Settings()
