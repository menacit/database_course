<!--
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0
X-Context: Database course - NoSQL lab - Assignment description
-->

# Database course - NoSQL lab

## Scenario description
In a futile attempt to make the agency look like a functioning workplace and discourage lavish
side-quests financed using the company credit card, management put stringent requirements on
documenting all mission activity. While a simple application was built to support the reporting,
no one ever bothered to build an interface to actually look through the submitted data. Funny how
things go sometimes.  
  
It's years later and fancy consultants have been hired to "bring out the agency's full potential".
"BIG DATA, DATA IS THE NEW GOLD - YOU MUST MINE IT!", they all screamed synchronously. As it
happens, the agency got all those mission reports laying around - perhaps they could be of use?  
  
Then again, the programmers never got around building an interface to actually look at the data.
"Just use psql and connect, noob!", they said - as if management ever would. Luckily, you know of
a great tool that provides both advanced search capabilities and a slick web UI to produce those
sparkling graphs that everyone loves.  
  
What are you waiting for? Let's migrate to OpenSearch and pray for a raise!


## Learning objectives
Practical knowledge of the NoSQL datastore "OpenSearch" and its query/visualization capabilities.


## Lab overview
The lab consist of... These services are
packaged as Docker containers and pre-configured to be run using Docker Compose. In order to
start the containers, navigate to the NoSQL lab directory ("resources/labs/nosql") on the student's
lab system (typically Vagrant VM) and execute the Docker Compose command:

```
$ cd /course_data/labs/nosql
$ docker compose up --build --detach
```

All tools required to complete the assignment should be pre-installed on the student's lab system. 


## Lab applications/containers
The sections below describe the purpose of each lab container managed by Docker Compose.


### "legacy-database.int.agency.test"
Container running PostgreSQL server, utilized by the "missions" web application. Configured to
automatically setup a database and a user account for the administrator user (see "environment"
section of container in "docker-compose.yml").


### "jumpbox.int.agency.test"
Basic container that provides the "psql" and curl/HTTPie CLI utilities for managing/querying the
databases. For more information, see "Accessing databases as user/administrator" heading of the
guidance section below.


### "missions.int.agency.test"
Container running the "missions" web application ("missions\_app/server.py") used to submit agent
mission reports. The web application is exposed to the lab system using port forwarding and should
be accessible using the URL "http://127.0.0.1:10004". Credentials for access is available in the
file "missions\_app/configuration.yml".


### "opensearch.int.agency.test"
Container running the OpenSearch datastore, utilized by the "missions" web application. Credentials
for authentication can be found in the environment variables for the "opensearch.int.agency.test"
container/service in "docker-compose.yml"


### "opensearch-app-user-configurator"
Container running the command-line HTTP client "curl" to create/configure a user account for the
"missions" app in OpenSearch via its REST API. Doesn't expose any services after initial execution.


### "dashboards.int.agency.test"
Container running the web application "OpenSearch Dashboards", which can be used to query,
manipulate and visualize documents stored in OpenSearch. The web application is exposed to the lab
system using port forwarding and should be accessible using the URL "http://127.0.0.1:10005".
Credentials for authentication can be found in the environment variables for the
"opensearch.int.agency.test" container/service in "docker-compose.yml"


## Tasks
As this exercise is a practice lab, none of the tasks below are graded. The student should, to the
best of their abilities, try to complete as many of the tasks below during the course.

- Startup lab environment using Docker Compose and validate access to web applications in a browser
- Submit a couple of example reports in the "missions" web application
- Modify the "missions" web application to store reports in OpenSearch index instead of PostgreSQL
- Create a query in OpenSearch Dashboards to filter reports based on the following requirements:
  - Must have ended within the last year
  - Must include the agent "Monster Hands" _or_ "Duchess" as participant
  - Should include the agent "Gilles de Rais" as participant
  - Should have a mission cost above 6000 USD
  - Should include the term "expense" in report text

- Configure explicit field mapping index to define the "location" field as "geo\_point"
- Create visualization with pie chart of participants were the mission location is Stockholm
- Write script to migrate data from PostgreSQL database to OpenSearch index
- Restrict privileges for the "app user in OpenSearch (see "database/opensearch\_app\_user.json")


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
The lab environment consists of several files to build, setup and run the containers for the (web)
applications and database. Many of these doesn't however need to be modified/reviewed by the
student to complete the lab. The list below contain file paths (relative to the lab directory) and
a short purpose description of files that the student is required to understand and/or modify:

