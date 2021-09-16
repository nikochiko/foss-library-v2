from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"

SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
    "postgres://", "postgresql://"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = env.str("SECRET_KEY")

SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT", default=300)

DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False


if ENV.lower() == "testing":
    WTF_CSRF_ENABLED = False
    assert SQLALCHEMY_DATABASE_URI.endswith(
        "_test"
    ), "DATABASE_URL should end in _test in testing environment"
