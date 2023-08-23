from flask import request, g
import json
from app import app, logger
from app import database_connection
from app import credentials_factory
from codebase_backend.decorators import catch_sever_crash
from sql_files.sql_helper_functions import get_sql_list

"""
path "/activity_feed" will return the content for the mainscreen: all open jobs and completed jobs 
ordered by time (earliest will be index 0). Expecting following dictionary in JSON:
(list of dictionaries)
region_name (str)
country (str)
REQUIREMENTS:
regions exists
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (list of dictionaries dictionary)
datetime_utc
type (open, accepted, completed)
job (dictionary)
    title (str)
    job_description (str)
    job_location (str)
region (dictionary)
    region_name (str)
    country (str)
picture [OPTIONAL] (list_of_dictionaries) 
    picture_location_firebase 
    picture_description [OPTIONAL]
labels (list_of_dictionaries)
    labels.label_name
    labels.description [OPTIONAL]
owner
    first_name
    last_name
    email_address
    alternative_communication [OPTIONAL]
    phone_number
    user_location
helper (only for completed)
    first_name
    last_name
    email_address
    alternative_communication [OPTIONAL]
    phone_number
    user_location
"""
@app.get('/activity_feed')
@catch_sever_crash
def activity_feed():
    arguments = request.get_json()
    try:
        region_id_list = get_sql_list([credentials_factory.get_region_id(region['country'],region['region_name']) for region in arguments])
    except KeyError as e:
        logger.error(g.execution_id, "KEY ERROR", e)
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{region_id_list}': region_id_list
    }

    completed_jobs_in_region_dataframe = database_connection('completed_jobs_in_region', **mapping)
    active_jobs_in_region_dataframe = database_connection('jobs_in_region', **mapping)
    accepted_jobs_in_region = database_connection('accepted_jobs_in_region',**mapping)
    database_connection.add_type(completed_jobs_in_region_dataframe, 'completed')
    database_connection.add_type(active_jobs_in_region_dataframe,'open')
    database_connection.add_type(accepted_jobs_in_region,'accepted')
    return json.dumps(database_connection.sort_jobs(completed_jobs_in_region_dataframe,active_jobs_in_region_dataframe, accepted_jobs_in_region))


"""
path "/active_jobs_in_region" will return the content for all open jobs: ordered by time (earliest will be index 0).
Expecting following dictionary in JSON:
regions (list of dictionaries)
    region_name (str)
    country (str)
REQUIREMENTS:
regions exists
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (list of dictionaries dictionary)
datetime_utc
job (dictionary)
    title (str)
    job_description (str)
    job_location (str)
region (dictionary)
    region_name (str)
    country (str)
picture [OPTIONAL] (list_of_dictionaries) 
    picture_location_firebase 
    picture_description [OPTIONAL]
labels (list_of_dictionaries)
    labels.label_name
    labels.description [OPTIONAL]
owner
    first_name
    last_name
    email_address
    alternative_communication [OPTIONAL]
    phone_number
    user_location
"""
@app.get('/active_jobs_in_region')
@catch_sever_crash
def active_jobs_in_region():

    arguments = request.get_json()
    try:
        region_id_list = get_sql_list(
            [credentials_factory.get_region_id(region['country'], region['region_name']) for region in arguments])
    except KeyError as e:
        logger.error(g.execution_id, "KEY ERROR", e)
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{region_id_list}': region_id_list
    }
    return json.dumps(database_connection('jobs_in_region', **mapping))

"""
path "/completed_jobs_by_user" will return the content for the completed jobs in profile menu: ordered by time 
(earliest will be index 0). Expecting following dictionary in JSON:
first_name
last_name
REQUIREMENTS:
user exists
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (list of dictionaries dictionary)
datetime_utc
job (dictionary)
    title (str)
    job_description (str)
    job_location (str)
region (dictionary)
    region_name (str)
    country (str)
picture [OPTIONAL] (list_of_dictionaries) 
    picture_location_firebase 
    picture_description [OPTIONAL]
labels (list_of_dictionaries)
    labels.label_name
    labels.description [OPTIONAL]
owner
    first_name
    last_name
    email_address
    alternative_communication [OPTIONAL]
    phone_number
    user_location
"""
@app.get('/completed_jobs_by_user')
@catch_sever_crash
def completed_jobs_by_user():
    arguments = request.get_json()
    try:
        user_id = credentials_factory.get_user_id(arguments['first_name'],arguments['last_name'])
    except KeyError as e:
        logger.error(g.execution_id, "KEY ERROR", e)
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{user_id}': user_id,
        '{pending}': 'FALSE'
    }
    return json.dumps(database_connection('user_completed_jobs', **mapping))

