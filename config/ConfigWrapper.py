from structlog import BoundLogger
import yaml
from yaml.loader import SafeLoader

from codebase_backend.SingletonMeta import SingletonMeta
from custom_exceptions.ConfigReadError import ConfigReadError

"""
The ConfigWrapper class provides a wrapper for a YAML configuration file 
that contains parameters and settings for the email client and server.

"""

class ConfigWrapper(metaclass=SingletonMeta):
    def __init__(self,file_name: str):
        with open(f"config/{file_name}.yaml", "r") as config:
            try:
                # Converts yaml document to python object
                self._loaded_config_dictionary = yaml.load(config, Loader=SafeLoader)

            except yaml.YAMLError as e:
                raise ConfigReadError(f"Unable to load config file, error:\n"
                                      f"{e}")

    def get_project_id(self) -> str:
        return self._loaded_config_dictionary.get('project_id')

    def get_SQL_instance_region(self) ->str:
        return self._loaded_config_dictionary.get("database_region")

    def get_SQL_instance_name(self) -> str:
        return self._loaded_config_dictionary.get("database_instance_name")

    def get_SQL_instance_connection_name(self) -> str:
        return f"{self.get_project_id()}:{self.get_SQL_instance_region()}:{self.get_SQL_instance_name()}"

    def get_database_role_user_name(self) -> str:
        return self._loaded_config_dictionary.get("database_user").get("user_name")

    def get_database_role_password(self) -> str:
        return self._loaded_config_dictionary.get("database_user").get("password")

    def get_database_name(self) -> str:
        return self._loaded_config_dictionary.get("database_user").get("database_name")

