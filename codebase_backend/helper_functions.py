import json
from typing import Dict, Any, Union, List, cast

import pymysql.err
from sqlalchemy.exc import ResourceClosedError

from codebase_backend import logger
from codebase_backend.CredentialsFactory import CredentialsFactory
from codebase_backend.DatabaseConnector import DatabaseConnector
from codebase_backend.semaphores import user_lock, picture_lock, region_lock, job_lock, label_user_lock, \
    label_job_lock
from sql_files.sql_helper_functions import get_sql_list, read_sql_file


def verify_labels(database_connection:DatabaseConnector, arguments: Dict[str,Union[str, List[Dict[str,str]]]]) -> list:
    mapping_verifying_labels = {
        '{label_name_list}': get_sql_list([f"'{label['label_name']}'" for label in arguments['labels']])
    }

    verified_labels = database_connection.execute_query('validate_label', **mapping_verifying_labels)

    if len(verified_labels) != len(arguments['labels']):
        return verified_labels
    else:
        return list()

def verify_regions(credentials_factory: CredentialsFactory, database_connection: DatabaseConnector,arguments: Dict[str,Union[str, List[Dict[str,str]]]]) -> list:
    mapping_verifying_regions = {
        '{region_id_list}': get_sql_list(
            [f"'{credentials_factory.get_region_id(region['country'], region['region_name'])}'" for region in
             arguments['regions']])
    }
    verified_regions = database_connection.execute_query('validate_region', **mapping_verifying_regions)
    if len(verified_regions) != len(arguments['regions']):
        return verified_regions
    else:
        return list()


def get_user_mapping(database_connection:DatabaseConnector,credentials_factory: CredentialsFactory, arguments: Dict[str,Union[str, List[Dict[str,str]]]])-> dict:
    tmp = {
        '{user_id}': f"'{credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])}'",
        '{first_name}': f"'{arguments['first_name']}'",
        '{last_name}': f"'{arguments['last_name']}'",
        '{email_address}': f"'{arguments['email_address']}'",
        '{phone_number}': f"'{arguments['phone_number']}'",
        '{location}': f"'{arguments['location']}'"
    }
    if arguments.get('password'):
        tmp['{password}'] = f"'{credentials_factory.hash_string(arguments['password'])}'"
    else:
        tmp['{password}'] = f"'{database_connection.execute_query('get_password', **tmp)[0]['password']}'"
    return tmp


def update_user_mapping_with_optional_information(mapping: Dict[str,str], arguments: Dict[str,Union[str, List[Dict[str,str]]]]) -> None:
    if arguments.get('alternative_communications') :
        mapping.update({
            '{alternative_communication_key}' : ",alternative_communication",
            '{alternative_communication_content}': f",'{arguments['alternative_communications']}'"
        })
    else:
        mapping.update({
            '{alternative_communication_key}': str(),
            '{alternative_communication_content}': str()
        })
    if arguments.get('bibliography'):
        mapping.update({
            '{bibliography_key}': ",bibliography",
            '{bibliography_content}': f",'{arguments['bibliography']}'"
        })
    else:
        mapping.update({
            '{bibliography_key}': str(),
            '{bibliography_content}': str()
        })
    if arguments.get('rating'):
        mapping.update({
            '{rating_key}': ",rating",
            '{rating_content}': f",'{arguments['rating']}'"
        })
    else:
        mapping.update({
            '{rating_key}': str(),
            '{rating_content}': str()
        })
    if arguments.get('number_of_ratings'):
        mapping.update({
            '{number_of_ratings_key}': ",number_of_ratings",
            '{number_of_ratings_content}': f",'{arguments['number_of_ratings']}'"
        })
    else:
        mapping.update({
            '{number_of_ratings_key}': str(),
            '{number_of_ratings_content}': str()
        })

