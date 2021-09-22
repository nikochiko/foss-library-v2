from flask import Flask, render_template
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from fosslib import books, frappe_api, members, public
from fosslib.database import db

csrf_protect = CSRFProtect()
migrate = Migrate()


def not_found_error(e):
    return render_template("404.html"), 404


def create_app(config_object="fosslib.settings", overrides=None):
    """Flask app factory"""
    app = Flask(__name__)
    app.config.from_object(config_object)

    if overrides is not None:
        app.config.update(overrides)

    # initialise extensions
    csrf_protect.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # custom error handlers
    app.register_error_handler(404, not_found_error)

    # register blueprints
    app.register_blueprint(books.views.blueprint)
    app.register_blueprint(frappe_api.views.blueprint)
    app.register_blueprint(members.views.blueprint)
    app.register_blueprint(public.views.blueprint)

    return app
