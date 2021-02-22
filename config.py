import os

class CovidDatabase:
    COVID_DBPARAMS = {          # Docker-compose config

        "WEBDB_ENV_MYSQL_DB_HOST": os.environ.get("WEBDB_ENV_MYSQL_DB_HOST", "covidwebdb"),
        "WEBDB_ENV_MYSQL_PORT": os.environ.get("WEBDB_ENV_MYSQL_PORT", "3306"),
        "WEBDB_ENV_MYSQL_DATABASE": os.environ.get(
            "WEBDB_ENV_MYSQL_DATABASE", "coviddb"
        ),
        "WEBDB_ENV_MYSQL_USER": os.environ.get("WEBDB_ENV_MYSQL_USER", "root"),
        "WEBDB_ENV_MYSQL_PASSWORD": os.environ.get(
            "WEBDB_ENV_MYSQL_PASSWORD", "admin123"
        ),
    }
    # COVID_DBPARAMS = {        # local config
    #
    #     "WEBDB_ENV_MYSQL_DB_HOST": os.environ.get("WEBDB_ENV_MYSQL_DB_HOST", "localhost"),
    #     "WEBDB_ENV_MYSQL_PORT": os.environ.get("WEBDB_ENV_MYSQL_PORT", "3306"),
    #     "WEBDB_ENV_MYSQL_DATABASE": os.environ.get(
    #         "WEBDB_ENV_MYSQL_DATABASE", "coviddb"
    #     ),
    #     "WEBDB_ENV_MYSQL_USER": os.environ.get("WEBDB_ENV_MYSQL_USER", "root"),
    #     "WEBDB_ENV_MYSQL_PASSWORD": os.environ.get(
    #         "WEBDB_ENV_MYSQL_PASSWORD", "bismillah"
    #     ),
    # }
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://{WEBDB_ENV_MYSQL_USER}:{WEBDB_ENV_MYSQL_PASSWORD}@"
        "{WEBDB_ENV_MYSQL_DB_HOST}:{WEBDB_ENV_MYSQL_PORT}/"
        "{WEBDB_ENV_MYSQL_DATABASE}".format(**COVID_DBPARAMS)
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class CovidWeb(CovidDatabase):
    PORT = os.environ.get("PORT",5000)
    HOST = os.environ.get("HOST", 'http://0.0.0.0')
    DEBUG = False