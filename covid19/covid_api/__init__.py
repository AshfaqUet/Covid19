from flask import Blueprint

covid_api = Blueprint("covid_api", __name__)

from covid19.covid_api import fetch_api,get_api
