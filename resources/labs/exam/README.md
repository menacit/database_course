<!--
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0
X-Context: Database course - Examination lab - Assignment description
-->

# Database course - Examination lab

## Scenario description
After months of unusually high tension at the office, something had to be done. The fancy
management consultants claimed that "everyone needs to be heard! \<3", which meant that development
of an internal discussion forum promptly began. Apparently management forgot to put
"knowledge of databases" in the developer job posting, resulting in a half-baked app. Meanwhile,
frustration is brewing at an unprecedented intensity.  

As with seemingly all computer-related tasks at the agency, this one falls into your lap.
Let's finish up the forum app and release those inner demons!


## Learning objectives
Practical knowledge of designing, using, hardening and operating PostgreSQL databases.


## Lab overview
The lab consist of a simple Python web application providing an internal discussion forum and
two PostgreSQL database servers. These services are packaged as Docker containers and
pre-configured to be run using Docker Compose. In order to start the containers, navigate to the
examination lab directory ("resources/labs/examination") on the student's lab system
(typically Vagrant VM) and execute the Docker Compose command:

```
$ cd /course_data/labs/exam
$ docker compose up --build --detach
```

All tools required to complete the assignment should be pre-installed on the student's lab system. 


## Screenshots

### Thread list view
![Screenshot of thread list view in forum app](screenshots/readme_forum_app_thread_list.png)


### Thread view
![Screenshot of thread view in forum app](screenshots/readme_forum_app_thread.png)


## Lab applications/containers
The sections below describe the purpose of each lab container managed by Docker Compose.


### "database-1.int.agency.test"
Container running PostgreSQL server, utilized by the "forum" web application. Configured to
automatically setup a database and a user account for the administrator user (see "environment"
section of container in "docker-compose.yml").


### "database-2.int.agency.test"
Container used for running PostgreSQL server as a read replica for "database-1". Configured to
automatically setup a user account for the administrator user (see "environment" section of
container in "docker-compose.yml").


### "jumpbox.int.agency.test"
Basic container that provides the "psql", curl/HTTPie and similar CLI utilities for
managing the databases and testing the forum application. Also provides the script/command
"forum\_test\_script.py" for automated testing/validation of application functionality. For more
information, see "Accessing databases and application" heading of the guidance section below.


### "forum.int.agency.test"
Container running the "forum" web application ("forum\_app/server.py") used to submit and respond
to discussion threads. The web application is exposed to the lab system using port forwarding and
should be accessible using the URL "http://127.0.0.1:10008". Credentials for access is available in
the file "forum\_app/configuration.yml".


## Tasks
Read the task lists below carefully before beginning the lab exercise. All database queries
implemented in the forum application must be protected against SQL injection attacks.


### Mandatory ("G")
- Start up lab environment using Docker Compose and validate access to web application/database
- Design and define table structure for forum application in the database "forum\_data"
- Create user "db\_app\_user" with privileges required to access/utilize the database "forum\_data"
- Design/Implement database queries in app to provide functionality for "GET /api/threads"
- Design/Implement database queries in app to provide functionality for "POST /api/threads"
- Design/Implement database queries in app to provide functionality for "GET /api/threads/\$ID"
- Design/Implement database queries in app to provide functionality for "PUT /api/threads/\$ID"
- Design/Implement database queries in app to provide functionality for "DELETE /api/threads/\$ID"


### Meritorious ("VG")
- Design/Implement database queries in app to provide functionality for "/api/top\_posters"
- Ensure that "foreign key constraints" are enforced for relevant table columns
- Extract/Store end-user's source IP address used during thread manipulation in database (C~~R~~UD)
- Enable logging of all database queries to "stderr" in PostgreSQL
- Restrict database permissions for "db\_app\_user" using principle of least privilege
- Perform backup and restore of "forum\_data" table in PostgreSQL ("database-1")
  - Setup a dedicated database user for data backup using principle of least privilege
  - Utilize the "pg\_dump" utility in the "jumpbox" container to perform backup
  - Modify/Delete some of the stored rows
  - Restore backup and validate result
  
