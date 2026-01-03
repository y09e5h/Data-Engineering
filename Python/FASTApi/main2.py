import json

from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import logging

from streamlit import rerun

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app = FastAPI()
app = FastAPI()

class User(BaseModel):
    username: str
    name: str
    age: int

def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager",
    )
    return db

@app.post("/add_user")
def add_user(user : User):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, name,age) VALUES (%s, %s,%s)", (user.username, user.name, user.age))
        db.commit()
        result = {"CreteUser": "Success"}
    except mysql.connector.Error as err:
        logging.error(err, exc_info=True)
        result = {"CreteUser": "Failed"}
    except Exception as err:
        logging.error(err, exc_info=True)
        result = {"CreteUser": "Failed"}
    finally:
        cursor.close()
        db.close()
    logging.info("User added successfully")
    return result

@app.get("/users")
async def get_users(username: str):
    result = {}
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        logging.error(f"User Creation Failed : {err}" ,exc_info=True)
        result = {"Error": err}
    except Exception as err:
        logging.error(f"User Creation Failed : {err}" ,exc_info=True)
        result =  {"Error": err}
    finally:
        cursor.close()
        db.close()
    return result

@app.get("/all_users")
def get_all_users():
    result = {}
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        logging.error(f"User Creation Failed : {err}", exc_info=True)
        result = {"Error": err}
    except Exception as err:
        logging.error(f"User Creation Failed : {err}", exc_info=True)
        result = {"Error": err}
    finally:
        cursor.close()
        db.close()
    return result

