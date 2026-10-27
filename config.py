
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-por-defecto'
    
    # Intentar construir la URI usando las variables de Railway o .env, con fallback a localhost
    db_user = os.environ.get('MYSQLUSER') or os.environ.get('DB_USER') or 'root'
    db_password = os.environ.get('MYSQLPASSWORD') or os.environ.get('DB_PASSWORD') or ''
    db_host = os.environ.get('MYSQLHOST') or os.environ.get('DB_HOST') or 'localhost'
    db_port = os.environ.get('MYSQLPORT') or os.environ.get('DB_PORT') or '3306'
    db_name = os.environ.get('MYSQLDATABASE') or os.environ.get('DB_NAME') or 'cafe_aroma'

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False