"""
path "/accepted_jobs_by_user" will return the content for the pending jobs in profile menu: ordered by time 
(earliest will be index 0). Expecting following dictionary in JSON:
first_name
last_name
REQUIREMENTS:
user exists
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (list of dictionaries dictionary)
datetime_utc
job (dictionary)
    title (str)
    job_description (str)
    job_location (str)
region (dictionary)
    region_name (str)
    country (str)
picture [OPTIONAL] (list_of_dictionaries) 
    picture_location_firebase 
    picture_description [OPTIONAL]
labels (list_of_dictionaries)
    labels.label_name
    labels.description [OPTIONAL]
owner
    first_name
    last_name
    email_address
    alternative_communication [OPTIONAL]
    phone_number
    user_location
"""
@app.get('/accepted_jobs_by_user')
@catch_sever_crash
def accepted_jobs_by_user():
    arguments = request.get_json()
    try:
        user_id = credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])
    except KeyError as e:
        logger.error(g.execution_id, "KEY ERROR", e)
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{user_id}': user_id,
        '{pending}': 'TRUE'
    }
    return json.dumps(database_connection('user_completed_jobs', **mapping))


"""
path "/liked_jobs_by_user" will return the content for the liked jobs in profile menu: ordered by time 
(earliest will be index 0). Expecting following dictionary in JSON:
first_name
last_name
REQUIREMENTS:
user exists
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (list of dictionaries dictionary)
datetime_utc
job (dictionary)
    title (str)
    job_description (str)
    job_location (str)
region (dictionary)
    region_name (str)
    country (str)
picture [OPTIONAL] (list_of_dictionaries) 
    picture_location_firebase 
    picture_description [OPTIONAL]
labels (list_of_dictionaries)
    labels.label_name
    labels.description [OPTIONAL]
owner
    first_name
    last_name
    email_address
    alternative_communication [OPTIONAL]
    phone_number
    user_location
"""
@app.get('/liked_jobs_by_user')
@catch_sever_crash
def liked_jobs_by_user():
    arguments = request.get_json()
    try:
        user_id = credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])
    except KeyError as e:
        logger.error(g.execution_id, "KEY ERROR", e)
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{user_id}': user_id
    }
    return json.dumps(database_connection('user_liked_jobs', **mapping))


"""
path "/jobs_owned_by_user" will return the content for the liked jobs in profile menu: ordered by time 
(earliest will be index 0). Expecting following dictionary in JSON:
first_name
last_name
REQUIREMENTS:
user exists
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (list of dictionaries dictionary)
datetime_utc
job (dictionary)
    title (str)
    job_description (str)
    job_location (str)
region (dictionary)
    region_name (str)
    country (str)
picture [OPTIONAL] (list_of_dictionaries) 
    picture_location_firebase 
    picture_description [OPTIONAL]
labels (list_of_dictionaries)
    labels.label_name
    labels.description [OPTIONAL]
owner (would send so you can keep reusing the feed you made + shows how others see as well) 
    first_name
    last_name
    email_address
    alternative_communication [OPTIONAL]
    phone_number
    user_location
"""
@app.get('/jobs_owned_by_user')
@catch_sever_crash
def jobs_owned_by_user():
    arguments = request.get_json()
    try:
        user_id = credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])
    except KeyError as e:
        logger.error(g.execution_id, "KEY ERROR", e)
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{user_id}': user_id
    }
    return json.dumps(database_connection('user_owns_jobs', **mapping))
"""
path "/all_users_in_region" will return the content for all users in region. Expecting following dictionary in JSON:
(list of dictionaries)
region_name (str)
country (str)
REQUIREMENTS:
regions exists
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (list of dictionaries dictionary)
region (dictionary)
    region_name (str)
    country (str)
picture [OPTIONAL] (dictionary) 
    picture_location_firebase 
    picture_description [OPTIONAL]
labels (list_of_dictionaries)
    labels.label_name
    labels.description [OPTIONAL]
user
    first_name
    last_name
    email_address
    alternative_communication [OPTIONAL]
    phone_number
    user_location
"""
@app.get('/all_users_in_region')
@catch_sever_crash
def all_users_in_region():
    arguments = request.get_json()
    try:
        region_id_list = get_sql_list(
            [credentials_factory.get_region_id(region['country'], region['region_name']) for region in arguments])
    except KeyError as e:
        logger.error(g.execution_id, "KEY ERROR", e)
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{region_id_list}': region_id_list
    }
    return json.dumps(database_connection.execute_query('users_in_region'),**mapping)

