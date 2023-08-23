import os

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from structlog import get_logger

from codebase_backend.CredentialsFactory import CredentialsFactory
from codebase_backend.DatabaseConnector import DatabaseConnector
from config.ConfigWrapper import ConfigWrapper

logger = get_logger()
config = ConfigWrapper("config")
app = Flask(__name__)

# configure Flask-SQLAlchemy to use Python Connector
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "creator": DatabaseConnector.get_conn
}

# initialize the app with the extension
db = SQLAlchemy()
db.init_app(app)
database_connection = DatabaseConnector(config,db)
credentials_factory = CredentialsFactory()

g.reading_counter_variable = 0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",8080)))