- Configure "database-2" as a read replica of "database-1" for high-availability
  - Validate result by disabling "database-1" and executing SELECT queries against the replica


## Lab report/documentation
Each student should submit a lab report containing **at least** the following information:
- Documentation of how each task was performed, including reasoning behind solution
- Documentation of verification steps taken to validate effect of each task
- Documentation of output from the automated application test script ("forum\_test\_script.py")
  
The lab report should be provided as a plain text file (".txt"), Markdown document or PDF file.
In addition to the report, all lab files that have been changed (scripts, configuration sets,
screenshots, etc.) should be provided as a ZIP or GZIP archive.  
  
Upload lab report and archive of changed files to
%REPORT_TARGET%.


## Guidance and resources

### Problems accessing lab web applications
The web application container utilize port forwarding rules to expose its web server and make it
accessible on the system where the Docker containers are running. If the lab environment is
running in a Vagrant VM, an additional layer of port forwarding is setup to enable direct access to
the web applications from the student's host computer.  

If the student has issues related to accessing the lab application using the web browser in their
host operating system, ensure that the latest version of the lab system Vagrantfile
("resources/labs/Vagrantfile") is utilized as earlier versions didn't setup the previously
described port forwarding automatically.


### Relevant lab files
The lab environment consists of several files to build, setup and run the containers for the web
application and databases. Many of these doesn't however need to be modified/reviewed by the
student to complete the lab. The list below contain file paths (relative to the lab directory) and
a short purpose description of files that the student is required to understand and/or modify:

- "docker-compose.yml": Describes how all containers should be run. Contains credentials
- "database/\*/postgresql.conf": PostgreSQL server configuration for database containers
- "database/\*/pg\_hba.conf": PostgreSQL authentication configuration for database containers
- "database-2\_shell.sh": Basic script for starting a command-line shell in database container
- "jumpbox\_shell.sh": Basic script for starting a command-line shell in jumpbox container
- "jumpbox/forum\_test\_script.py": Automated script to test functionality provided by forum app
- "jumpbox/share": Directory shared with jumpbox container, available at container path "/share"
- "forum\_app/configuration.yml": Configuration for "forum" web application. Contains credentials
- "forum\_app/server.py": Source code for forum app. Describes change requirements for endpoints


### Avoid screenshots of text
During a debugging session or lab guidance with the course teacher, avoid taking screenshots of
text error messages/output whenever possible. Instead, utilize the copy-paste feature to extract
and send the relevant output/error messages. This practice enables easy high-lighting of relevant
error messages and code snippets.


### Verifying setup of lab system
Before starting with the lab tasks, the student should ensure their computer ("the lab system") has
been setup and configured properly. The file "resources/labs/README.md" included in the course
resource archive describes the configuration prerequisites and steps to validate them.


### Viewing container/application logs
The application and database containers produce log messages which may be useful to review. To
follow/show the log stream of all lab containers, execute the following command:

```
$ docker compose logs --follow
```

In order to inspect logs for a specific container, append the container/service name:

```
$ docker copose logs --follow database-1.int.agency.test
```


### Vagrant and working directory
When running commands such as "vagrant up" or "vagrant ssh", it's important that the working
directory ("$PWD") is the same as the "Vagrantfile" is stored in. If the commands are not executed
in this directory, Vagrant won't know which specific box/environment the command refers to.


### File paths in Docker containers
When referring to file paths in Docker files or runtime configuration for containers, keep in mind
that these are not the same as on the host system/Ubuntu VM. In order to access files from the
system running Docker, use "bind volumes" during run-time (see "volumes" section in
"docker-compose.yml" for examples).


