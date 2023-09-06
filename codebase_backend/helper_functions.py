import json
from typing import Dict, Any, Union, List, cast

from sqlalchemy.exc import ResourceClosedError

from codebase_backend.CredentialsFactory import CredentialsFactory
from codebase_backend.DatabaseConnector import DatabaseConnector
from codebase_backend.semaphores import user_lock, picture_lock, region_lock, job_lock, label_user_lock, \
    label_job_lock
from sql_files.sql_helper_functions import get_sql_list


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


def get_user_mapping(credentials_factory: CredentialsFactory, arguments: Dict[str,Union[str, List[Dict[str,str]]]])-> dict:
    return {
        '{user_id}': f"'{credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])}'",
        '{first_name}': f"'{arguments['first_name']}'",
        '{last_name}': f"'{arguments['last_name']}'",
        '{email_address}': f"'{arguments['email_address']}'",
        '{phone_number}': f"'{arguments['phone_number']}'",
        '{password}': f"'{credentials_factory.hash_string(arguments['password'])}'",
        '{location}': f"'{arguments['location']}'"
    }


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

        mapping_user = get_user_mapping(credentials_factory,arguments)
    except KeyError as e:
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    update_user_mapping_with_optional_information(mapping_user,arguments)
    user_lock.acquire()
    database_connection.execute_query('delete_user',False,**mapping_user)
    database_connection.execute_query('insert_user',False,**mapping_user)
    user_lock.release()
    return dict()

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
def insert_picture_user(credentials_factory: CredentialsFactory, database_connection: DatabaseConnector, arguments:Dict[str,Union[str, List[Dict[str,str]]]]):

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
    database_connection.execute_query('delete_picture', False,**mapping_picture)
    database_connection.execute_query('insert_picture',False,**mapping_picture)
    picture_lock.release()

def insert_labels_user(credentials_factory: CredentialsFactory, database_connection: DatabaseConnector, arguments:Dict[str,Union[str, List[Dict[str,str]]]]):
    user_id = credentials_factory.get_user_id(arguments['first_name'],arguments['last_name'])
    label_list = [
        get_sql_list([f"'{user_id}'", f"'{label['label_name']}'"]) for label in arguments['labels']
    ]
    mapping = {
        '{label_list}': get_sql_list(label_list)
    }
    label_user_lock.acquire()
    database_connection.execute_query('insert_labels_user',False,**mapping)
    label_user_lock.release()


def insert_regions_user(credentials_factory: CredentialsFactory, database_connection: DatabaseConnector, arguments:Dict[str,Union[str, List[Dict[str,str]]]]):
    user_id = f"'{credentials_factory.get_user_id(arguments['first_name'], arguments['second_name'])}'"
    region_list = [
        get_sql_list([f"'{user_id}'", f"'{credentials_factory.get_region_id(region['country'], region['region_name'])}'"]) for region in arguments['regions']
    ]
    mapping = {
        '{region_list}': get_sql_list(region_list)
    }
    region_lock.acquire()
    database_connection.execute_query('insert_regions_user',False,**mapping)
    region_lock.release()

def get_change_user_name_mapping(credentials_factory: CredentialsFactory, arguments:Dict[str,Union[str, List[Dict[str,str]]]]):
    existing_user_id = f"'{credentials_factory.get_user_id(arguments['existing_first_name'],arguments['existing_last_name'])}'"
    return {
            '{existing_user_id}': existing_user_id,
            '{new_first_name}': f"'{arguments['new_first_name']}'",
            '{new_last_name}': f"'{arguments['new_last_name']}'"
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
    job_lock.acquire()
    try:
        database_connection.execute_query('delete_job',False,**mapping_job)
    except ResourceClosedError:
        pass
    database_connection.execute_query('insert_job',False,**mapping_job)
    job_lock.release()
    return dict()

def get_job_mapping(credentials_factory: CredentialsFactory, arguments: Dict[str,Union[str, List[Dict[str,str]]]])-> dict:
    user_id_owner = credentials_factory.get_user_id(arguments['first_name'],arguments['last_name'])
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

def insert_pictures_job(credentials_factory: CredentialsFactory, database_connection: DatabaseConnector,arguments:Dict[str,Union[str, List[Dict[str,str]]]]):
    try:
        mapping_pictures = get_pictures_mapping_job(credentials_factory,arguments)
    except KeyError as e:
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    update_picture_mapping_with_optional_information()
    picture_lock.acquire()
    for mapping_picture in mapping_pictures:
        database_connection.execute_query('insert_picture_user',False,**mapping_picture)
    picture_lock.release()

def get_pictures_mapping_job(credentials_factory: CredentialsFactory, arguments:Dict[str,Union[str, List[Dict[str,str]]]]):
    picture_dicts = cast(List[Dict[str, str]], arguments['picture'])
    user_id_owner = credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])
    region_id = credentials_factory.get_region_id(cast(Dict[str, str], arguments['region'])['country'],
                                                  cast(Dict[str, str], arguments['region'])['region_name'])
    return [{
        '{picture_id}': f"'{credentials_factory.get_picture_id(picture_dict['picture_location_firebase'])}'",
        '{picture_location_firebase}': f"'{picture_dict['picture_location_firebase']}'",
        '{user_id_key}': str(),
        '{user_id_content}': str(),
        '{job_id_key}': 'job_id',
        '{job_id_content}': f"'{credentials_factory.get_job_id(arguments['title'],user_id_owner,region_id)}'"
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
    user_id_owner = credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])
    region_id = credentials_factory.get_region_id(cast(Dict[str, str], arguments['region'])['country'],
                                                  cast(Dict[str, str], arguments['region'])['region_name'])
    job_id = credentials_factory.get_job_id(arguments['title'],user_id_owner,region_id)
    label_list = [
        get_sql_list([f"'{job_id}'", f"'{label['label_name']}'"]) for label in arguments['labels']
    ]
    mapping = {
        '{label_list}': get_sql_list(label_list)
    }
    label_job_lock.acquire()
    database_connection.execute_query('insert_labels_job',False, **mapping)
    label_job_lock.release()

def get_change_job_title_mapping(credentials_factory:CredentialsFactory, arguments:[Dict[str,Union[str, List[Dict[str,str]]]]]):
    existing_job_id = credentials_factory.get_user_id(arguments['existing_first_name'],
                                                       arguments['existing_last_name'])
    return {
        '{existing_job_id}': f"'{existing_job_id}'",
        '{new_title}': f"'{arguments['title']}'"
    }