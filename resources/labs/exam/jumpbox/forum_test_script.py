#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Examination lab - Source code for "forum" test script

'''
forum_test_script - Automated testing script for "forum" web application.
'''

try:
    import logging as _log
    import sys
    
    import requests
    import yaml
    
except Exception as error_message:
    raise Exception(f'Failed to import required Python dependencies: {error_message}')


# -------------------------------------------------------------------------------------------------
def request(description, app_user, method, url_path, body):
    target_url = target_base_url + url_path
    _log.info(
        f'Sending HTTP request to {description} as {app_user} - {method} {target_url} with body:\n'
        + repr(body))

    try:
        raw_response = requests.request(
            method, target_url, json=body, auth=(app_user, app_users[app_user]))

        raw_response.raise_for_status()
        response = raw_response.json()
        _log.debug('Response data from server:\n' + repr(response))

    except Exception as error_message:
        raise Exception(f'Failed to perform HTTP request: "{error_message}"')

    return response


# -------------------------------------------------------------------------------------------------
# Load configuration from YAML file and validate that required keys/options are present
configuration_path = '/etc/forum_test_script_configuration.yml'

try:
    with open(configuration_path, 'r') as file_handle:
        raw_configuration = yaml.safe_load(file_handle)
        
except Exception as error_message:
    raise Exception(f'Failed to load configuration from "{configuration_path}": {error_message}')

if not isinstance(raw_configuration, dict):
    raise Exception(f'The file "{configuration_path}" is not parsable as a dictionary')

for required_key in ['log_level', 'target_base_url', 'app_users']:
    if not required_key in raw_configuration.keys():
        raise Exception(f'Missing option/key "{required_key}": ' + repr(raw_configuration))  
    
if not isinstance(raw_configuration['app_users'], dict):
    raise Exception('Option "app_users" must be a dictionary (key=username, value=password)')

match raw_configuration['log_level']:
    case 'INFO':
        logger_level = _log.INFO

    case 'DEBUG':
        logger_level = _log.DEBUG
        
    case _:
        raise Exception('Option "log_level" is invalid (must be "INFO" or "DEBUG")')

_log.basicConfig(format='%(levelname)s: %(message)s', level=logger_level)
_log.debug('Loaded app configuration: ' + repr(raw_configuration))

target_base_url = raw_configuration['target_base_url']
app_users = raw_configuration['app_users']

# -------------------------------------------------------------------------------------------------
_log.info(f'Starting test execution against "{target_base_url}"')

