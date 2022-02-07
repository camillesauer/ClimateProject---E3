import os
import sqlalchemy
from credentials import YOUR_KEY, YOUR_USERNAME
from credentials import mysql_pseudo, mysql_mdp, database_name
from kaggle.api.kaggle_api_extended import KaggleApi

os.environ['KAGGLE_USERNAME'] = YOUR_USERNAME
os.environ['KAGGLE_KEY'] = YOUR_KEY

api = KaggleApi()
api.authenticate()

def mysql_connect():
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@localhost/{2}'.format(mysql_pseudo, mysql_mdp, database_name),
    pool_recycle=1, pool_timeout=57600).connect()
    return database_connection
print("done")


