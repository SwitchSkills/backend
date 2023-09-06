from flask import request, g
import json

from codebase_backend import app, logger, credentials_factory, database_connection
from codebase_backend.decorators import catch_sever_crash
from sql_files.sql_helper_functions import get_sql_list, read_sql_file

@app.route('/')
def home():
  return 'Hello World'

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
pictures [OPTIONAL] (list_of_dictionaries) 
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
    print("in activity_feed")
    arguments = request.get_json()
    try:
        region_id_list = get_sql_list([f"'{credentials_factory.get_region_id(region['country'],region['region_name'])}'" for region in arguments])
    except KeyError as e:
        logger.error(f"id: {g.execution_id}\n KEY ERROR: {e}")
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{region_id_list}': region_id_list
    }
    print("to db conn")
    completed_jobs_in_region = database_connection.execute_query('completed_jobs_in_region', **mapping)
    open_jobs_in_region = database_connection.execute_query('jobs_in_region', **mapping)
    accepted_jobs_in_region = database_connection.execute_query('accepted_jobs_in_region',**mapping)
    database_connection.add_type(completed_jobs_in_region, 'completed')
    database_connection.add_type(open_jobs_in_region,'open')
    database_connection.add_type(accepted_jobs_in_region,'accepted')
    completed_jobs_in_region = database_connection.group_attributes_jobs(completed_jobs_in_region)
    open_jobs_in_region = database_connection.group_attributes_jobs(open_jobs_in_region)
    accepted_jobs_in_region = database_connection.group_attributes_jobs(accepted_jobs_in_region)
    result = database_connection.sort_jobs(completed_jobs_in_region,open_jobs_in_region, accepted_jobs_in_region)
    return json.dumps({'code':200, 'message': result}, default= str)


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
pictures [OPTIONAL] (list_of_dictionaries) 
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
            [f"'{credentials_factory.get_region_id(region['country'], region['region_name'])}'" for region in arguments])
    except KeyError as e:
        logger.error(f"id: {g.execution_id}\n KEY ERROR: {e}")
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{region_id_list}': region_id_list
    }
    result = database_connection.execute_query('jobs_in_region', **mapping)
    result = database_connection.group_attributes_jobs(result)
    return json.dumps({'code': 200, 'message': result},default=str)

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
pictures [OPTIONAL] (list_of_dictionaries) 
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
        user_id = f"'{credentials_factory.get_user_id(arguments['first_name'],arguments['last_name'])}'"
    except KeyError as e:
        logger.error(f"id: {g.execution_id}\n KEY ERROR: {e}")
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
    result = database_connection.execute_query('user_completed_jobs', **mapping)
    result = database_connection.group_attributes_jobs(result)
    return json.dumps({'code': 200, 'message':result},default=str)

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
pictures [OPTIONAL] (list_of_dictionaries) 
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
        user_id = f"'{credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])}'"
    except KeyError as e:
        logger.error(f"id: {g.execution_id}\n KEY ERROR: {e}")
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
    result = database_connection.execute_query('user_completed_jobs', **mapping)
    result = database_connection.group_attributes_jobs(result)
    return json.dumps({'code': 200, 'message': result},default=str)


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
pictures [OPTIONAL] (list_of_dictionaries) 
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
        user_id = f"'{credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])}'"
    except KeyError as e:
        logger.error(f"id: {g.execution_id}\n KEY ERROR: {e}")
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{user_id}': user_id
    }
    result = database_connection.execute_query('user_liked_jobs', **mapping)
    result = database_connection.group_attributes_jobs(result)
    return json.dumps({'code':200, 'message': result},default=str)


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
pictures [OPTIONAL] (list_of_dictionaries) 
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
        user_id = f"'{credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])}'"
    except KeyError as e:
        logger.error(f"id: {g.execution_id}\n KEY ERROR: {e}")
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{user_id}': user_id
    }
    result = database_connection.execute_query('user_owns_jobs', **mapping)
    result = database_connection.group_attributes_jobs(result)
    return json.dumps({'code':200, 'message': result},default=str)
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
regions (list_of_dictionaries)
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
            [f"'{credentials_factory.get_region_id(region['country'], region['region_name'])}'" for region in arguments])
    except KeyError as e:
        logger.error(f"id: {g.execution_id}\n KEY ERROR: {e}")
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    mapping = {
        '{region_id_list}': region_id_list
    }
    result = database_connection.execute_query('users_in_region',**mapping)
    result = database_connection.group_attributes_user(result)
    return json.dumps({'code': 200, 'message': result},default=str)

"""
path "/search_job" will return the searched items. Expecting following dictionary in JSON:
region (list of dictionaries)
    country (str)
    region_name (str)
type (description,owner,skills,skills_description,title)
(following key is depending on type) (everything can be substring) 
search = description 
OR
first_name (one or both)
last_name (one or both)
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
pictures [OPTIONAL] (list_of_dictionaries) 
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
            [f"'{credentials_factory.get_region_id(region['country'], region['region_name'])}'" for region in arguments['region']])
        mapping = {
            '{region_id_list}': region_id_list,
        }
        if arguments['type'] == 'owner':
            mapping.update( {
                '{search_first_name}': arguments['first_name'] if arguments.get('first_name') else str(),
                '{search_last_name}': arguments['last_name'] if arguments.get('last_name') else str()
            })
        else:
            mapping.update({
                '{search}': arguments['search']
            })
    except KeyError as e:
        logger.error(f"id: {g.execution_id}\n KEY ERROR: {e}")
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    result = database_connection.execute_query(search_query,**mapping)
    result = database_connection.group_attributes_jobs(result)
    return json.dumps({'code': 200, 'message': result},default=str)

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
regions (list_of_dictionaries)
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
        mapping = {
            '{users_in_region}': read_sql_file('users_in_region'),
            '{user_additional_information}': read_sql_file('user_additional_information', True),
            '{region_id_list}': read_sql_file('all_regions', True)
        }
        search_query = 'search_users_on_' + arguments['type']
        if arguments['type'] == 'full_name':
            mapping.update( {
                '{search_first_name}' : arguments['first_name'] if arguments.get('first_name') else str(),
                '{search_last_name}': arguments['last_name'] if arguments.get('last_name') else str()
            })
        else:
            mapping.update({
                '{search}': arguments['search']
            })
    except KeyError as e:
        logger.error(f"id: {g.execution_id}\n KEY ERROR: {e}")
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    result = database_connection.execute_query(search_query, **mapping)
    result = database_connection.group_attributes_user(result)
    return json.dumps({'code':200, 'message': result},default=str)
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
pictures [OPTIONAL] (list_of_dictionaries) 
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
        user_id = f"'{credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])}'"
    except KeyError as e:
        logger.error(f"id: {g.execution_id}\n KEY ERROR: {e}")
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
    relevant_jobs = database_connection.group_attributes_jobs(relevant_jobs)
    [job.update({
                'matching_score': database_connection.overlap([label['label_name'] for label in job['labels']], [label['label_name'] for label in skills_user])
                })
                for job in relevant_jobs]

    database_connection.sort_recommendations(relevant_jobs)
    return json.dumps({'code':200, 'message':relevant_jobs},default=str)