"""
path "/search_job" will return the searched items. Expecting following dictionary in JSON:
region (list of dictionaries)
    country (str)
    region_name (str)
type (description,owner,skills,skills_description,title)
(following key is depending on type) (everything can be substring) 
search = description 
OR
search = first_name+last_name
OR
search = skill
OR
search = skill description 
OR
search = title 
REQUIREMENTS:
/
ON SUCCESS (list of dictionaries dictionary) (can be empty list)
datetime_utc
job (dictionary)
    title (str)
    job_description (str)
    job_location (str)
region (dictionary)
    region_name (str)
    country (str)
picture [OPTIONAL] (list_of_dictionaries) 
    picture_location_firebase 
    picture_description [OPTIONAL]
labels (list_of_dictionaries)
    labels.label_name
    labels.description [OPTIONAL]
owner
    first_name
    last_name
    email_address
    alternative_communication [OPTIONAL]
    phone_number
    user_location
"""
@app.get('/search_jobs')
@catch_sever_crash
def search_jobs():

    arguments = request.get_json()
    try:
        search_query = 'search_jobs_on_' + arguments['type']
        region_id_list = get_sql_list(
            [credentials_factory.get_region_id(region['country'], region['region_name']) for region in arguments['region']])
        mapping = {
            '{region_id_list}': region_id_list,
        }
        if arguments['type'] == 'full_name':
            mapping.update( {
                '{search_first_name}': arguments['first_name'] if arguments['first_name'] else str(),
                '{search_last_name}': arguments['last_name'] if arguments['last_name'] else str()
            })
        else:
            mapping.update({
                '{search}': arguments['search']
            })
    except KeyError as e:
        logger.error(g.execution_id, "KEY ERROR", e)
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    return json.dumps(database_connection.execute_query(search_query,**mapping))

"""
path "/search_users" will return the search user. Expecting following dictionary in JSON:
type (full_name, bibliography, email_address, phone_number)
(following key is depending on type) (everything can be substring)
first_name (one or both)
last_name (one or both)
OR
search = bibliography 
OR
search = email 
OR
search = phone_number 
REQUIREMENTS:
/
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (list of dictionaries dictionary) (can be empty list)
region (dictionary)
    region_name (str)
    country (str)
picture [OPTIONAL] (dictionary) 
    picture_location_firebase 
    picture_description [OPTIONAL]
labels (list_of_dictionaries)
    labels.label_name
    labels.description [OPTIONAL]
user
    first_name
    last_name
    email_address
    alternative_communication [OPTIONAL]
    phone_number
    user_location
"""
@app.get('/search_users')
@catch_sever_crash
def search_users():
    #(full_name, bibliography, email_address, phone_number)
    arguments = request.get_json()
    try:
        search_query = 'search_users_on_' + arguments['type']
        if arguments['type'] == 'full_name':
            mapping = {
                '{search_first_name}' : arguments['first_name'] if arguments['first_name'] else str(),
                '{search_last_name}': arguments['last_name'] if arguments['last_name'] else str()
            }
        else:
            mapping = {
                '{search}': arguments['search']
            }
    except KeyError as e:
        logger.error(g.execution_id, "KEY ERROR", e)
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    return json.dumps(database_connection.execute_query(search_query, **mapping))
"""
path "/match_jobs" will return the jobs that are a match for the user: ordered by match quality sub-ordered on time 
(earliest will be index 0). Expecting following dictionary in JSON:
first_name
last_name
REQUIREMENTS:
user exists
ON SUCCESS (list of dictionaries dictionary) (can be empty list)
datetime_utc
job (dictionary)
    title (str)
    job_description (str)
    job_location (str)
region (dictionary)
    region_name (str)
    country (str)
picture [OPTIONAL] (list_of_dictionaries) 
    picture_location_firebase 
    picture_description [OPTIONAL]
labels (list_of_dictionaries)
    labels.label_name
    labels.description [OPTIONAL]
owner
    first_name
    last_name
    email_address
    alternative_communication [OPTIONAL]
    phone_number
    user_location
"""
@app.get('/match_jobs')
@catch_sever_crash
def match_jobs():
    arguments = request.get_json()
    try:
        user_id = credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])
    except KeyError as e:
        logger.error(g.execution_id, "KEY ERROR", e)
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{user_id}': user_id,
    }
    relevant_jobs = database_connection.execute_query('recommended_jobs', **mapping)
    skills_user = database_connection.execute_query('labels_by_user',**mapping)

    [job.update({
                'matching_score': database_connection.overlap([label['label_name'] for label in job['labels']], skills_user)
                })
                for job in relevant_jobs]

    database_connection.sort_recommendations(relevant_jobs)
    return relevant_jobs
