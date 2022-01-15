from flask import Flask, render_template, url_for, request, flash, session, redirect, abort

app = Flask(__name__)

app.config["SECRET_KEY"] = "itsasecret"

menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Перове приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]


@app.route("/")
def index():
    return render_template("index.html", menu=menu)


@app.route("/about")
def about():
    return render_template("about.html", title="About", menu=menu)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form["username"]) > 2:
            flash("Сообщение отправлено", category="success")
        else:
            flash("Ошибка", category="error")
    return render_template("contact.html", title="Обратная связь", menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page404.html", title="Страница не найдена", menu=menu), 404


@app.route("/login", methods=["POST", "GET"])
def login():
    if "user_logged" in session:
        return redirect(url_for("profile", username=session["user_logged"]))
    elif request.method == "POST" and request.form["username"] == "111" and request.form["password"] == "111":
        session["user_logged"] = request.form["username"]
        return redirect(url_for("profile", username=session["user_logged"]))
    return render_template("login.html", title="Авторизация", menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if "user_logged" not in session or session["user_logged"] != username:
        abort(401)
    return f"User: {username}"


if __name__ == "__main__":
    app.run(debug=True)
