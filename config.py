class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = "mysql://b9ab4a01ee401a:c72942a5@us-cdbr-east-05.cleardb.net/heroku_900b184db8de02d"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 300
    SECRET_KEY = "horrible_secret_key"
    LOGIN_DISABLED = True

