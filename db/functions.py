import sqlite3
import aiogram
from loader import db, cur

def create_user():
    cur.execute("INSERT INTO `users` VALUES()")