def verify_and_insert_user(credentials_factory: CredentialsFactory ,database_connection: DatabaseConnector, arguments:Dict[str,Union[str, List[Dict[str,str]]]]) -> str:
    try:
        if arguments.get('labels'):
            if verified_labels := verify_labels(database_connection,arguments):
                return json.dumps({
                    'code': 400,
                    'message': f"invalid labels!\n"
                               f"given_labels:{[label['label_name'] for label in arguments['labels']]}\n"
                               f"verified_labels:{verified_labels}"
                })

        if verified_regions := verify_regions(credentials_factory,database_connection,arguments):
            return json.dumps({
                'code': 400,
                'message': f"invalid regions!\n"
                           f"given_regions:{[(region['country'],region['region_name']) for region in arguments['regions']]}\n"
                           f"verified_labels:{[(region['country'],region['region_name']) for region in verified_regions]}"
            })

        mapping_user = get_user_mapping(database_connection,credentials_factory,arguments)
    except KeyError as e:
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    update_user_mapping_with_optional_information(mapping_user,arguments)
    user_lock.acquire()
    try:
        database_connection.execute_query(['delete_user', 'insert_user'],False,**mapping_user)
    finally:
        user_lock.release()
    return str()

def get_picture_mapping(credentials_factory: CredentialsFactory,arguments:Dict[str,Union[str, List[Dict[str,str]]]]):
    picture_dict = cast(Dict[str,str],arguments['picture'])
    return {
                '{picture_id}' : f"'{credentials_factory.get_picture_id(picture_dict['picture_location_firebase'])}'",
                '{picture_location_firebase}': f"'{picture_dict['picture_location_firebase']}'",
                '{user_id_key}': ",user_id",
                '{user_id_content}': f",'{credentials_factory.get_user_id(arguments['first_name'],arguments['last_name'])}'",
                '{job_id_key}': str(),
                '{job_id_content}': str()
            }

def update_picture_mapping_with_optional_information(mapping_picture: Dict[str,str], arguments:Dict[str,Union[str, List[Dict[str,str]]]]):
    picture_dict = cast(Dict[str, str], arguments['picture'])
    if picture_dict.get('description'):
        mapping_picture.update(
            {
                '{description_key}': ",description",
                '{description_content}': f",'{picture_dict['description']}'"
            }
        )
    else:
        mapping_picture.update(
            {
                '{description_key}': str(),
                '{description_content}': str()
            }
        )
def insert_picture_user(credentials_factory: CredentialsFactory, database_connection: DatabaseConnector, arguments:Dict[str,Union[str, List[Dict[str,str]]]]) -> str:

    try:
        mapping_picture = get_picture_mapping(credentials_factory,arguments)
    except KeyError as e:
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    update_picture_mapping_with_optional_information(mapping_picture,arguments)
    picture_lock.acquire()
    try:
        database_connection.execute_query('insert_picture',False,**mapping_picture)
    finally:
        picture_lock.release()
    return str()
def insert_labels_user(credentials_factory: CredentialsFactory, database_connection: DatabaseConnector, arguments:Dict[str,Union[str, List[Dict[str,str]]]]):
    user_id = credentials_factory.get_user_id(arguments['first_name'],arguments['last_name'])
    if len(arguments["labels"])> 1:
        label_list = [
            get_sql_list([f"'{user_id}'", f"'{label['label_name']}'"]) for label in arguments['labels']
        ]
        mapping = {
            '{label_list}': ",".join(label_list)
        }
        label_user_lock.acquire()
        try:
            database_connection.execute_query('insert_labels_user',False,**mapping)
        finally:
            label_user_lock.release()
    else:
        label_name = arguments["labels"][0]['label_name']
        mapping = {
            "{user_id}": f"'{user_id}'",
            "{label_name}": f"'{label_name}'"
        }
        label_user_lock.acquire()
        try:
            database_connection.execute_query('insert_label_user', False, **mapping)
        finally:
            label_user_lock.release()


