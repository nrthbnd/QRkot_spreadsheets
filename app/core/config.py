from typing import Optional

from pydantic import BaseSettings, EmailStr

from constants import APP_TITLE, DATABASE_URL, ENV_FILE_NAME, SECRET


class Settings(BaseSettings):
    """Считывать переменные окружения из файла."""
    app_title: str = APP_TITLE
    database_url: str = DATABASE_URL
    secret: str = SECRET

    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = ''
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        """Файл с переменными окружения."""
        env_file = ENV_FILE_NAME


settings = Settings()
