# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - NoSQL lab - Source code for "missions" web application

'''
missions - Web application to submit mission logs.

Expects missions report in JSON format subbmitted to the "/submit_report" end-point.
Example report data:

```
{
  "code_name":"Bum Fight At Night",
  "start_datetime":"2024-12-02T01:00", "end_datetime":"2024-12-02T03:30",
  "budget": 500, "cost": 861,
  "report":"Everything went as expected - the subjects started to brawl in the alley.",
  "location":{"lat":"40.783679409824956","lon":"-77.85092353820802"},
  "participants":[
    "Duchess",
    "Gilles de Rais"
  ],
  "used_gadgets":[
    "Fake mustache",
    "Stinky overcoat",
    "Bottle of brandy"
  ]
}
```
'''

try:
    import logging as _log
    import time
    
    from flask import Flask, redirect, render_template, request
    from flask_httpauth import HTTPBasicAuth
    from opensearchpy import OpenSearch as opensearch
    from psycopg import connect as postgresql
    import yaml
    
except Exception as error_message:
    raise Exception(f'Failed to import required Python dependencies: {error_message}')

# -------------------------------------------------------------------------------------------------
# Load configuration from YAML file and validate that required keys/options are present
configuration_path = '/etc/app_configuration.yml'

try:
    with open(configuration_path, 'r') as file_handle:
        raw_configuration = yaml.safe_load(file_handle)
        
except Exception as error_message:
    raise Exception(f'Failed to load configuration from "{configuration_path}": {error_message}')

if not isinstance(raw_configuration, dict):
    raise Exception(f'The file "{configuration_path}" is not parsable as a dictionary')

for required_key in ['log_level', 'app_users', 'postgresql_settings', 'opensearch_settings']:
    if not required_key in raw_configuration.keys():
        raise Exception(f'Missing option/key "{required_key}": ' + repr(raw_configuration))  
    
if not isinstance(raw_configuration['app_users'], dict):
    raise Exception('Option "app_users" must be a dictionary (key=username, value=password)')

for dbms_name in ['postgresql', 'opensearch']:
    if not isinstance(raw_configuration[dbms_name + '_settings'], dict):
        raise Exception(f'Option "{dbms_name}_settings" must be parseable as a dictionary')
    
    for required_key in ['remote_host', 'user', 'password']:
        if not required_key in raw_configuration[dbms_name + '_settings'].keys():
            raise Exception(
                f'Missing {dbms_name} option/key "{required_key}": ' + repr(raw_configuration))

if not 'database_name' in raw_configuration['postgresql_settings'].keys():
    raise Exception(
        'Missing postgresql option/key "database_name": ' + repr(raw_configuration))

match raw_configuration['log_level']:
    case 'INFO':
        logger_level = _log.INFO

    case 'DEBUG':
        logger_level = _log.DEBUG
        
    case _:
        raise Exception('Option "log_level" is invalid (must be "INFO" or "DEBUG")')

_log.basicConfig(format='%(levelname)s: %(message)s', level=logger_level)
_log.debug('Loaded app configuration: ' + repr(raw_configuration))

app_users = raw_configuration['app_users']
postgresql_settings = raw_configuration['postgresql_settings']
opensearch_settings = raw_configuration['opensearch_settings'] 

# -------------------------------------------------------------------------------------------------
_log.info('Initializing PostgreSQL client with specified settings')

s = postgresql_settings 
target_uri = f'postgresql://{s['user']}:{s['password']}@{s['remote_host']}/{s['database_name']}'
_log.debug(f'PostgreSQL connection URI: {target_uri}')

try:
    postgresql_client = postgresql(target_uri)
    _log.debug('Connected to database: ' + postgresql_client.info.dsn)
    
except Exception as error_message:
    raise Exception(f'Failed to connect to PostgreSQL database: "{error_message}"')

# -------------------------------------------------------------------------------------------------
_log.info('Initializing OpenSearch client with specified settings')

try:
    s = opensearch_settings
    opensearch_client = opensearch(
        hosts=[{'host': s['remote_host'], 'port': 9200}],
        http_auth=(s['user'], s['password']),
        use_ssl=True, verify_certs=False)

    opensearch_server_information = opensearch_client.info()
    _log.debug('Connected to OpenSearch server: ' + repr(opensearch_server_information))

