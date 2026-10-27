import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-por-defecto'
    
    # 1. Intentar buscar una URL completa de conexión directa (común en la nube)
    database_url = os.environ.get('MYSQL_URL') or os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI')

    if database_url:
        # Si Railway provee una URL directa, la usamos (asegurando el prefijo pymysql si es necesario)
        if database_url.startswith("mysql://"):
            database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # 2. Si no, construirlas con las variables individuales o usar localhost en local
        db_user = os.environ.get('MYSQLUSER') or os.environ.get('DB_USER') or 'root'
        db_password = os.environ.get('MYSQLPASSWORD') or os.environ.get('DB_PASSWORD') or ''
        db_host = os.environ.get('MYSQLHOST') or os.environ.get('DB_HOST') or 'localhost'
        db_port = os.environ.get('MYSQLPORT') or os.environ.get('DB_PORT') or '3306'
        db_name = os.environ.get('MYSQLDATABASE') or os.environ.get('DB_NAME') or 'cafe_aroma'

        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False