import os
import sqlite3

from flask import Flask, g, render_template, request, flash, abort

from DataBase import DataBase

# конфигурация
DATABASE = ""
DEBUG = True
SECRET_KEY = "secret"

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, "flsite.db")))


def connect_db():
    connect = sqlite3.connect(app.config["DATABASE"])
    connect.row_factory = sqlite3.Row  # чтоб работать как со словарем
    return connect


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource("sq_db.sql", "r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route("/")
def index():
    db = get_db()
    dbase = DataBase(db)
    return render_template("index.html", menu=dbase.get_menu(), posts=dbase.get_post_annonce(), title="Про Flask")


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    db = get_db()
    dbase = DataBase(db)
    if request.method == "POST":
        if len(request.form["name"]) > 4 and len(request.form["post"]) > 10:
            res = dbase.add_post(request.form["name"], request.form["post"], request.form["url"])
            if not res:
                flash("Ошибка добавления статьи", category="error")
            else:
                flash("Статья добавлена успешно", category="success")
        else:
            flash("Ошибка добавления статьи", category="error")
    return render_template("add_post.html", menu=dbase.get_menu(), title="Добавление статьи")


@app.route("/post/<alias>")
def show_post(alias):
    db = get_db()
    dbase = DataBase(db)
    title, post = dbase.get_post(alias)
    if not title:
        abort(404)
    return render_template("post.html", menu=dbase.get_menu(), title=title, post=post)


if __name__ == "__main__":
    app.run(debug=True)
