import json

import requests

def test_activity_feed():
    arguments = [{
        'country': 'Belgium',
        'region_name': 'Brussels Capital Region'
    }]
    r = requests.get('http://127.0.0.1:5000/activity_feed', json=arguments)
    print('ACTIVITY_FEED:')
    print(r.json())
    print('______________________________________________')

def test_active_jobs_in_regions():
    arguments = [{
        'country': 'Belgium',
        'region_name': 'Brussels Capital Region'
    }]
    r = requests.get('http://127.0.0.1:5000/active_jobs_in_region', json=arguments)
    print('ACTIVE_JOBS_IN_REGION:')
    print(r.json())
    print('______________________________________________')

def test_completed_jobs_by_user():

    arguments = {
        'first_name': 'Judith',
        'last_name': 'Van Looveren'
    }
    r = requests.get('http://127.0.0.1:5000/completed_jobs_by_user', json=arguments)
    print('COMPLETED_JOBS_BY_USER:')
    print(r.json())
    print('______________________________________________')

def test_accepted_jobs_by_user():

    arguments = {
        'first_name': 'Judith',
        'last_name': 'Van Looveren'
    }
    r = requests.get('http://127.0.0.1:5000/accepted_jobs_by_user', json=arguments)
    print('ACCEPTED_JOBS_BY_USER:')
    print(r.json())
    print('______________________________________________')

def test_liked_jobs_by_user():

    arguments = {
        'first_name': 'Judith',
        'last_name': 'Van Looveren'
    }
    r = requests.get('http://127.0.0.1:5000/liked_jobs_by_user', json=arguments)
    print('LIKED_JOBS_BY_USER:')
    print(r.json())
    print('______________________________________________')

def test_owned_jobs_by_user():

    arguments = {
        'first_name': 'Nation',
        'last_name': 'Builder'
    }
    r = requests.get('http://127.0.0.1:5000/jobs_owned_by_user', json=arguments)
    print('OWNED_JOBS_BY_USER:')
    print(r.json())
    print('______________________________________________')

def test_all_users_in_region():
    arguments = [{
        'country': 'Belgium',
        'region_name': 'Brussels Capital Region'
    }]
    r = requests.get('http://127.0.0.1:5000/all_users_in_region', json=arguments)
    print('ALL USERS IN REGION:')
    print(r.json())
    print('______________________________________________')

def test_search_jobs():
    diff_types = ['description', 'owner', 'skills', 'skills_description', 'title']
    diff_search = ['repair a flat tire', None, 'bicycle repair','non-electric bicycles','repair of bike']
    for type, search in zip(diff_types, diff_search):
        arguments = {
            'region':[{
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

        r = requests.get('http://127.0.0.1:5000/search_jobs', json=arguments)
        print(f'SEARCH_JOBS:{type}')
        print(r.json())
        print('______________________________________________')

def test_search_users():
    diff_types = ['full_name', 'bibliography', 'email_address', 'phone_number']
    diff_search = [ None, 'passionate', 'team@', '+91']
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

        r = requests.get('http://127.0.0.1:5000/search_users', json=arguments)
        print(f'SEARCH_USERS:{type}')
        print(r.json())
        print('______________________________________________')

def test_match_jobs():
    arguments = {
        'first_name': 'Judith',
        'last_name': 'Van Looveren'
    }
    r = requests.get('http://127.0.0.1:5000/match_jobs', json=arguments)
    print('MATCHED_JOBS:')
    print(r.json())
    print('______________________________________________')

def test_insert_or_update_user():
    arguments = {
        'first_name': 'Dag',
        'last_name': 'Malstaf',
        'email_address': 'study_boy@gmail.com',
        'phone_number': '+32471785072',
        'alternative_communications': 'https://www.linkedin.com/in/dag-malstaf/',
        'bibliography': 'killing other CS students with gracefulness',
        'picture': {
            'picture_location_firebase': 'test_location',
            'description': 'testing purposes'
                },
        'password': 'test_for_dummies',
        'location': 'bib :(',
        'labels': [{
            'label_name': 'bicycle repair'
        }],
        'regions':[
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
    r = requests.post('http://127.0.0.1:5000/user', json=arguments)
    print('USER:')
    print(r)
    print(r.json())
    print('______________________________________________')


if __name__=='__main__':

    #test_activity_feed()
    #test_active_jobs_in_regions()
    #test_completed_jobs_by_user()
    #test_accepted_jobs_by_user()
    #test_liked_jobs_by_user()
    #test_owned_jobs_by_user()
    #test_all_users_in_region()
    #test_search_jobs()
    #test_search_users()
    #test_match_jobs()
    test_insert_or_update_user()


