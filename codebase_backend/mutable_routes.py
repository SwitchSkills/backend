import json

from flask import request, g

from codebase_backend import app, credentials_factory, database_connection, logger
from codebase_backend.decorators import catch_sever_crash
from codebase_backend.helper_functions import verify_and_insert_user, get_change_user_name_mapping, insert_picture_user, \
    insert_regions_user, insert_labels_user, verify_and_insert_job, insert_pictures_job, insert_labels_job, \
    get_change_job_title_mapping
from codebase_backend.semaphores import user_lock, completed_job_lock, liked_job_lock


"""
path "/user" will add a user to the database OR update existing user using (first_name, last_name) key, 
to change this key use path "change_user_name". Expecting following dictionary in JSON:
first_name (str)
last_name (str)
email_address (str)
phone_number (str: +32 476 26 73 97 format)
alternative_communications [OPTIONAL] (str: link)
bibliography [OPTIONAL] (str)
picture [OPTIONAL] (dictionary)
    picture_location_firebase (str: download url)
    description [OPTIONAL] (str)
password (str, would do dubbel hash (frontend & backend) if easy to implement in frontend)
location (str)
labels [OPTIONAL] (list of dictionaries)
    label_name (str)
regions (list of dictionaries)
    region_name (str)
    country (str)
rating [OPTIONAL]
number_of_ratings [OPTIONAL]
REQUIREMENTS:
combination first name & last name UNIQUE
email_address UNIQUE
phone_number UNIQUE
label exists
region exists
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (dictionary)
code 200
"""


@app.post('/user')
@catch_sever_crash
def user():
    arguments = request.get_json()
    if error_message := verify_and_insert_user(credentials_factory, database_connection, arguments):
        return error_message

    if arguments.get('picture'):
        insert_picture_user(credentials_factory, database_connection, arguments)

    insert_labels_user(credentials_factory, database_connection, arguments)
    insert_regions_user(credentials_factory, database_connection, arguments)

    return json.dumps({'code': 200})


"""
path "/change_user_name" will change the (first_name, last_name) key of an existing user. Expecting following dictionary in JSON:
existing_first_name
existing_last_name
new_first_name
new_last_name
REQUIREMENTS:
combination new first name & new last name UNIQUE
existing user exists in db
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (dictionary)
code 200
"""


@app.post("/change_user_name")
@catch_sever_crash
def change_user_name():
    arguments = request.get_json()

    try:
        mapping = get_change_user_name_mapping(credentials_factory, arguments)
    except KeyError as e:
        logger.error(f"id: {g.execution_id}\n KEY ERROR: {e}")
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    user_lock.acquire()
    database_connection.execute_query('update_user_name', **mapping)
    user_lock.release()
    return json.dumps({'code': 200})


"""
path "/job" will add a job to the database OR update an existing job using the key (title), to change the title 
use path "/change_job_title". Expecting following dictionary in JSON format
title (str)
description (str)
datetime_made_utc [OPTIONAL]
datetime_expires_utc [OPTIONAL]
region (dictionary)
    region_name (str)
    country (str)
location (str)
first_name_owner
last_name_owner
labels (list of dictionaries)
    label_name (str)
picture [OPTIONAL] (list of dictionary)
    picture_location_firebase (str: download url)
    description [OPTIONAL] (str)
REQUIREMENTS:
title UNIQUE
user exists
region exists
label exists
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS(dictionary)
code 200
"""


@app.post('/job')
@catch_sever_crash
def job():
    arguments = request.get_json()
    arguments.update({
        'regions': [arguments['region']]  # recycle check code from user regions
    })
    if error_message := verify_and_insert_job(credentials_factory, database_connection, arguments):
        return error_message

    if arguments.get('picture'):
        insert_pictures_job(credentials_factory, database_connection, arguments)

    insert_labels_job(credentials_factory, database_connection, arguments)
    return json.dumps({'code': 200})


"""
path "/change_job_title" will change the title key of an existing job. Expecting following dictionary in JSON:
existing_title
new_title
REQUIREMENTS:
combination new title UNIQUE
existing job exists in db
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (dictionary)
code 200
"""


@app.post('/change_job_title')
@catch_sever_crash
def change_job_title():
    arguments = request.get_json()

    try:
        mapping = get_change_job_title_mapping(credentials_factory, arguments)
    except KeyError as e:
        logger.error(f"id: {g.execution_id}\n KEY ERROR: {e}")
        return json.dumps(
            {
                'code': 400,
                'message': f"following key error: {e}"
            }
        )
    user_lock.acquire()
    database_connection.execute_query('update_job_title', **mapping)
    user_lock.release()
    return json.dumps({'code': 200})


"""
path "/user_liked_job" will mark a job in the database as liked by a user. Expecting following dictionary in JSON format
first_name (str)
last_name (str)
job_title (str)
REQUIREMENTS:
user exists
job exists
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (dictionary)
code 200
"""


@app.post('/user_liked_job')
@catch_sever_crash
def user_liked_job():
    arguments = request.get_json()
    user_id = credentials_factory.get_user_id(arguments['first_name'],arguments['last_name'])
    mapping = {
        '{user_id}': user_id,
        '{title}': arguments['title']
    }
    liked_job_lock.acquire()
    database_connection.execute_query('insert_liked_job',**mapping)
    liked_job_lock.release()
    return json.dumps({'code': 200})

