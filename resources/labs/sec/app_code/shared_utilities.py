# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Security lab - Shared utilities code

import logging as _log
import yaml
from psycopg import connect as db_connect


# -------------------------------------------------------------------------------------------------
class _AppUsers:
    '''Class soley used for providing the "check_login" function to validate user credentials'''

    def check_login(self, username, password):
        _log.info(f'Checking login credentials for app user "{username}"')
        _log.debug(f'Password associated with app user "{username}" in login attempt: {password}')

        if not username in self.app_users_dictionary.keys():
            _log.warning(f'Non-existing user "{username}" tried to authenticate')
            return

        if not password == self.app_users_dictionary[username]:
            _log.warning(f'User "{username}" tried to authenticate with an invalid password')
            return

        _log.info(f'Successfully authenticated user "{username}"')

        return username
            
    
    def __init__(self, app_users_dictionary):
        self.app_users_dictionary = app_users_dictionary
        return

    
# -------------------------------------------------------------------------------------------------
def _configure_logging(log_level):
    '''Configures a basic logger instance with the configured severity level'''

    match log_level:
        case 'INFO':
            logger_level = _log.INFO

        case 'DEBUG':
            logger_level = _log.DEBUG

        case _:
            raise Exception(f'"{log_level}" is not a valid log level ("INFO" or "DEBUG")')

    _log.basicConfig(format='%(levelname)s: %(message)s', level=logger_level)
    _log.debug('If you see this, debug logging is enabled!')

    return


# -------------------------------------------------------------------------------------------------
def _database_connection(remote_host, database_name, user, password):
    '''Sets up database connection and returns handler'''

    connection_uri = f'postgresql://{user}:{password}@{remote_host}/{database_name}'
    _log.info(f'Trying to connect database "{database_name}" on "{remote_host}" as user "{user}"')
    _log.debug('Connection URI: ' + connection_uri)
    
    try:
        database_handle = db_connect(connection_uri)
        database_handle.autocommit = True
        _log.debug('Connected to database: ' + database_handle.info.dsn)

    except Exception as error_message:
        raise Exception(f'Failed to connect to database: "{error_message}"')

    return database_handle


# -------------------------------------------------------------------------------------------------
def load_configuration(file_path='/etc/app_configuration.yml'):
    '''Loads configuration from YAML file and returns logger, users, login checker and DB handle'''

    try:
        with open(file_path, 'r') as file_handle:
            raw_configuration = yaml.safe_load(file_handle)

    except Exception as error_message:
        raise Exception(f'Failed to load app configuration from "{file_path}": {error_message}')

    if not isinstance(raw_configuration, dict):
        raise Exception(f'The configuration file "{file_path}" is not parsable as a dictionary')

    for required_key in ['log_level', 'app_users', 'database_settings']:
        if not required_key in raw_configuration.keys():
            raise Exception(f'Missing option/key "{required_key}": ' + repr(raw_configuration))

    if not isinstance(raw_configuration['app_users'], dict):
        raise Exception('Option "app_users" must be a dictionary (key=username, value=password)')

    app_users = raw_configuration['app_users']
    check_login = _AppUsers(app_users).check_login

    if not isinstance(raw_configuration['database_settings'], dict):
        raise Exception('Option "database_settings" must be parseable as a dictionary')

    for required_key in ['remote_host', 'database_name', 'user', 'password']:
        if not required_key in raw_configuration['database_settings'].keys():
            raise Exception(f'Missing DB option/key "{required_key}": ' + repr(raw_configuration))

    database_settings = raw_configuration['database_settings']
    
    _configure_logging(raw_configuration['log_level'])
    database_handle = _database_connection(
        database_settings['remote_host'], database_settings['database_name'],
        database_settings['user'], database_settings['password'])

    _log.debug('Loaded app configuration: ' % repr(raw_configuration))

    return _log, users, check_login, database_handle
