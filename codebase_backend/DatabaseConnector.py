from typing import Dict

import pandas as pd
from google.cloud.sql.connector import Connector, IPTypes

from codebase_backend.SingletonMeta import SingletonMeta
from config.ConfigWrapper import ConfigWrapper
from custom_exceptions.QueryConstructionError import QueryConstructionError
from sql_files.sql_helper_functions import read_sql_file


class DatabaseConnector(metaclass=SingletonMeta):

    def __init__(self,config:ConfigWrapper, database_connector):
        self._config = config
        self._db_conn = database_connector
        self._sub_query_mapping: Dict[str,str] = {
            '{completed_jobs}': read_sql_file('completed_jobs', True),
            '{job_additional_information}': read_sql_file('job_additional_information', True),
            '{user_additional_information}': read_sql_file('user_additional_information',True),
            '{user_search_first_name}': read_sql_file('user_search_first_name}',True),
            '{user_search_full_name}': read_sql_file('user_search_full_name', True),
            '{user_search_last_name': read_sql_file('user_search_last_name', True)
        }

    @staticmethod
    def get_conn():
        connector = Connector()
        config = ConfigWrapper("config")
        return connector.connect(
            config.get_SQL_instance_connection_name(),  # Cloud SQL Instance Connection Name
            "pymysql",
            user=config.get_database_role_user_name(),
            password=config.get_database_role_password(),
            db="my-database",
            ip_type=IPTypes.PUBLIC  # IPTypes.PRIVATE for private IP
        )

    def execute_query(self,filename:str,**kwargs) -> pd.DataFrame:

        result = self._db_conn.engine.execute(self._get_query(filename, **kwargs))
        print(result)
        return pd.DataFrame()
    def _get_query(self,filename, **kwargs) -> str:
        raw_sql = read_sql_file(filename)
        template_sql = str()
        for key, value in self._sub_query_mapping:
            template_sql = raw_sql.replace(key,value)
        for key, value in kwargs:
            plain_text_query = template_sql.replace(key,value)
        try:
            assert('{' not in plain_text_query)
            assert('}' not in plain_text_query)
        except AssertionError:
            raise QueryConstructionError(plain_text_query)
        return plain_text_query