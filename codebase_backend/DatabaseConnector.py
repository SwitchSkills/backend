import os
from typing import Dict, List, Any

from flask import g
from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy import text

from codebase_backend import logger, DEBUG
from codebase_backend.SingletonMeta import SingletonMeta
from config.ConfigWrapper import ConfigWrapper
from custom_exceptions.QueryConstructionError import QueryConstructionError
from sql_files.sql_helper_functions import read_sql_file


class DatabaseConnector(metaclass=SingletonMeta):

    def __init__(self,config:ConfigWrapper, database_engine):
        self._config = config
        self._db_engine = database_engine
        self._sub_query_mapping: Dict[str,str] = {
            '{completed_jobs}': read_sql_file('completed_jobs', True),
            '{job_additional_information}': read_sql_file('job_additional_information', True),
            '{user_additional_information}': read_sql_file('user_additional_information',True),
            '{accepted_jobs}': read_sql_file('accepted_jobs', True)
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
            db=config.get_database_name(),
            ip_type=IPTypes.PUBLIC  # IPTypes.PRIVATE for private IP
        )

    def execute_query(self,filename:str,fetch_query = True, **kwargs) -> List[Dict[str,Any]]:

        with self._db_engine.connect() as conn:
            if fetch_query:
                result = conn.execute(text(self._get_query(filename, **kwargs))).mappings().all()
                result = [dict(row_mapping) for row_mapping in result]

                if DEBUG:
                    logger.info(f"id:{g.execution_id}\n"
                            f"{result}")
                    logger.info(f"id:{g.execution_id}\n"
                            f"{type(result)}:")
                    logger.info("_____________________________________________________")
                return result
            else:
                conn.execute(text(self._get_query(filename, **kwargs)))
                conn.commit()


    def _get_query(self,filename, **kwargs) -> str:
        plain_text_query = read_sql_file(filename)
        for key, value in self._sub_query_mapping.items():
            plain_text_query = plain_text_query.replace(key,value)
        for key, value in kwargs.items():
            plain_text_query = plain_text_query.replace(key,value)
        try:
            assert('{' not in plain_text_query)
            assert('}' not in plain_text_query)
        except AssertionError:
            raise QueryConstructionError(f"missed substitution in query:\n{plain_text_query}")
        if DEBUG:
            logger.info(f"id:{g.execution_id}\n"
                        f"{filename}:")
            logger.info(f"id:{g.execution_id}\n {plain_text_query}")
        return plain_text_query

    def sort_jobs(self,list_1, list_2, list_3) -> list[Dict[str,Any]]:
        tmp = self._sort_jobs_2(list_1,list_2)
        return self._sort_jobs_2(tmp, list_3)

    def _sort_jobs_2(self, list_1, list_2) -> list[Dict[str,Any]]:
        index_1 = 0
        index_2 = 0
        len_list_1 = len(list_1)
        len_list_2 = len(list_2)
        tmp = list()
        while True:
            if index_1 == len_list_1:
                tmp.extend(list_2[index_2:])
                return tmp
            elif index_2 == len_list_2:
                tmp.extend(list_1[index_1:])
                return tmp
            if list_1[index_1].get('datetime_utc') > list_2[index_2].get('datetime_utc'):
                tmp.append(list_1[index_1])
                index_1 += 1
            else:
                tmp.append(list_2[index_2])
                index_2 += 1
    @staticmethod
    def overlap(list_to_check,list_with_values) -> int:
        count = 0
        for value in list_with_values:
            if value in list_to_check:
                count+=1
        try:
            assert(count != 0)
        except AssertionError:
            QueryConstructionError("There is a bug in the recommended_jobs query\n"
                                   f"list_to_check (of job):{list_to_check}\n"
                                   f"list_with_values (of user): {list_with_values}"
            )
        return round(float(count)*100/len(list_with_values))

    """
    Quicksort
    """
    def sort_recommendations(self,recommendations, low_index = None, high_index = None) -> None:
        if high_index is None:
            high_index = len(recommendations) - 1
        if low_index is None:
            low_index = 0
        if low_index < high_index:
            spil_position = self._reposition_spil(recommendations, low_index, high_index)

            # recursive call on the left of pivot
            self.sort_recommendations(recommendations, low_index, spil_position - 1)

            # recursive call on the right of pivot
            self.sort_recommendations(recommendations, spil_position + 1, high_index)
        # function to find the partition position
    @staticmethod
    def _reposition_spil(recommendations, low_index, high_index) -> int:

        pivot = recommendations[high_index]
        secondary_index = low_index

        for index_loop in range(low_index, high_index):
            if recommendations[index_loop]['matching_score'] >= pivot['matching_score']:
                (recommendations[secondary_index], recommendations[index_loop]) = (
                    recommendations[index_loop], recommendations[secondary_index])
                secondary_index = secondary_index + 1

        (recommendations[secondary_index], recommendations[high_index]) = (
        recommendations[high_index], recommendations[secondary_index])
        return secondary_index

    def add_type(self,list_with_dict:List[Dict[str,Any]], type:str) -> None:
        if list_with_dict:
            for element in list_with_dict:
                element.update({
                    'type': type
                })

    def group_attributes_jobs(self,jobs) -> List[Dict[str,str]]:
        job_ids = list()
        tmp = list()
        for job in jobs:
            if id := job['job_id'] != job_ids:
                job_ids.append(id)
                tmp_job = job.copy()
                tmp_job['pictures'] = [{
                    'picture_location_firebase': job['picture_location_firebase'],
                    'picture_description': job['picture_description']
                }]
                tmp_job['labels'] = [{
                    'label_name': job['label_name'],
                    'label_description': job['label_description']
                }]
                tmp.append(tmp_job)
            else:
                duplicate_job = tmp[job_ids.index(id)]
                duplicate_job['pictures'].append({
                    'picture_location_firebase': job['picture_location_firebase'],
                    'picture_description': job['picture_description']
                })
                duplicate_job['labels'].append({
                    'label_name': job['label_name'],
                    'label_description': job['label_description']
                })
        return tmp

    def group_attributes_user(self,users) -> List[Dict[str,str]]:
        user_ids = list()
        tmp = list()
        for user in users:
            if id := user['user_id'] != user_ids:
                user_ids.append(id)
                tmp_user = user.copy()
                tmp_user['regions'] = [{
                    'region_name': user['region_name'],
                    'country': user['country']
                }]
                tmp_user['labels'] = [{
                    'label_name': user['label_name'],
                    'label_description': user['label_description']
                }]
                tmp.append(tmp_user)
            else:
                duplicate_user = tmp[user_ids.index(id)]
                duplicate_user['regions'].append({
                    'region_name': user['region_name'],
                    'country': user['country']
                })
                duplicate_user['labels'].append({
                    'label_name': user['label_name'],
                    'label_description': user['label_description']
                })
        return tmp