try:
    # ---------------------------------------------------------------------------------------------
    threads = request(
        'fetching thread list', 'pam',
        'GET', '/api/threads',
        None)

    if not isinstance(threads, list):
        raise Exception('Server returned thread list that could not be parsed as list')

    for thread in threads:
        if not isinstance(thread, dict):
            raise Exception('Thread list item must be a dictionary')

        for required_key in ['id', 'title', 'author', 'updated']:
            if not required_key in thread.keys():
                raise Exception(f'Required thread item key "{required_key}" is missing')

            if not thread[required_key]:
                raise Exception(f'Required thread item key "{required_key}" contains empty value')

        if not isinstance(thread['id'], int):
            raise Exception('Required thread item key "id" must be an integer')

        for string_key in ['title', 'author', 'updated']:
            if not isinstance(thread[string_key], str):
                raise Exception(f'Required thread item key "{string_key}" must be a string')

        for example_thread in ['Fight club anyone?!', 'Office manners', 'My sincerest apology']:
            if example_thread == thread['title']:
                request(
                    f'cleanup previous example thread "{example_thread}"', thread['author'],
                    'DELETE', f'/api/threads/{thread["id"]}',
                    None)
    
    # ---------------------------------------------------------------------------------------------
    fight_club_thread_id = request(
        'create fightclub thread', 'pam',
        'POST', '/api/threads',
        {
            'title': 'Fight club anyone?!',
            'topic_description': 'I love bare-knuckle boxing. Who is with me?!'
        })

    if not isinstance(fight_club_thread_id, int):
        raise Exception('Server did not return thread ID after creation')

    if fight_club_thread_id == 424242:
        _log.warning('Server returned example thread ID - have you really changed the code?')

    # ---------------------------------------------------------------------------------------------
    manners_thread_id = request(
        'create office manners thread', 'malory',
        'POST', '/api/threads',
        {
            'title': 'Office manners',
            'topic_description': 'Let us discuss how we should behave in the office. Suggestions?'
        })

    request(
        'answer manners thread', 'cheryl',
        'PUT', f'/api/threads/{manners_thread_id}',
        'I suggest we disallow storing "experiments" in the kitchen fridge!')
    
    request(
        'answer manners thread', 'malory',
        'PUT', f'/api/threads/{manners_thread_id}',
        'Agreed. In the same vein: glue is not food! :-@')

    manners_thread = request(
        'fetching manners thread', 'pam',
        'GET', f'/api/threads/{manners_thread_id}',
        None)

    if not isinstance(manners_thread, dict):
        raise Exception('Server did not return dictionary as a response')

    for required_key in ['title', 'topic_description', 'created', 'author', 'responses']:
        if not required_key in manners_thread.keys():
            raise Exception(f'Server response did not include required key "{required_key}"')

        if not manners_thread[required_key]:
            raise Exception(f'Required key "{required_key}" in response contains an empty value')

    for required_key in ['title', 'topic_description', 'created', 'author']:
        if not isinstance(manners_thread[required_key], str):
            raise Exception(f'Required key "{required_key}" must be a string')

    if not isinstance(manners_thread['responses'], list):
        raise Exception(f'Required key "responses" must be a list')

    if manners_thread['title'] != 'Office manners':
        raise Exception('Thread title did not contain expected value')
        
    if manners_thread['author'] != 'malory':
        raise Exception('Thread author did not contain expected value')
        
    if not 'Let us discuss how we' in manners_thread['topic_description']:
        raise Exception('Thread topic description did not contain expected value')

    if len(manners_thread['responses']) != 2:
        raise Exception('Thread response count did not match expected value')

    manners_thread_response = manners_thread['responses'][0]
    if not isinstance(manners_thread_response, dict):
        raise Exception('Thread response item must be a dictionary')

    for required_key in ['comment', 'author', 'responded']:
        if not required_key in manners_thread_response.keys():
            raise Exception(f'Thread response item did not contain required key "{required_key}"')

    if manners_thread_response['author'] != 'cheryl':
        raise Exception('Thread response item key "author" did not contain expected value')

    if not 'I suggest we disallow' in manners_thread_response['comment']:
        raise Exception('Thread response item key "comment" did not contain expected value')

    # ---------------------------------------------------------------------------------------------
    apology_thread_id = request(
        'create apology thread', 'cyril',
        'POST', '/api/threads',
        {
            'title': 'My sincerest apology',
            'topic_description': 'Just went way over the line. I promise to never strangle again!'
        })

    if not isinstance(apology_thread_id, int):
        raise Exception('Server did not return thread ID after creation')
    
    request(
        'answer apology thread', 'pam',
        'PUT', f'/api/threads/{apology_thread_id}',
        'HahHAHAHAHahahahahaaa OMG ROFLMAO!!!11one')
    
    # ---------------------------------------------------------------------------------------------
    threads = request(
        'fetching thread list', 'pam',
        'GET', '/api/threads',
        None)

    thread_ids = []
    for thread in threads:
        thread_ids.append(thread['id'])

    for example_thread_id in [fight_club_thread_id, manners_thread_id]:
        if not example_thread_id in thread_ids:
            raise Exception(
                f'Expected thread with ID {example_thread_id} is missing in thread list')

    request(
        'delete apology thread', 'cyril',
        'DELETE', f'/api/threads/{apology_thread_id}',
        None)
    
    threads = request(
        'fetching thread list', 'cyril',
        'GET', '/api/threads',
        None)

    for thread in threads:
        if thread['title'] == 'My sincere apology':
            raise Exception('Deleted example thread should not appear in thread list')

    # ---------------------------------------------------------------------------------------------
    top_posters = request(
        'fetch list of top posters', 'malory',
        'GET', '/api/top_posters',
        None)

    if not isinstance(top_posters, list):
        raise Exception('Top posters response from server should be a list')

    if len(top_posters) != 3:
        raise Exception('Number of top posters did not match expected value of 3')

    for top_poster in top_posters:
        if not isinstance(top_poster, str):
            raise Exception('Top poster list item must be a string')

        if not top_poster:
            raise Exception('Top poster list item is an empty string')
    
    # ---------------------------------------------------------------------------------------------
    try:
        request(
            'delete non-authored thread', 'malory',
            'DELETE', f'/api/threads/{fight_club_thread_id}',
            None)
    
    except:
        pass

    else:
        raise Exception('Thread deletion by non-author should be disallowed')

    # ---------------------------------------------------------------------------------------------
    try:
        request(
            'create duplicate title thread', 'pam',
            'POST', '/api/threads',
            {
                'title': 'Fight club anyone?!',
                'topic_description': 'Got no answers in previous thread - WHO IS WITH ME?!'
            })

    except:
        pass

    else:
        raise Exception('Thread creation with duplicate title should be disallowed')
    
except Exception as error_message:
    _log.critical(f'Failed to execute test: {error_message}')
    sys.exit(1)

_log.info('Successfully executed tests! :-D')
sys.exit(0)
