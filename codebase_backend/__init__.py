from structlog import get_logger
from config.ConfigWrapper import ConfigWrapper
logger = get_logger()
config = ConfigWrapper("config")
DEBUG =False

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from codebase_backend.CredentialsFactory import CredentialsFactory
from codebase_backend.DatabaseConnector import DatabaseConnector



app = Flask(__name__)

# configure Flask-SQLAlchemy to use Python Connector
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "creator": DatabaseConnector.get_conn
}


# initialize the app with the extension
db = SQLAlchemy()
db.init_app(app)
with app.app_context():
    database_connection = DatabaseConnector(config,db.engine)
    credentials_factory = CredentialsFactory()

from codebase_backend import immutable_routes,mutable_routes, app_rules