### Avoid usage of "docker-compose" command
Old documentation about how to utilize Docker Compose often refer to the command "docker-compose".
This is a legacy method of using the utility associated with several problems and should be avoided
in favor of the command "docker compose" (without dash separating the words). 


### Docker Compose and working directory
When running commands such as "docker compose up --build" or "docker compose rm", it's important
that the working directory ("$PWD") is the same as the "docker-compose.yml" is stored in.
If the commands are not executed in this directory, Docker won't know which specific Compose
environment the command refers to.


### Executing Compose without "--build" argument
The file "docker-compose.yml" specifies that Docker Compose should build container images to host
the example web application. If the Python source code of this applications is changed, it may
however not be automatically rebuilt. As this can cause problems and make testing changes
difficult, make sure to always include the "--build" flag when starting up the Compose environment:

```
$ docker compose up --build --detach
```


### Resetting Compose environment
If the student wishes to purge current state of the containers/database storage volume (in other
words, "reset it"), execute the following commands:

```
$ docker compose rm --volumes --stop
$ docker volume rm exam_database_1_data
$ docker volume rm exam_database_2_data
```


### Hostname resolution in Compose
When specifying multiple containers/services in a Docker Compose file, the different
containers/services can utilize each others names to as network host names instead of specifying
IP addresses in configuration options. This means that a service called "web" can connect to the
database container "db" using the host name "db". For more information, see "Links" section below.


### Enabling application debug logging
The lab application supports debug message logging by setting the option "log_level" to "DEBUG" in
the applications' configuration file ("forum\_app/configuration.yml"). This will increase the
verbosity of log messages, but may aid the student when investigating problems or implementing
changes.


### "Errno -3: Try again!"
If the "forum" web application fail to start due to the database error "Errno -3: Try again!",
it means that the application couldn't resolve the hostname specified in the database URI.
Ensure that the correct hostname is used (matching the application container's name in the file
"docker-compose.yml") and that the correct remote is specified in the application configuration
file in "forum\_app/configuration.yml.


### Accessing databases and application
In order to query/update/migrate the databases, the container "jumpbox.int.agency.test" is provided
with pre-installed clients and Python modules for HTTP and PostgreSQL. To enable easy
access, a simple wrapper-script exist to spawn a shell in the running container:

```
$ cd /course_data/labs/exam
$ ./jumpbox_shell.sh
```

Once inside the shell, commands can be executed interactively:

```
$ psql "postgresql://admin:Ct=Snackul4@database-1.int.agency.test/forum_data"
```

Alternatively, additional command-line arguments can be provided to the script which will be
executed directly inside the container:

```
$ ./jumpbox_shell.sh http GET "http://malory:h3art_rich@forum.int.agency.test:5000/api/threads/2"
```


### Identifying required changes in forum app
Several of the lab tasks require that the student modify the forum application source code
("forum\_app/server.py") in order to implement database queries and return relevant data.
Each API end-point in the application (for example, "GET /api/threads/\$ID") has a corresponding
Python function to handle the request.  
  
In the "docstring" for each of these functions, requirements and examples are provided:

```python
[...]

@app.get('/api/threads/<int:thread_id>')
@authentication.login_required
def get_thread(thread_id):
    '''
    Purpose: Get content from specified forum thread.
    Expected response:
        - Thread title
        - Topic description
        - Topic creation timestamp
        - List of responses with comment, author and response timestamp
    
    Sorting: List of responses sorted by response timestamp (oldest first)
    Constraints: None
    Request body structure: None
    '''

    example_response = {
        'title': 'Office manners',
        'topic_description': 'Let us discuss how we should behave in the office. Suggestions?',
        'created': '2024-03-02 16:11:40+01',
        'author': 'malory',
        'responses': [
            {
                'comment': 'I suggest we disallow storing "experiments" in the kitchen fridge!',
                'author': 'cheryl',
                'responded': '2024-03-03 03:28:10+01'
            },
            {
                'comment': 'Agreed. In the same vein: glue is not food! :-@',
                'author': 'malory',
                'responded': '2024-03-03 10:23:52+01'
            }
        ]
    }

[...]
```

