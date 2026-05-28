"""Configuración de la aplicación (Single Responsibility: solo config)."""
import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql+psycopg2://bne_user:bne_password_123@localhost:5432/bne_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key_change_in_production')
