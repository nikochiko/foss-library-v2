from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def not_found_error(e):
    return render_template("404.html"), 404