These requirements and example responses should be reviewed carefully before changes are made.


### Implementing database queries in forum app
Several of the lab tasks require that the student modify the forum application source code
("forum\_app/server.py") in order to implement database queries and return relevant data.
Each API end-point in the application (for example, "GET /api/threads) has a corresponding
Python function to handle the request.  
  
In order to aid initial testing and implementation of database queries, many of the functions has
a variable called "example\_response" pre-defined:

```python
@app.get('/api/threads')
@authentication.login_required
def list_threads():
    '''
    Purpose: Return list of threads.
    Expected response: List of threads with ID, title, author and last update timestamp.
    Sorting: Latest updated threads first.
    Constraints: None
    Request body structure: None
    '''

    example_response = [
        {
            'id': 2,
            'title': 'Office manners',
            'author': 'malory',
            'updated': '2024-03-03 10:23:52+01'
        },
        {
            'id': 1,
            'title': 'Fight club anyone?!',
            'author': 'pam',
            'updated': '2024-03-01 14:39:42+01'
        }
    ]
    
    # ---------------------------------------------------------------------------------------------
    app_user = authentication.current_user()
    _log.info(f'Fetching list of threads for user "{app_user}"')
    
    response = []
    try:
        with postgresql_client.cursor() as cursor:
            # TODO: Write your SQL quer(y|ies) here!
            postgresql_client.commit()
    
    except Exception as error_message:
        raise Exception(
            f'Failed fetching thread list for user "{app_user}" from database: "{error_message}"')

    # TODO: Remove variable assignment below
    response = example_response
    _log.debug('Generated response data for thread listing: ' + repr(response))

    return jsonify(response)

[...]
```

The student should make sure to remove the `response = example\_response` variable assignment after
implementing their database queries in the `with postgresql\_client.cursor() as cursor` code block.

Once changes has been implemented, issue the command below to rebuild and restart affected
Docker containers:

```
$ docker compose up --build --detach
```


### Testing changes to forum app
In order to aid implementation of changes in the forum app, an automated test script exist that
performs actions in the application as multiple users and verifies server results. To run the
script, execute the following command and observe the output:

```
$ ./jumpbox_shell.sh forum_test_script.py"
```

To increase the log verbosity of the test script, set "log\_level" setting to "DEBUG" in the
configuration file "jumpbox/forum\_test\_script\_configuration.yml".


### Stopping specific containers/services
In order to selectively stop a specific container in the Compose environment, issue a command
similar to the one demonstrated below:

```
$ docker compose stop database-1.int.agency.test
```


### Restarting/Reloading PostgreSQL
When certain server/authentication configuration options are modified in PostgreSQL, the process
must be reloaded or restarted for the changes to take effect.  
  
Many guides instruct the administrator to restart PostgreSQL using commands like
"systemctl restart postgresql.service" or "/etc/init.d/postgresql restart". These commands are
however not applicable to the lab environment as the PostgreSQL process is directly executed in
the database containers. An equivalent option would be issuing the following command:

```
$ docker compose restart database-1.int.agency.test
```


### Accessing OS shell on database-2
In order to enable easy access to an "operating system" shell for modifying arbitrary files and
issuing commands in the container "database-2.int.agency.test", execute the command below in
the lab directory ("resources/labs/exam"):

```
$ ./database-2_shell.sh
```


### Enabling PostgreSQL on database-2
Backup/Configuration tools like "pg\_basebackup" requires deletion and modification of files
actively utilized by a running PostgreSQL server process. A common practice is to temporarily stop
the server process before executing these types of tools and enabling it afterward.
  
Due to the way PostgreSQL is executed in the lab environment, this is however not trivial and the
server process is therefore not automatically executed in the secondary database container.
In order to enable it, modify "docker-compose.yml" and comment out/remove the "entrypoint" option
for the "database-2.int.agency.test" container/service. After performing changes to the Compose
configuration file, the following command must be executed for changes to take effect:

```
$ docker compose up --build --detach
```


### Authentication configuration in PostgreSQL
"Users" in PostgreSQL typically consist of a role with a password assigned and the "LOGIN"
privilege configured. In addition to roles, a configuration file called "pg\_hba.conf" restricts
how users can authenticate to the database - it enables administrators to limit which protocols,
network source addresses, login methods and similar are permitted.  

Even if the "all" option is used to allow connections to any database on the server, access using
the replication protocol (as opposed to regular queries) must be explicitly enabled.


### Asking for assistance
In order to minimize repeated answers to recurring questions, several common issues are brought up
in the lab description (this README file). The teacher should also update the guidance section of
the lab description if such need arises during the course. Before requesting help/guidance from the
course leader, the student should utter the secret passphrase "Black ICE".


### Links
- [Vagrant port forwards](https://developer.hashicorp.com/vagrant/docs/networking/forwarded_ports)
- ["Compose" getting started guide](https://docs.docker.com/get-started/08_using_compose/)
- ["Compose" networking overview](https://docs.docker.com/compose/networking/)
- [PostgreSQL image on Docker Hub](https://hub.docker.com/_/postgres/)
- ["psql" command documentation](https://www.postgresql.org/docs/current/app-psql.html)
- [PGSQL connection URIs](https://www.prisma.io/dataguide/postgresql/short-guides/connection-uris)
- [HTTPie usage guide](https://httpie.io/docs/cli/usage)
- [PGSQL connection URIs](https://www.prisma.io/dataguide/postgresql/short-guides/connection-uris)
- [PostgreSQL documentation - "CREATE TABLE"](https://www.postgresql.org/docs/current/sql-createtable.html)
- [PostgreSQL Basics: Roles and privileges](https://www.red-gate.com/simple-talk/databases/postgresql/postgresql-basics-roles-and-privileges/)
- [PostgreSQL Tutorials - Create table](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-create-table/)
- [PostgreSQL Tutorials - Timestamps](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-timestamp/)
- [PostgreSQL Tutorials - Foreign key](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-foreign-key/)
- [PostgreSQL Tutorials - Create role](https://www.postgresqltutorial.com/postgresql-administration/postgresql-roles/)
- [PostgreSQL Tutorials - Grant privileges](https://www.postgresqltutorial.com/postgresql-administration/postgresql-grant/)
- [BetterStack - Postgres logging](https://betterstack.com/community/guides/logging/how-to-start-logging-with-postgresql/)
- [OWASP - SQL injection overview](https://owasp.org/www-community/attacks/SQL_Injection)
- [psycopg - Cursor classes](https://www.psycopg.org/psycopg3/docs/api/cursors.html)
- [psycopg - Passing query parameters](https://www.psycopg.org/psycopg3/docs/basic/params.html)
- [Python Flask - "request.remote\_addr"](https://flask.palletsprojects.com/en/3.0.x/api/#flask.Request.remote_addr)
- [PostgreSQL documentation - "pg\_dump"](https://www.postgresql.org/docs/current/app-pgdump.html)
- [PostgreSQL documentation - High-availability](https://www.postgresql.org/docs/current/high-availability.html)
- [PostgreSQL documentation - "Warm standby"](https://www.postgresql.org/docs/current/warm-standby.html)
- [PostgreSQL documentation - "pg\_basebackup"](https://www.postgresql.org/docs/current/app-pgbasebackup.html)
- [DO Tutorials - Streaming replication with PostgreSQL](https://www.digitalocean.com/community/tutorials/how-to-set-up-physical-streaming-replication-with-postgresql-12-on-ubuntu-20-04)
