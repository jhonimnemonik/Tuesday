import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///db/data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'your_password_salt_here'
    SECURITY_PASSWORD_HASH = 'bcrypt'

    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your_email@example.com'
    MAIL_PASSWORD = 'your_email_password'

    BLACK_CONFIG = {
        'line_length': 120,
        'target_version': ['py37'],
        'exclude': '/(migrations|\.git)/'
    }

print(Config.SQLALCHEMY_DATABASE_URI)