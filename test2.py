import json

import requests
import urlfetch
# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.


def test_activity_feed():
    arguments = [{
        'country': 'Belgium',
        'region_name': 'Brussels Capital Region'
    }]
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/activity_feed', json=arguments)
    print('ACTIVITY_FEED:')
    print(r.json())
    print('______________________________________________')


def test_active_jobs_in_regions():
    arguments = [{
        'country': 'Belgium',
        'region_name': 'Brussels Capital Region'
    },
        {
            'country': 'Belgium',
            'region_name': 'West Flanders'
        }]
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/active_jobs_in_region', json=arguments)
    print('ACTIVE_JOBS_IN_REGION:')
    print(r.json())
    print('______________________________________________')


def test_completed_jobs_by_user():
    arguments = {
        'first_name': 'Judith',
        'last_name': 'Van Looveren'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/completed_jobs_by_user', json=arguments)
    print('COMPLETED_JOBS_BY_USER:')
    print(r.json())
    print('______________________________________________')


def test_accepted_jobs_by_user():
    arguments = {
        'first_name': 'Judith',
        'last_name': 'Van Looveren'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/accepted_jobs_by_user', json=arguments)
    print('ACCEPTED_JOBS_BY_USER:')
    print(r.json())
    print('______________________________________________')


def test_liked_jobs_by_user():
    arguments = {
        'first_name': 'Judith',
        'last_name': 'Van Looveren'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/liked_jobs_by_user', json=arguments)
    print('LIKED_JOBS_BY_USER:')
    print(r.json())
    print('______________________________________________')


def test_owned_jobs_by_user():
    arguments = {
        'first_name': 'Nation',
        'last_name': 'Builder'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/jobs_owned_by_user', json=arguments)
    print('OWNED_JOBS_BY_USER:')
    print(r.json())
    print('______________________________________________')


def test_all_users_in_region():
    arguments = [{
        'country': 'Belgium',
        'region_name': 'Brussels Capital Region'
    }]
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/all_users_in_region', json=arguments)
    print('ALL USERS IN REGION:')
    print(r.json())
    print('______________________________________________')


def test_search_jobs():
    diff_types = ['description', 'owner', 'skills', 'skills_description', 'title']
    diff_search = ['repair a flat tire', None, 'bicycle repair', 'non-electric bicycles', 'repair of bike']
    for type, search in zip(diff_types, diff_search):
        arguments = {
            'region': [{
                'country': 'Belgium',
                'region_name': 'Brussels Capital Region'
            }],
            'type': type
        }
        if type != 'owner':
            arguments.update({'search': search})
        else:
            arguments.update({
                'last_name': 'Build'
            })

        r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/search_jobs', json=arguments)
        print(f'SEARCH_JOBS:{type}')
        print(r.json())
        print('______________________________________________')


def test_search_users():
    diff_types = ['full_name', 'bibliography', 'email_address', 'phone_number']
    diff_search = [None, 'passionate', 'team@', '+91']
    for type, search in zip(diff_types, diff_search):
        arguments = {
            'type': type
        }
        if type != 'full_name':
            arguments.update({'search': search})
        else:
            arguments.update({
                'last_name': 'Build'
            })

        r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/search_users', json=arguments)
        print(f'SEARCH_USERS:{type}')
        print(r.json())
        print('______________________________________________')


def test_match_jobs():
    arguments = {
        'first_name': 'Judith',
        'last_name': 'Van Looveren'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/match_jobs', json=arguments)
    print('MATCHED_JOBS:')
    print(r.json())
    print('______________________________________________')


def test_insert_or_update_user():
    arguments = {
        'first_name': 'Dag',
        'last_name': 'yoy',
        'email_address': 'study_boy@gmail.com',
        'phone_number': '+32',
        'alternative_communications': 'https://www.linkedin.com/in/dag-malstaf/',
        'bibliography': 'killing other CS students with gracefulness',
        'picture': {
            'picture_location_firebase': 'test_location_yoy',
            'description': 'testing purposes'
        },
        'password': 'test_for_dummies',
        'location': 'bib :(',
        'labels': [{
            'label_name': 'bicycle repair'
        }],
        'regions': [
            {
                'region_name': 'Luxembourg',
                'country': 'Belgium'
            }
        ],
        'rating': 5,
        'number_of_ratings': 1
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/user', json=arguments)
    print('USER1:')
    print(r)
    print(r.json())
    print('______________________________________________')
    arguments = {
        'first_name': 'Dag',
        'last_name': 'Malstaf',
        'email_address': 'study_boy@gmail.com',
        'phone_number': '+32471785072',
        'alternative_communications': 'https://www.linkedin.com/in/dag-malstaf/',
        'bibliography': 'killing other CS students with gracefulness',
        'picture': {
            'picture_location_firebase': 'test_location_malstaf',
            'description': 'testing purposes'
        },
        'password': 'test_for_dummies',
        'location': 'bib :(',
        'labels': [{
            'label_name': 'bicycle repair'
        },
            {
                'label_name': 'gardening'
            }],
        'regions': [
            {
                'region_name': 'Luxembourg',
                'country': 'Belgium'
            },
            {
                'region_name': 'Namur',
                'country': 'Belgium'
            }
        ],
        'rating': 5,
        'number_of_ratings': 1
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/user', json=arguments)
    print('USER2:')
    print(r)
    print(r.json())
    print('______________________________________________')


def test_change_user_name():
    arguments = {
        'existing_first_name': 'Dag',
        'existing_last_name': 'Malstaf',
        'new_first_name': 'Frontend',
        'new_last_name': 'Beest',
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/change_user_name', json=arguments)
    print('USER CHANGE NAME:')
    print(r)
    print(r.json())
    print('______________________________________________')


def test_insert_or_update_job():
    arguments = {
        'title': 'repair of bike',
        'description': 'testing and crying at the same time => I am a multitasker!!!',
        'picture': {
            'picture_location_firebase': 'test_location_job',
            'description': 'testing purposes job'
        },
        'location': 'idk',
        'labels': [{
            'label_name': 'bicycle repair'
        }],
        'region':
            {
                'region_name': 'Brussels Capital Region',
                'country': 'Belgium'
            },
        'first_name_owner': 'Nation',
        'last_name_owner': 'Builder'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/job', json=arguments)
    print('JOB1:')
    print(r)
    print(r.json())
    print('______________________________________________')
    arguments = {
        'title': 'repair of bike',
        'description': 'testing and crying at the same time => I am a multitasker!!!',
        'picture': {
            'picture_location_firebase': 'test_location_job',
            'description': 'testing purposes job'
        },
        'location': 'idk',
        'labels': [{
            'label_name': 'bicycle repair'
        },
            {'label_name': 'gardening'}],
        'region':
            {
                'region_name': 'Brussels Capital Region',
                'country': 'Belgium'
            },
        'first_name_owner': 'Nation',
        'last_name_owner': 'Builder'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/job', json=arguments)
    print('JOB2:')
    print(r)
    print(r.json())
    print('______________________________________________')


def test_change_job_title():
    arguments = {
        'existing_title': 'repair of bike',
        'new_title': 'repair of chain of bike',
        'region':
            {
                'region_name': 'Brussels Capital Region',
                'country': 'Belgium'
            },
        'first_name_owner': 'Nation',
        'last_name_owner': 'Builder'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/change_job_title', json=arguments)
    print('USER JOB TITLE:')
    print(r)
    print(r.json())
    print('______________________________________________')


def test_change_job_region():
    arguments = {
        'current_region': {
            'region_name': 'Brussels Capital Region',
            'country': 'Belgium'
        },
        'new_region': {
            'region_name': 'West Flanders',
            'country': 'Belgium'
        },
        'first_name_owner': 'Nation',
        'last_name_owner': 'Builder',
        'title': 'repair of chain of bike'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/change_job_region', json=arguments)
    print('CHANGE JOB REGION:')
    print(r)
    print(r.json())
    print('______________________________________________')


def test_user_liked_job():
    arguments = {
        'first_name': 'Tristan',
        'last_name': 'Toye',
        'title': 'repair of chain of bike',
        'job_region': {
            'country': 'Belgium',
            'region_name': 'West Flanders'
        },
        'first_name_owner': 'Nation',
        'last_name_owner': 'Builder'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/user_liked_job', json=arguments)
    print('USER LIKED JOB:')
    print(r)
    print(r.json())
    print('______________________________________________')


def test_user_unliked_job():
    arguments = {
        'first_name': 'Tristan',
        'last_name': 'Toye',
        'title': 'repair of chain of bike',
        'job_region': {
            'country': 'Belgium',
            'region_name': 'West Flanders'
        },
        'first_name_owner': 'Nation',
        'last_name_owner': 'Builder'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/user_unliked_job', json=arguments)
    print('USER UNLIKED JOB:')
    print(r)
    print(r.json())
    print('______________________________________________')


def test_user_accepted_job():
    arguments = {
        'first_name': 'Tristan',
        'last_name': 'Toye',
        'title': 'repair of chain of bike',
        'job_region': {
            'country': 'Belgium',
            'region_name': 'West Flanders'
        },
        'first_name_owner': 'Nation',
        'last_name_owner': 'Builder'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/user_accepted_job', json=arguments)
    print('USER ACCEPTED JOB:')
    print(r)
    print(r.json())
    print('______________________________________________')


def test_user_completed_job():
    arguments = {
        'first_name': 'Tristan',
        'last_name': 'Toye',
        'title': 'repair of chain of bike',
        'job_region': {
            'country': 'Belgium',
            'region_name': 'West Flanders'
        },
        'first_name_owner': 'Nation',
        'last_name_owner': 'Builder'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/user_completed_job', json=arguments)
    print('USER COMPLETED JOB:')
    print(r)
    print(r.json())
    print('______________________________________________')


def test_user_not_completed_job():
    arguments = {
        'first_name': 'Tristan',
        'last_name': 'Toye',
        'title': 'repair of chain of bike',
        'job_region': {
            'country': 'Belgium',
            'region_name': 'West Flanders'
        },
        'first_name_owner': 'Nation',
        'last_name_owner': 'Builder'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/user_not_complete_job', json=arguments)
    print('USER NOT COMPLETED JOB:')
    print(r)
    print(r.json())
    print('______________________________________________')


def test_user_receive_rating():
    arguments = {
        'first_name': 'Judith',
        'last_name': 'Van Looveren',
        'rating': 5
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/user_received_rating', json=arguments)
    print('USER RECEIVED RATING1:')
    print(r)
    print(r.json())
    print('______________________________________________')
    arguments = {
        'first_name': 'Judith',
        'last_name': 'Van Looveren',
        'rating': 4
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/user_received_rating', json=arguments)
    print('USER RECEIVED RATING2:')
    print(r)
    print(r.json())
    print('______________________________________________')


def test_all_labels():
    r = requests.get('https://ethereal-yen-394407.ew.r.appspot.com/all_labels')
    print('ALL LABELS:')
    print(r)
    print(r.json())
    print('______________________________________________')


def test_all_regions():
    r = requests.get('https://ethereal-yen-394407.ew.r.appspot.com/all_regions')
    print(r)
    print(r.json())
    print('______________________________________________')

def test_login():

    diff_types = ['full_name', 'email_address', 'phone_number']
    diff_search = [None, 'nation.builder.team@gmail.com', '+919216753560']
    for type, search in zip(diff_types, diff_search):
        arguments = {
            'type': type,
            'password': 'NationBuilders'
        }
        if type != 'full_name':
            arguments.update({'search': search})
        else:
            arguments.update({
                'first_name': 'Nation',
                'last_name': 'Builder'
            })

        r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/login', json=arguments)
        print(f'LOGIN:{type}')
        print(r.json())
        print('______________________________________________')
    arguments = {
        'type': 'full_name',
        'password': 'NationBuilders',
        'first_name': 'Natio',
        'last_name': 'Builder'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/login', json=arguments)
    print(f'LOGIN: WRONG USER')
    print(r.json())
    print('______________________________________________')
    arguments = {
        'type': 'full_name',
        'password': 'WrongPassword',
        'first_name': 'Nation',
        'last_name': 'Builder'
    }
    r = requests.post('https://ethereal-yen-394407.ew.r.appspot.com/login', json=arguments)
    print(f'LOGIN: WRONG PASSWORD')
    print(r.json())
    print('______________________________________________')

if __name__ == '__main__':
    test_login()


