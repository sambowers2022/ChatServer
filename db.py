import mysql.connector
from dotenv import load_dotenv
import os

def init():
    load_dotenv()
    db = mysql.connector.connect(
        host="localhost",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PWD"],
        database="chat"
        )
    print("Database connected")
    return db

