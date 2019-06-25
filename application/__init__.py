from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
# import jinja2

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

# app.jinja_env.filters['zip'] = zip

from application import routes, models
