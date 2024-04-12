# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Security lab - Source code for "payroll" web application

'''payroll - Web application to list/change agent salaries'''

try:
    from shared_utilities import load_configuration
    from flask import Flask, redirect, render_template
    from flask_httpauth import HTTPBasicAuth

except Exception as error_message:
    raise Exception(f'Failed to import required Python dependencies: {error_message}')

app_name = 'payroll'
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
@app.route('/update_salary/<int:agent_id>/<int:new_salary>')
@authentication.login_required
def update_salary(agent_id, new_salary):
    _log.info(
        f'"{authentication.current_user()}" updates salary to {new_salary} for agent {agent_id}')
    
    try:
        # NOTE: MAKE SURE THAT USERS ARE NOT ALLOWED TO UPDATE THEIR OWN SALARY!
        database_handle.execute(
            "UPDATE agents SET salary = %i WHERE id = %i AND NOT name ILIKE '%s %%'"
            % (new_salary, agent_id, authentication.current_user()))

    except Exception as error_message:
        raise Exception(
            f'Failed to update salary for agent {agent_id}: {error_message}')

    return redirect(f'/salary/{agent_id}', code=302)


# -------------------------------------------------------------------------------------------------
@app.route('/salary/<int:agent_id>')
@authentication.login_required
def return_salary_page(agent_id):
    _log.info(f'User "{authentication.current_user()}" requested salary page for agent {agent_id}')

    try:
        with database_handle.cursor() as cursor:
            cursor.execute(
                'SELECT name, salary FROM agents WHERE id = %s', (agent_id,))
            
            query_result = cursor.fetchone()
            if not query_result:
                raise Exception(f'Salary query for agent {agent_id} did not return any matches')

            name, salary = query_result
        
    except Exception as error_message:
        raise Exception(
            f'Failed to query salary for agent {agent_id} from database: "{error_message}"')

    return render_template(
        'salary.html.jinja', app_name=app_name, app_icon='1F9CE',
        agent_id=agent_id, name=name, salary=salary)


# -------------------------------------------------------------------------------------------------
@app.route('/')
@authentication.login_required
def return_agent_list():
    _log.info(f'User "{authentication.current_user()}" requested list of agents for salary review')

    agents = []

    try:
        with database_handle.cursor() as cursor:
            cursor.execute('SELECT id, name, salary FROM agents ORDER BY salary DESC')
            query_results = cursor.fetchall()

        if not query_results:
            raise Exception('Agents information query did not return any matches')

        for query_result in query_results:
            agents.append({
                'agent_id': query_result[0], 'name': query_result[1], 'salary': query_result[2]})

    except Exception as error_message:
        raise Exception(
            f'Failed to query agents information from database: "{error_message}"')
        
    return render_template(
        'index.html.jinja', app_name=app_name, app_icon='1F46A', agents=agents)
