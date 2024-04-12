# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Security lab - Source code for "agents" web application

'''agents - Web application to list agents and show their employee profiles'''

try:
    from shared_utilities import load_configuration
    from flask import Flask, redirect, render_template
    from flask_httpauth import HTTPBasicAuth

except Exception as error_message:
    raise Exception(f'Failed to import required Python dependencies: {error_message}')

app_name = 'agents'
_log, _, check_login, database_handle = load_configuration()

# -------------------------------------------------------------------------------------------------
_log.debug('Setting up Flask application and authentication extension')

app = Flask(app_name, template_folder='.')
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

authentication = HTTPBasicAuth()
authentication.verify_password(check_login)


# -------------------------------------------------------------------------------------------------
@app.route('/is_the_server_up_and_running')
def return_healh_status():
    return f'Yes, the {app_name} application does indeed seem to be up and running!'


# -------------------------------------------------------------------------------------------------
# Yes - this end-point is vulnerable to CSRF, indeed - exploit it as a bonus lab task!
@app.route('/assign_gadget/<int:agent_id>/<int:gadget_id>')
@authentication.login_required
def assign_gadget(agent_id, gadget_id):
    _log.info(f'"{authentication.current_user()}" assigns gadget {gadget_id} to agent {agent_id}')
    
    try:
        database_handle.execute(
            'INSERT INTO gadget_assignments (gadget_id, agent_id) VALUES (%s, %s)',
            (gadget_id, agent_id))

    except Exception as error_message:
        raise Exception(
            f'Failed to assign gadget {gadget_id} to agent {agent_id}: {error_message}')

    return redirect(f'/profile/{agent_id}', code=302)


# -------------------------------------------------------------------------------------------------
@app.route('/profile/<int:agent_id>')
@authentication.login_required
def return_agent_profile(agent_id):
    _log.info(f'User "{authentication.current_user()}" requested profile for agent {agent_id}')

    profile = {}
    available_gadgets = []
    assigned_gadgets = []

    try:
        with database_handle.cursor() as cursor:
            _log.info(f'Querying profile information for agent {agent_id}')
            cursor.execute(
                'SELECT id, name, code_name, salary FROM agents WHERE id = %s', (agent_id,))
            
            profile_query_result = cursor.fetchone()
            if not profile_query_result:
                raise Exception(f'Profile query for agent {agent_id} did not return any matches')

            profile['agent_id'], profile['name'], profile['code_name'], profile['salary'] = (
                profile_query_result)
                
            _log.info('Querying gadgets available for agents')
            cursor.execute('SELECT id, name, price FROM gadgets ORDER by price ASC')

            available_gadget_query_results = cursor.fetchall()
            if not available_gadget_query_results:
                raise Exception('Query for available gadgets did not return any results')

            for available_gadget_query_result in available_gadget_query_results:
                available_gadgets.append({
                    'gadget_id': available_gadget_query_result[0],
                    'name': available_gadget_query_result[1],
                    'price': available_gadget_query_result[2]
                })
            
            _log.info(f'Querying gadgets assigned to agent {agent_id}')
            cursor.execute(
                'SELECT DISTINCT gadgets.name FROM gadgets '
                'INNER JOIN gadget_assignments ON gadgets.id = gadget_assignments.gadget_id '
                'WHERE gadget_assignments.agent_id = %s', (agent_id,))

            assigned_gadget_query_results = cursor.fetchall()
            for assigned_gadget_query_result in assigned_gadget_query_results:
                assigned_gadgets.append(assigned_gadget_query_result[0])
        
    except Exception as error_message:
        raise Exception(
            f'Failed to query agent profile {agent_id} from database: "{error_message}"')

    return render_template(
        'profile.html.jinja', app_name=app_name, app_icon='1F575', profile=profile,
        available_gadgets=available_gadgets, assigned_gadgets=assigned_gadgets)


# -------------------------------------------------------------------------------------------------
@app.route('/')
@authentication.login_required
def return_agent_list():
    _log.info(f'User "{authentication.current_user()}" requested list of agents')

    agents = []

    try:
        with database_handle.cursor() as cursor:
            cursor.execute('SELECT id, name, code_name, salary FROM agents ORDER BY salary ASC')
            query_results = cursor.fetchall()

        if not query_results:
            raise Exception('Agents information query did not return any matches')

        for query_result in query_results:
            agents.append({
                'agent_id': query_result[0], 'name': query_result[1],
                'code_name': query_result[2], 'salary': query_result[3]})

    except Exception as error_message:
        raise Exception(
            f'Failed to query agents information from database: "{error_message}"')
        
    return render_template(
        'index.html.jinja', app_name=app_name, app_icon='1F5DD', agents=agents)
