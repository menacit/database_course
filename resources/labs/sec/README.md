# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Security lab - Assignment description


# Database course - Security lab

## Scenario description
Ever since the former (and only?) system administrator mysteriously disappeared, IT incidents have
been a recurring nuisance at the spy agency. Sure, a broken satellite here and a malfunctioning
brain control chip there is manageable, but the nuisance turned into a major headache the day all
employee data/agent files were stolen from the organization's top secret database.  

Mayhaps not an ideal starting point for your DevOps career, but at least you won't run out of
problems to solve any time soon. After peaking at the code/configuration for internal systems and
the database (while nearly suffering a heart attack), you've identified some potential weaknesses
that the attackers may have taken advantage of.  

Let's get those pesky ants out of your cup, pour a stiff one and harden up the IT systems.


## Learning objectives
Practical knowledge of access/privilege control, logging and injection mitigation in SQL databases.


## Lab overview
The lab consist of three Python web applications that use a shared PostgreSQL database for storing
and retrieving information about the spy agency's agents and their equipment. These services are
packaged as Docker containers and pre-configured to be run using Docker Compose. In order to
start the containers, navigate to the security lab directory ("resources/labs/sec") on the
student's lab system (typically Vagrant VM) and execute the Docker Compose command:

```
$ cd /course_data/labs/sec
$ docker compose up --build --detach
```

All tools required to complete the assignment should be pre-installed on the student's lab system. 


## Lab applications/containers
The sections below describe the purpose of each lab container managed by Docker Compose.


