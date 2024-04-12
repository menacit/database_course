# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Security lab - Source code for "gadgets" web application

'''gadgets - Web application to list/add spy gadgets to inventory'''

try:
    from shared_utilities import load_configuration
    from flask import Flask, redirect, render_template
    from flask_httpauth import HTTPBasicAuth

except Exception as error_message:
    raise Exception(f'Failed to import required Python dependencies: {error_message}')

app_name = 'gadgets'
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
@app.route('/add_gadget/<string:name>/<int:price>')
@authentication.login_required
def add_gadget(name, price):
    _log.info(
        f'"{authentication.current_user()}" added gadget "{name}" ({price} USD)')
    
    try:
        database_handle.execute('INSERT INTO gadgets (name, price) VALUES (%s, %s)', (name, price))

    except Exception as error_message:
        raise Exception(
            f'Failed to add new gadget "{name}" with price {price} USD: {error_message}')

    return redirect('/', code=302)


# -------------------------------------------------------------------------------------------------
@app.route('/')
@authentication.login_required
def return_gadget_list():
    _log.info(f'User "{authentication.current_user()}" requested list of spy gadgets')

    gadgets = []

    try:
        with database_handle.cursor() as cursor:
            cursor.execute('SELECT name, price FROM gadgets ORDER BY name ASC')
            query_results = cursor.fetchall()

        if not query_results:
            raise Exception('Gadget list query did not return any matches')

        for query_result in query_results:
            gadgets.append({'name': query_result[0], 'price': query_result[1]})

    except Exception as error_message:
        raise Exception(
            f'Failed to query gadgets information from database: "{error_message}"')
        
    return render_template(
        'index.html.jinja', app_name=app_name, app_icon='1F50F', gadgets=gadgets)