def insert_regions_user(credentials_factory: CredentialsFactory, database_connection: DatabaseConnector, arguments:Dict[str,Union[str, List[Dict[str,str]]]]):
    user_id = f"{credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])}"
    if len(arguments['regions'])>1:
        region_list = [
            get_sql_list([f"'{user_id}'", f"'{credentials_factory.get_region_id(region['country'], region['region_name'])}'"]) for region in arguments['regions']
        ]
        mapping = {
            '{region_list}': ",".join(region_list)
        }
        region_lock.acquire()
        try:
            database_connection.execute_query('insert_regions_user',False,**mapping)
        finally:
            region_lock.release()
    else:
        region_id = credentials_factory.get_region_id(arguments['regions'][0]['country'], arguments['regions'][0]['region_name'])

        mapping = {
            '{user_id}': f"'{user_id}'",
            '{region_id}': f"'{region_id}'"
        }
        region_lock.acquire()
        try:
            database_connection.execute_query('insert_region_user', False, **mapping)
        finally:
            region_lock.release()

def get_change_user_name_mapping(credentials_factory: CredentialsFactory, arguments:Dict[str,Union[str, List[Dict[str,str]]]]):
    existing_user_id = f"'{credentials_factory.get_user_id(arguments['existing_first_name'],arguments['existing_last_name'])}'"
    new_user_id = f"'{credentials_factory.get_user_id(arguments['new_first_name'], arguments['new_last_name'])}'"
    return {
            '{existing_user_id}': existing_user_id,
            '{new_first_name}': f"'{arguments['new_first_name']}'",
            '{new_last_name}': f"'{arguments['new_last_name']}'",
            '{new_user_id}': new_user_id
        }

def verify_and_insert_job(credentials_factory: CredentialsFactory ,database_connection: DatabaseConnector, arguments:Dict[str,Union[str, List[Dict[str,str]]]]) -> str:
    try:
        if verified_labels := verify_labels(database_connection,arguments):
            return json.dumps({
                'code': 400,
                'message': f"invalid labels!\n"
                           f"given_labels:{[label['label_name'] for label in arguments['labels']]}\n"
                           f"verified_labels:{verified_labels}"
            })
        if verified_regions := verify_regions(credentials_factory,database_connection,arguments):
            return json.dumps({
                'code': 400,
                'message': f"invalid regions!\n"
                           f"given_regions:{[(region['country'],region['region_name']) for region in arguments['regions']]}\n"
                           f"verified_labels:{[(region['country'],region['region_name']) for region in verified_regions]}"
            })

        mapping_job = get_job_mapping(credentials_factory,arguments)
    except KeyError as e:
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    update_job_mapping_with_optional_information(mapping_job,arguments)
    if database_connection.execute_query('search_completed_job', **mapping_job):
        logger.error(f"id: {g.execution_id}\n job is pending or completed: {mapping_job['{job_id}']}")
        return json.dumps(
            {
                'code': 400,
                'message': f"job is pending or completed: {mapping_job['{job_id}']}"
            }
        )
    job_lock.acquire()
    try:
        database_connection.execute_query(['delete_job','insert_job'],False,**mapping_job)
    except ResourceClosedError:
        pass
    finally:
        job_lock.release()
    return str()

def get_job_mapping(credentials_factory: CredentialsFactory, arguments: Dict[str,Union[str, List[Dict[str,str]]]])-> dict:
    user_id_owner = credentials_factory.get_user_id(arguments['first_name_owner'],arguments['last_name_owner'])
    region_id = credentials_factory.get_region_id(cast(Dict[str,str],arguments['region'])['country'],cast(Dict[str,str],arguments['region'])['region_name'])
    return {
        '{job_id}': f"'{credentials_factory.get_job_id(arguments['title'],user_id_owner,region_id)}'",
        '{description}' : f"'{arguments['description']}'",
        '{title}': f"'{arguments['title']}'",
        '{region_id}': f"'{region_id}'",
        '{user_id_owner}': f"'{user_id_owner}'",
        '{location}': f"'{arguments['location']}'"
    }

