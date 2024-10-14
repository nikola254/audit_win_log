import os
import psycopg2
import urllib.parse
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    username = 'postgres'
    password = 'root'
    dbname = 'RO'

    quoted_username = urllib.parse.quote_plus(username)
    quoted_password = urllib.parse.quote_plus(password)

    
    SQLALCHEMY_DATABASE_URI = f'postgresql://{quoted_username}:{quoted_password}@localhost/{dbname}'