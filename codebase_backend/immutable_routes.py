from app import app

"""
path "/activity_feed" will return the content for the mainscreen: all open jobs and completed jobs 
ordered by time (earliest will be index 0). Expecting following dictionary in JSON:
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
helper (only for completed)
    first_name
    last_name
    email_address
    alternative_communication [OPTIONAL]
    phone_number
    user_location
"""
@app.get('/activity_feed')
def activity_feed():
    pass

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
def active_jobs_in_region():
    pass

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
def completed_jobs_by_user():
    pass

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
def accepted_jobs_by_user():
    pass
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
def liked_jobs_by_user():
    pass
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
def jobs_owned_by_user():
    pass
"""
path "/all_users_in_region" will return the content for all users in region. Expecting following dictionary in JSON:
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
def all_users_in_region():
    pass

"""
path "/search_job" will return the searched items. Expecting following dictionary in JSON:
type (description,owner,skills,skills_description,title)
(following key is depending on type) (everything can be substring)
search_description
OR
first_name 
last_name
OR
search_skill 
OR
search_description
OR
search_title
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
def search_jobs():
    pass

"""
path "/search_users" will return the search user. Expecting following dictionary in JSON:
type (name, bibliography, email_address, phone_number)
(following key is depending on type) (everything can be substring)
first_name
last_name
OR
search_bibliography
OR
search_email_address
OR
search_phone_number
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
def search_users():
    pass
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
def match_jobs():
    pass

