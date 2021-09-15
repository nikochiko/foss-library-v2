from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from pony.flask import Pony

csrf_protect = CSRFProtect()
pony = Pony()


def not_found_error(e):
    return render_template("404.html"), 404


def create_app(config_object="foss_library.settings"):
    """Flask app factory"""
    app = Flask(__name__)
    app.config.from_object(config_object)

    # initialise extensions
    csrf_protect.init_app(app)
    pony.init_app(app)

    # custom error handlers
    app.register_error_handler(404, not_found_error)
