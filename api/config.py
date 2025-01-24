import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI", "mysql+pymysql://root:1q2w3e4r5t@localhost:3306/checador-xrom"
    )


user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DB")


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )


config = {"development": DevelopmentConfig, "production": ProductionConfig}
