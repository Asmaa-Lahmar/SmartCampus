"""Paramètres de l'API, lus dans les variables d'environnement puis dans backend/.env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+psycopg://smartcampus:smartcampus@localhost:5432/smartcampus"

    # Jeton JWT (ENF-02)
    jwt_secret: str = "dev-secret-a-remplacer-en-production-0123456789"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 30

    # Domaine des adresses autorisées (RG-11)
    allowed_email_domain: str = "usms.ac.ma"

    # Blocage après échecs de connexion (RG-02)
    max_failed_attempts: int = 3
    lock_minutes: int = 15

    # Coût du hachage bcrypt (ENF-01) ; les tests le baissent pour aller plus vite
    bcrypt_rounds: int = 12

    # Mot de passe des comptes de démonstration (src/seed.py)
    seed_password: str = "SmartCampus2026!"


settings = Settings()