except Exception as error_message:
    raise Exception(f'Failed to connect to OpenSearch: "{error_message}"')

# -------------------------------------------------------------------------------------------------
_log.debug('Setting up Flask application and authentication extension')

app = Flask('missions', template_folder='.')
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

authentication = HTTPBasicAuth()


# -------------------------------------------------------------------------------------------------
@authentication.verify_password
def verify_credentials(app_user, password):
    _log.info(f'Checking login credentials for app user "{app_user}"')
    _log.debug(f'Password associated with app user "{app_user}" in login attempt: {password}')

    if not app_user in app_users.keys():
        _log.warning(f'Non-existing app user "{app_user}" tried to authenticate')
        return

    if not password == app_users[app_user]:
        _log.warning(f'App user "{app_user}" tried to authenticate with invalid password')
        return

    _log.debug(f'Successfully authenticated app user "{app_user}"')
    return app_user


# -------------------------------------------------------------------------------------------------
@app.route('/is_the_server_up_and_running', methods=['GET', 'HEAD'])
def return_healh_status():
    return f'Yes, the web application does indeed seem to be up and running!'


# -------------------------------------------------------------------------------------------------
@app.route('/submit_report', methods=['POST'])
@authentication.login_required
def handle_report_submission():
    app_user = authentication.current_user()
    _log.info(f'Handling mission report submission from user "{app_user}"')

    _log.debug('Checking content type of received request')
    if request.headers.get('Content-Type').lower().lower() != 'application/json; charset=utf-8':
        _log.warning(f'User "{app_user}" tried submitting a report with an invalid content type')

        return 'Invalid content type!', 400

    _log.debug('Trying to parse request body data as JSON')
    request_data = request.json
    _log.debug('Parsed request data: ' + repr(request_data))

    _log.debug('Performing very rudimental validation of received report data structure')
    if not isinstance(request_data, dict):
        _log.warning(f'User "{app_user}" submitted report that was not parsable as a dictionary')

        return 'Invalid report format!', 400 

    # ---------------------------------------------------------------------------------------------
    # TODO: Store submitted reports in OpenSearch instead of PostgreSQL database
    _log.info('Storing received report in PostgreSQL database')
    s = request_data
    
    try:
        with postgresql_client.cursor() as cursor:
            _log.debug('Inserting data in "missions" table"')
            cursor.execute(
                'INSERT INTO missions ('
                '    submission_datetime, start_datetime, end_datetime,'
                '    code_name, budget, cost, location_latitude, location_longitude,'
                '    report_author, report'
                ') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id', (
                    time.ctime(), s['start_datetime'], s['end_datetime'], s['code_name'],
                    s['budget'], s['cost'], s['location']['lat'], s['location']['lon'],
                    app_user, s['report']))
            
            mission_id = cursor.fetchone()[0]
            _log.debug(f'Submitted mission report ID in database: #{mission_id}')

            # A more efficient alternative would be "cursor.executemany", but not as easy to read.
            for name in s['participants']:
                _log.debug(f'Inserting participant "{name}" for mission #{mission_id} in DB')
                cursor.execute(
                    'INSERT INTO participants (mission_id, name) VALUES (%s, %s)',
                    (mission_id, name))
    
            for name in s['used_gadgets']:
                _log.debug(f'Inserting used gadget "{name}" for mission #{mission_id} in DB')
                cursor.execute(
                    'INSERT INTO used_gadgets (mission_id, name) VALUES (%s, %s)',
                    (mission_id, name))

            _log.debug('Commiting database changes')
            postgresql_client.commit()
    
    except Exception as error_message:
        raise Exception(
            f'Failed to add mission report from user "{app_user}" in database: "{error_message}"')

    return 'Report received and stored!', 200


# -------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'HEAD'])
@authentication.login_required
def return_mission_log_form():
    _log.info(f'User "{authentication.current_user()}" requested mission log form')
    return render_template('index.html.jinja', app_user=authentication.current_user())
