import pandas as pd

from config.ConfigWrapper import ConfigWrapper


#TODO: make it singleton
class DataBaseWrapper:

    def __init__(self, config: ConfigWrapper):
        self._config = config
        pass

    def execute_query(self, file_name: str) -> pd.DataFrame:
        pass

    def __initialise_database_connection(self):
        pass
    def __authenticate_user(self):
        pass

    def __assume_role(self):
        pass