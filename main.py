from flask import Flask, render_template, url_for, request

app = Flask(__name__)

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
        print(request.form["username"])
    return render_template("contact.html", title="Обратная связь", menu=menu)


@app.route("/profile/<username>")
def profile(username):
    return f"User: {username}"


if __name__ == "__main__":
    app.run(debug=True)