def update_job_mapping_with_optional_information(mapping,arguments :  Dict[str,Union[str, List[Dict[str,str]]]]):
    if arguments.get('datetime_made_utc') :
        mapping.update({
            '{datetime_made_utc_key}' : ',datetime_made_utc',
            '{datetime_made_utc_content}': f",'{arguments['datetime_made_utc']}'"
        })
    else:
        mapping.update({
            '{datetime_made_utc_key}': str(),
            '{datetime_made_utc_content}': str()
        })
    if arguments.get('datetime_expires_utc'):
        mapping.update({
            '{datetime_expires_utc_key}': ',datetime_expires_utc',
            '{datetime_expires_utc_content}': f",'{arguments['datetime_expires_utc']}'"
        })
    else:
        mapping.update({
            '{datetime_expires_utc_key}': str(),
            '{datetime_expires_utc_content}': str()
        })

def insert_pictures_job(credentials_factory: CredentialsFactory, database_connection: DatabaseConnector,arguments:Dict[str,Union[str, List[Dict[str,str]]]]) -> str:
    try:
        mapping_pictures = get_pictures_mapping_job(credentials_factory,arguments)
    except KeyError as e:
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    picture_lock.acquire()
    try:
        for mapping_picture, picture_argument in zip(mapping_pictures, arguments['pictures']):
            update_picture_mapping_with_optional_information(mapping_picture, {'picture':picture_argument})
            database_connection.execute_query('insert_picture',False,**mapping_picture)
    finally:
        picture_lock.release()
    return str()

def get_pictures_mapping_job(credentials_factory: CredentialsFactory, arguments:Dict[str,Union[str, List[Dict[str,str]]]]):
    picture_dicts = cast(List[Dict[str, str]], arguments['pictures'])
    user_id_owner = credentials_factory.get_user_id(arguments['first_name_owner'], arguments['last_name_owner'])
    region_id = credentials_factory.get_region_id(cast(Dict[str, str], arguments['region'])['country'],
                                                  cast(Dict[str, str], arguments['region'])['region_name'])
    return [{
        '{picture_id}': f"'{credentials_factory.get_picture_id(picture_dict['picture_location_firebase'])}'",
        '{picture_location_firebase}': f"'{picture_dict['picture_location_firebase']}'",
        '{user_id_key}': str(),
        '{user_id_content}': str(),
        '{job_id_key}': ',job_id',
        '{job_id_content}': f",'{credentials_factory.get_job_id(arguments['title'],user_id_owner,region_id)}'"
    } for picture_dict in picture_dicts]

def update_picture_job_mapping_with_optional_information(mapping_pictures: List[Dict[str,str]], arguments:[Dict[str,Union[str, List[Dict[str,str]]]]]):
    picture_dicts = cast(List[Dict[str, str]], arguments['picture'])
    for index, picture_dict in enumerate(picture_dicts):
        if picture_dict.get('description'):
            mapping_pictures[index].update(
                {
                    '{description_key}': ',description',
                    '{description_content}': f",'{picture_dict['description']}'"
                }
            )
        else:
            mapping_pictures[index].update(
                {
                    '{description_key}': str(),
                    '{description_content}': str()
                }
            )


def insert_labels_job(credentials_factory: CredentialsFactory, database_connection: DatabaseConnector, arguments:[Dict[str,Union[str, List[Dict[str,str]]]]]):
    user_id_owner = credentials_factory.get_user_id(arguments['first_name_owner'], arguments['last_name_owner'])
    region_id = credentials_factory.get_region_id(cast(Dict[str, str], arguments['region'])['country'],
                                                  cast(Dict[str, str], arguments['region'])['region_name'])
    job_id = credentials_factory.get_job_id(arguments['title'],user_id_owner,region_id)
    if len(arguments['labels']) > 1:
        label_list = [
            get_sql_list([f"'{job_id}'", f"'{label['label_name']}'"]) for label in arguments['labels']
        ]
        mapping = {
            '{label_list}': ",".join(label_list)
        }
        label_job_lock.acquire()
        try:
            database_connection.execute_query('insert_labels_job',False, **mapping)
        finally:
            label_job_lock.release()
    else:
        label_name = arguments['labels'][0]['label_name']
        mapping = {
            '{job_id}': f"'{job_id}'",
            '{label_name}': f"'{label_name}'"
        }
        label_job_lock.acquire()
        try:
            database_connection.execute_query('insert_label_job', False, **mapping)
        finally:
            label_job_lock.release()

