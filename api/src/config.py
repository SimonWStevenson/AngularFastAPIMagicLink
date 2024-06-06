from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    admin_email: str
    admin_password: str
    website_url: str
    website_url_serve: str
    server_url: str
    jwt_secret_key: str
    session_token_days: int
    user_token_minutes: int
    model_config = SettingsConfigDict(env_file=".env")
