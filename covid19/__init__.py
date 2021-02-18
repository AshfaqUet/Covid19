from flask import Flask
from config import CovidWeb
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(CovidWeb)
    db.init_app(app)
    db.app = app

    # BluePrints
    from covid19.covid_api import covid_api         # importing blueprint
    app.register_blueprint(covid_api)         # registering the blueprint

    # from web.users import users             # importing blueprint
    # app.register_blueprint(users)         # registering the blueprint
    return app