"""
path "/user_liked_job" will mark a job in the database as liked by a user. Expecting following dictionary in JSON format
first_name (str)
last_name (str)
job_title (str)
REQUIREMENTS:
user exists
job exists
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (dictionary)
code 200
"""


@app.post('/user_unliked_job')
@catch_sever_crash
def user_unliked_job():
    arguments = request.get_json()
    user_id = credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])
    mapping = {
        '{user_id}': user_id,
        '{title}': arguments['title']
    }
    liked_job_lock.acquire()
    database_connection.execute_query('delete_liked_job', **mapping)
    liked_job_lock.release()
    return json.dumps({'code': 200})


"""
path "/user_accepted_job" will mark a job in the database as accepted, but not completed yet, by a user. Expecting following dictionary in JSON format
first_name_user (str)
last_name_user (str)
job_title (str)
datetime_request_utc [OPTIONAL] (datetime)
REQUIREMENTS:
user exists
job exists
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (dictionary)
code 200
"""


@app.post('/user_accepted_job')
@catch_sever_crash
def user_accepted_job():
    arguments = request.get_json()
    user_id = credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])
    mapping = {
        '{user_id}': user_id,
        '{title}': arguments['title'],
        '{pending}': 'TRUE'
    }
    if arguments.get('datetime_request_utc'):
        mapping.update({
            '{datetime_request_utc_key}': 'datetime_request_utc',
            '{datetime_request_utc_content}': arguments['datetime_request_utc']
        })
    else:
        mapping.update({
            '{datetime_request_utc_key}': str(),
            '{datetime_request_utc_content}': str()
        })
    completed_job_lock.acquire()
    database_connection.execute_query('insert_accepted_job', **mapping)
    completed_job_lock.release()
    return json.dumps({'code': 200})


"""
path "/user_completed_job" will mark a job in the database as completed by a user. Expecting following dictionary in JSON format
first_name_user (str)
last_name_user (str)
job_title (str)
datetime_confirmation_utc [OPTIONAL] (datetime)
REQUIREMENTS:
user exists
job exists
previous accepted call has been made for this job and user combination
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS OR NO CHANGE(dictionary)
code 200
"""


@app.post('/user_completed_job')
@catch_sever_crash
def user_completed_job():
    arguments = request.get_json()
    user_id = credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])
    mapping = {
        '{user_id}': user_id,
        '{title}': arguments['title'],
    }
    if arguments.get('datetime_confirmation_utc'):
        mapping.update({
            '{datetime_confirmation_utc_key}': ', datetime_confirmation_utc = ',
            '{datetime_confirmation_utc_content}': arguments['datetime_confirmation_utc']
        })
    else:
        mapping.update({
            '{datetime_confirmation_utc_key}': str(),
            '{datetime_confirmation_utc_content}': str()
        })
    completed_job_lock.acquire()
    database_connection.execute_query('insert_completed_job', **mapping)
    completed_job_lock.release()
    return json.dumps({'code': 200})


"""
path "/user_completed_job" will mark a job in the database as completed by a user. Expecting following dictionary in JSON format
first_name_user (str)
last_name_user (str)
job_title (str)
REQUIREMENTS:
user exists
job exists
previous accepted call has been made for this job and user combination
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (dictionary)
code 200
"""


@app.post('/user_not_complete_job')
@catch_sever_crash
def user_not_completed_job():
    arguments = request.get_json()
    user_id = credentials_factory.get_user_id(arguments['first_name'], arguments['last_name'])
    mapping = {
        '{user_id}': user_id,
        '{title}': arguments['title'],
    }
    completed_job_lock.acquire()
    database_connection.execute_query('delete_accepted_job', **mapping)
    completed_job_lock.release()
    return json.dumps({'code': 200})


"""
path "/user_receive_rating" will update the rating of a existing user. Expecting following dictionary in JSON format
first_name
last_name
rating
REQUIREMENT:
user exists
rating is between 200 and 5
ON BREAK: (dictionary)
code 400 (client error)
message (str)
ON NOT SUCCESSFUL (dictionary)
code 500 (server error)
ON SUCCESS (dictionary)
code 200
ASSUMPTION: rating comes from user that completed a job 
"""


@app.post('/user_received_rating')
@catch_sever_crash
def user_received_rating():
    arguments = request.get_json()
    user_id = credentials_factory.get_user_id(arguments['first_name'],arguments['last_name'])
    mapping = {
        '{user_id}': user_id
    }
    rating_information = database_connection.execute_query('get_rating_information_user',**mapping)
    mapping.update({
        '{rating}': (int(rating_information['number_of_ratings'])*float(rating_information['rating'])+int(arguments['rating']))/(int(rating_information['number_of_ratings'])+1),
        '{number_of_ratings}': int(rating_information['number_of_ratings'])+1
    })
    user_lock.acquire()
    database_connection.execute_query('update_rating_user',**mapping)
    user_lock.release()