### "database.int.agency.test"
Container running PostgreSQL server and the database "agency\_data" used by all lab applications.
Based on the [official PostgreSQL Docker image](https://hub.docker.com/_/postgres/) with the
"PGAudit" extension pre-installed. Configured to automatically setup a database and a user account
for the administrator user (see "environment" section of container in "docker-compose.yml").


### "jumpbox.int.agency.test"
Basic container that exposes the "psql" CLI utility for managing/querying the database. For more
information, see "Accessing database as user/administrator" heading of guidance section.


### "agents.int.agency.test"
Container running the "agents" web application ("app\_code/agents/server.py") used to list employed
agents and assign spy gadgets/equipment to them. The web application is exposed to the lab system
using port forwarding and should be accessible using the URL "http://127.0.0.1:10001".


### "payroll.int.agency.test"
Container running the "payroll" web application ("app\_code/payroll/server.py") used to
review/change salary for employed agents. The web application is exposed to the lab system using
port forwarding and should be accessible using the URL "http://127.0.0.1:10002".


### "gadgets.int.agency.test"
Container running the "gadgets" web application ("app\_code/gadgets/server.py") used to list/add
spy gadgets/equipment available to agents. The web application is exposed to the lab system using
port forwarding and should be accessible using the URL "http://127.0.0.1:10003".


## Tasks
As this exercise is a practice lab, none of the tasks below are graded. The student should, to the
best of their abilities, try to complete as many of the tasks below during the course.

- Startup lab environment using Docker Compose and validate access to applications in a web browser
- Setup and configure usage of dedicated database users for each web application
- Disable and revoke privileges for the shared database user account "shared\_app\_user"
- Restrict privileges for the "agents" app database user to only access the required tables
- Restrict privileges for the "gadgets" app database user to only access the required tables
- Utilize column-level security to only expose required columns to the "payroll" app database user
- Configure the database server to log all queries to "stderr"
- Fix SQL injection flaw in the "payroll" web application ("app\_code/payroll/server.py)
- Configure and utilize "PGAudit" extension from granular query logging


## Lab report/documentation
Each student should submit a lab report containing **at least** the following information:
- Documentation of how each task was performed, including reasoning behind solution
- Documentation of verification steps taken to validate effect of each task
  
The lab report should be provided as a plain text file (".txt"), Markdown document or PDF file.
In addition to the report, all lab files that have been changed (scripts, configuration sets,
screenshots, etc.) should be provided as a ZIP or GZIP archive.  
  
Upload lab report and archive of changed files to
%REPORT_TARGET%.


## Guidance and resources

### Problems accessing lab web applications
The web application containers utilize port forwarding rules to expose their web server and make it
accessible on the system where the Docker containers are running. If the lab environment is
running in a Vagrant VM, an additional layer of port forwarding is setup to enable direct access to
the web applications from the student's host computer.  

If the student has issues related to accessing the lab applications using the web browser in their
host operating system, ensure that the latest version of the lab system Vagrantfile
("resources/labs/Vagrantfile") is utilized as earlier versions didn't setup the previously
described port forwarding automatically.


### Relevant lab files
The lab environment consists of several files to build, setup and run the containers for the web
applications and database. Many of these doesn't however need to be modified/reviewed by the
student to complete the lab. The list below contain file paths (relative to the lab directory) and
a short purpose description of files that the student is required to understand and/or modify:

- "docker-compose.yml": Describes how all containers should be run. Contains credentials for DB
- "app\_configuration/\*.yml": Configuration files for applications. Contains credentials for DB
- "app\_code/\*/server.py": Python source code for web applications
- "database/first\_startup\_scripts/initialize.sql": Script setting up database and default data
- "database/postgresql.conf": Configuration file for database server shared with container
- "postgres\_client.sh": Basic script for executing the PostgreSQL CLI client in jumpbox container


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
The web application and database containers produce log messages which may be useful to review.
To follow/show the log stream of all lab containers, execute the following command:

```
$ docker compose logs --follow
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
the example web applications. If the Python source code of these applications is changed, they
may however not be automatically rebuilt. As this can cause problems and make testing changes
difficult, make sure to always include the "--build" flag when starting up the Compose environment:

```
$ docker compose up --build --detach
```


### Hostname resolution in Compose
When specifying multiple containers/services in a Docker Compose file, the different
containers/services can utilize each others names to as network host names instead of specifying
IP addresses in configuration options. This means that a service called "web" can connect to the
database container "db" using the host name "db". For more information, see "Links" section below.


### Enabling application debug logging
The lab application supports debug message logging by setting the option "log_level" to "DEBUG" in
the applications' configuration file ("app\_configuration/agents.yml", for example). This will
increase the verbosity of log messages, but may aid the student when investigating problems or
implementing changes.


### "Errno -3: Try again!"
If any of the web applications fail to start due to the database error "Errno -3: Try again!",
it means that the application couldn't resolve the hostname specified in the database URI.
Ensure that the correct hostname is used (matching the application container's name in the file
"docker-compose.yml") and that the correct remote is specified in the application configuration
file in "app\_configuration/\*.yml.


### "ERROR: permission denied for sequence..."
If error messages containing "ERROR: permission denied for sequence" appear in the database role,
it likely means that the database user don't have sufficient privileges to query/modify the
"sequence tables" in the agency database. For more information and an example how this type of
permission problem can be solved, see the file "database/first\_startup\_scripts/initialize.sql".


### Accessing database as user/administrator
The container "jumpbox.int.agency.test" contains a CLI PostgreSQL client, useful for manipulating
tables, adding users/roles and testing queries as unprivileged users in the database. This program 
can be used by executing a command in the running container and supplying the database connection
details/user credentials specified in "docker-compose.yml". To ease the process and directly gain
a SQL prompt, the shell script "postgres\_client.sh" (found in the lab directory) can be executed
with a PostgreSQL connection URI:

```
$ cd /course_data/labs/sec
$ ./postgres_client.sh "postgresql://db_admin:Ct=Snackul4@database.int.agency.test/agency_data"
```

Additional options for the "psql" command can be supplied by appending them as arguments to the
script:

```
$ ./postgres_client.sh --help
```


### Asking for assistance
In order to minimize repeated answers to recurring questions, several common issues are brought up
in the lab description (this README file). The teacher should also update the guidance section of
the lab description if such need arises during the course. Before requesting help/guidance from the
course leader, the student should utter the secret passphrase "covfefe".


### Links
- [Vagrant port forwards](https://developer.hashicorp.com/vagrant/docs/networking/forwarded_ports)
- ["Compose" getting started guide](https://docs.docker.com/get-started/08_using_compose/)
- ["Compose" networking overview](https://docs.docker.com/compose/networking/)
- [PostgreSQL image on Docker Hub](https://hub.docker.com/_/postgres/)
- ["psql" command documentation](https://www.postgresql.org/docs/current/app-psql.html)
- [PGSQL connection URIs](https://www.prisma.io/dataguide/postgresql/short-guides/connection-uris)
- [PostgreSQL Tutorials - CREATE role](https://www.postgresqltutorial.com/postgresql-administration/postgresql-roles/)
- [PostgreSQL Tutorials - GRANT privileges](https://www.postgresqltutorial.com/postgresql-administration/postgresql-grant/)
- [EDB tutorials - Column-/Row-level security](https://www.enterprisedb.com/postgres-tutorials/how-implement-column-and-row-level-security-postgresql)
- [BetterStack - Postgres logging](https://betterstack.com/community/guides/logging/how-to-start-logging-with-postgresql/)
- [OWASP - SQL injection overview](https://owasp.org/www-community/attacks/SQL_Injection)
- [psycopg - Passing query parameters](https://www.psycopg.org/psycopg3/docs/basic/params.html)
- [OWASP - Cross-Site Request Forgery overview](https://owasp.org/www-community/attacks/csrf)
- [PGAudit extension documentation](https://github.com/pgaudit/pgaudit/blob/master/README.md)
