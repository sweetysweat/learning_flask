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

    def add_post(self, title, text, url):
        try:
            self.__cursor.execute(f"SELECT COUNT() as 'count' FROM posts WHERE url LIKE '{url}'")
            res = self.__cursor.fetchone()
            if res["count"] != 0:
                print("Статья с таким url уже существует")
                return False

            tm = math.floor(time.time())
            self.__cursor.execute("INSERT INTO posts VALUES (NULL, ?, ?, ?, ?)", (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД", str(e))
            return False
        return True

    def get_post(self, alias):
        try:
            self.__cursor.execute(f"SELECT title, text FROM posts WHERE url LIKE ? LIMIT 1", (alias,))
            res = self.__cursor.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД", str(e))
        return False, False

    def get_post_annonce(self):
        try:
            self.__cursor.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
            res = self.__cursor.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД", str(e))
        return []

    def add_user(self, name, email, psw_hash):
        try:
            self.__cursor.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cursor.fetchone()
            if res["count"] > 0:
                print("Пользователь с таким email уже существует")
                return False
            tm = math.floor(time.time())
            self.__cursor.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?)", (name, email, psw_hash, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления в БД", e)
            return False
        return True

    def get_user(self, user_id):
        try:
            self.__cursor.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cursor.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД", e)
        return False

    def get_user_by_email(self, email):
        try:
            self.__cursor.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cursor.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД", e)
        return False
