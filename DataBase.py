import math
import sqlite3
import time


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def get_menu(self):
        sql = "SELECT * FROM mainmenu"
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def add_post(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cursor.execute("INSERT INTO posts VALUES (NULL, ?, ?, ?)", (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД", str(e))
            return False
        return True

    def get_post(self, post_id):
        try:
            self.__cursor.execute(f"SELECT title, text FROM posts WHERE id = {post_id} LIMIT 1")
            res = self.__cursor.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД", str(e))
        return False, False

    def get_post_anonce(self):
        try:
            self.__cursor.execute(f"SELECT id, title, text FROM posts ORDER BY time DESC")
            res = self.__cursor.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД", str(e))
        return []