def get_change_job_title_mapping(credentials_factory:CredentialsFactory, arguments:[Dict[str,Union[str, List[Dict[str,str]]]]]):
    user_id_owner = credentials_factory.get_user_id(arguments['first_name_owner'], arguments['last_name_owner'])
    region_id = credentials_factory.get_region_id(cast(Dict[str, str], arguments['region'])['country'],
                                                  cast(Dict[str, str], arguments['region'])['region_name'])

    existing_job_id = credentials_factory.get_job_id(arguments['existing_title'], user_id_owner, region_id)
    new_job_id = credentials_factory.get_job_id(arguments['new_title'], user_id_owner, region_id)
    return {
        '{existing_job_id}': f"'{existing_job_id}'",
        '{new_title}': f"'{arguments['new_title']}'",
        '{new_job_id}': f"'{new_job_id}'"
    }

def get_change_job_region_mapping(credentials_factory:CredentialsFactory, arguments:[Dict[str,Union[str, List[Dict[str,str]]]]]):
    user_id_owner = credentials_factory.get_user_id(arguments['first_name_owner'], arguments['last_name_owner'])
    current_region_id = credentials_factory.get_region_id(cast(Dict[str, str], arguments['current_region'])['country'],
                                                  cast(Dict[str, str], arguments['current_region'])['region_name'])
    new_region_id = credentials_factory.get_region_id(cast(Dict[str, str], arguments['new_region'])['country'],
                                                          cast(Dict[str, str], arguments['new_region'])[
                                                              'region_name'])
    existing_job_id = credentials_factory.get_job_id(arguments['title'],  user_id_owner, current_region_id)
    new_job_id = credentials_factory.get_job_id(arguments['title'], user_id_owner,new_region_id)
    print(new_job_id)
    return {
        '{existing_job_id}': f"'{existing_job_id}'",
        '{new_region_id}': f"'{new_region_id}'",
        '{new_job_id}': f"'{new_job_id}'"
    }


def search_user_mapping_and_query(arguments:[Dict[str,Union[str, List[Dict[str,str]]]]], login= False):
    mapping = {
        '{users_in_region}': read_sql_file('users_in_region') if not login else read_sql_file('login'),
        '{user_additional_information}': read_sql_file('user_additional_information', True),
        '{region_id_list}': read_sql_file('all_regions', True)
    }
    if login:
        base_string = "= '{content}'"
    else:
        base_string = "LIKE '%{content}%'"
    search_query = 'search_users_on_' + arguments['type']
    if arguments['type'] == 'full_name':
        mapping.update({
            '{search_first_name}': base_string.format(content = arguments['first_name']) if arguments.get('first_name') else base_string.format(content = str()),
            '{search_last_name}': base_string.format(content = arguments['last_name']) if arguments.get('last_name') else base_string.format(content=str())
        })
    else:
        mapping.update({
            '{search}': base_string.format(content = arguments['search'])
        })
    return mapping, search_query

def no_none_check_list_of_dict(list_of_dict):
    for dictionary in list_of_dict:
        if not no_none_check_dict(dictionary):
            return False
    return True
def no_none_check_dict(dictionary):
    for value in dictionary.values():
        if not value:
            return False
        elif type(value) == list:
            return no_none_check_list_of_dict(value)
        elif type(value) == dict:
            return no_none_check_dict(value)

    return True