- "docker-compose.yml": Describes how all containers should be run. Contains credentials
- "database/first\_startup\_scripts/initialize.sql": Script setting up the SQL DB and default data
- "jumpbox\_shell.sh": Basic script for starting a command-line shell in jumpbox container
- "jumpbox/share": Directory shared with jumpbox container, available at container path "/share"
- "missions\_app/server.py": Python source code for "missions" web app
- "missions\_app/configuration.yml": Configuration for "missions" web app. Contains credentials


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
$ docker volume rm nosql_sql_database_data
$ docker volume rm nosql_nosql_database_data
```


### Hostname resolution in Compose
When specifying multiple containers/services in a Docker Compose file, the different
containers/services can utilize each others names to as network host names instead of specifying
IP addresses in configuration options. This means that a service called "web" can connect to the
database container "db" using the host name "db". For more information, see "Links" section below.


### Enabling application debug logging
The lab application supports debug message logging by setting the option "log_level" to "DEBUG" in
the applications' configuration file ("missions\_app/configuration.yml"). This will increase the
verbosity of log messages, but may aid the student when investigating problems or implementing
changes.


### "Errno -3: Try again!"
If the "missions" web application fail to start due to the database error "Errno -3: Try again!",
it means that the application couldn't resolve the hostname specified in the database URI.
Ensure that the correct hostname is used (matching the application container's name in the file
"docker-compose.yml") and that the correct remote is specified in the application configuration
file in "missions\_app/configuration.yml.


### Accessing databases as user/administrator
In order to query/update/migrate the databases, the container "jumpbox.int.agency.test" is provided
with pre-installed clients and Python modules for HTTP, PostgreSQL and OpenSearch. To enable easy
access, a simple wrapper-script exist to spawn a shell in the running container:

```
$ cd /course_data/labs/ops
$ ./jumpbox_shell.sh
```

Once inside the shell, commands can be executed interactively:

```
$ psql "postgresql://admin:Ct=Snackul4@legacy-database.int.agency.test/mission_data"
```

Alternatively, additional command-line arguments can be provided to the script which will be
executed directly inside the container:

```
$ ./jumpbox_shell.sh \
  https --verify=no GET "admin:Ct=Snackul4@opensearch.int.agency.test:9200/_cluster/health"
```


### OpenSearch TLS/certificate errors
The OpenSearch container utilizes a "self-signed" X.509 certificate to support TLS (HTTPS).
This certificate is not signed by a certificate authority included in default trust-stores and
attempts to perform HTTP(S) requests to OpenSearch may result in errors such as:

```
curl: (60) SSL certificate problem: self-signed certificate
curl failed to verify the legitimacy of the server...
```

To ignore this error, configure the client to disable validation of server certificates. In curl,
the command-line flag "--insecure" may be included. In HTTPie, the option is "--verify=no".
Do however note that usage of these types of certificates and disabled validation is highly
discouraged in production environments.


### Finding more OpenSearch documentation/examples
As mentioned during the lectures, OpenSearch is a fork of Elasticsearch/Kibana. While the projects
have started to diverge, most tutorials and documentation describing how to solve problems in
Elasticsearch also applies to OpenSearch. If the official OpenSearch documentation does not explain
a concept, try including "Elasticsearch" in search terms.


### Asking for assistance
In order to minimize repeated answers to recurring questions, several common issues are brought up
in the lab description (this README file). The teacher should also update the guidance section of
the lab description if such need arises during the course. Before requesting help/guidance from the
course leader, the student should utter the secret passphrase "hunter2".


### Links
- [Vagrant port forwards](https://developer.hashicorp.com/vagrant/docs/networking/forwarded_ports)
- ["Compose" getting started guide](https://docs.docker.com/get-started/08_using_compose/)
- ["Compose" networking overview](https://docs.docker.com/compose/networking/)
- [PostgreSQL image on Docker Hub](https://hub.docker.com/_/postgres/)
- ["psql" command documentation](https://www.postgresql.org/docs/current/app-psql.html)
- [PGSQL connection URIs](https://www.prisma.io/dataguide/postgresql/short-guides/connection-uris)
- [OpenSearch CLI documentation](https://opensearch.org/docs/latest/tools/cli/)
- [HTTPie usage guide](https://httpie.io/docs/cli/usage)
- [Introduction to OpenSearch](https://opensearch.org/docs/latest/getting-started/intro/)
- [Basic CRUD in OpenSearch](https://opensearch.org/docs/latest/getting-started/communicate/)
- [OpenSearch query DSL documentation ("Lucene")](https://opensearch.org/docs/latest/query-dsl/)
- [OpenSearch Dashboards documentation](https://opensearch.org/docs/latest/dashboards/)
- [OpenSearch Python client documentation](https://opensearch-project.github.io/opensearch-py/)
- [Opensearch Python client basic usage guide](https://github.com/opensearch-project/opensearch-py/blob/main/USER_GUIDE.md)
- [OpenSearch - Mappings and field types](https://opensearch.org/docs/latest/field-types/)
- [OpenSearch Dashboards - Using maps](https://opensearch.org/docs/latest/dashboards/visualize/geojson-regionmaps/)
