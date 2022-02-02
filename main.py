import os
import sqlite3

from flask import Flask, g, render_template, request, flash, abort, redirect, url_for

from werkzeug.security import generate_password_hash, check_password_hash

from DataBase import DataBase

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from UserLogin import UserLogin

# конфигурация
DATABASE = ""
DEBUG = True
SECRET_KEY = "secret"

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, "flsite.db")))

login_manager = LoginManager(app)

login_manager.login_view = "login"
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"



@login_manager.user_loader
def load_user(user_id):
    print("load user")
    return UserLogin().from_db(user_id, dbase)


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase(db)


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
    return render_template("index.html", menu=dbase.get_menu(), posts=dbase.get_post_annonce(), title="Про Flask")


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
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
@login_required
def show_post(alias):
    title, post = dbase.get_post(alias)
    if not title:
        abort(404)
    return render_template("post.html", menu=dbase.get_menu(), title=title, post=post)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    if request.method == "POST":
        user = dbase.get_user_by_email(request.form["email"])
        if user and check_password_hash(user["psw"], request.form["psw"]):
            user_login = UserLogin().create(user)
            rm = True if request.form.get("remainme") else False
            login_user(user_login, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))
        flash("Неверный логин или пароль", "error")
    return render_template("login.html", menu=dbase.get_menu(), title="Авторизация")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form["name"]) > 4 and len(request.form["email"]) > 4 and len(request.form["psw"]) > 4 and \
                request.form["psw"] == request.form["psw2"]:
            psw_hash = generate_password_hash(request.form["psw"])
            res = dbase.add_user(request.form["name"], request.form["email"], psw_hash)
            if res:
                flash("Регистрация прошла успешно", "success")
                return redirect(url_for("login"))
            else:
                flash("Ошибка добавления данных в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")
    return render_template("register.html", menu=dbase.get_menu(), title="Регистрация")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли с аккаунта", "success")
    return redirect(url_for("login"))


@app.route("/profile")
@login_required
def profile():
    return f"""<p><a href="{url_for("logout")}">Выйти из профиля</a></p>
            <p>user info: {current_user.get_id()}</p>"""


if __name__ == "__main__":
    app.run(debug=True)
