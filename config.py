class Config:
    """Application configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///rules.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = True