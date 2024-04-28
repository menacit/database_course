<!--
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0
X-Context: Database course - Operations lab - Assignment description
-->

# Database course - Operations lab

## Scenario description
You're suddenly awakened from your slumber by a distraught scream from the neighboring cubical:
"git revert!! git revert!!!111one". After helping your coworker to calm down enough to utter
understandable sentences, you've realized what just happened. The Big Boss just forwarded an angry
email from the government's auditors complaining that they can no longer access our mission
reports.
  
After some digging around, you realize that (despite what everyone wholeheartedly promised)
they've been given direct access to the SQL database - that's right, the same SQL database you've
just finished migrating from in favor of OpenSearch. Apparently they've built a complex system
around this and "can't possibly be expected to change it on such a short notice". No biggie, let's
just store the reports in both PostgreSQL and OpenSearch for now - that should make everyone happy,
right?  

Besides the complaints (written in ALL CAPS, of course), the email also referred to several legal
requirements that the agency must follow to keep the "license to kill". Skimming through these,
you realize that both highly-available data access and meticulous disaster recovery plans are
mandatory.  

Once again, the agency's future depend on you rolling up those sleeves. Besides, nothing compares
to the joy experienced when legal requirements are fulfilled! 


## Learning objectives
Practical knowledge of high-availability/disaster recovery of PostgreSQL and OpenSearch.


## Lab overview
The lab consist of a simple Python web application, used to store the agency's mission reports in
PostgreSQL and OpenSearch, and several containers running database servers.  These services are
packaged as Docker containers and pre-configured to be run using Docker Compose. In order to
start the containers, navigate to the operations lab directory ("resources/labs/ops") on the
student's lab system (typically Vagrant VM) and execute the Docker Compose command:

```
$ cd /course_data/labs/ops
$ docker compose up --build --detach
```

All tools required to complete the assignment should be pre-installed on the student's lab system. 


## Lab applications/containers
The sections below describe the purpose of each lab container managed by Docker Compose.


### "sql-database-1.int.agency.test"
Container running PostgreSQL server, utilized by the "missions" web application. Configured to
automatically setup a database and a user account for the administrator user (see "environment"
section of container in "docker-compose.yml").


### "sql-database-2.int.agency.test"
Container used for running PostgreSQL server as a read replica for "sql-database-1". Configured to
automatically setup a user account for the administrator user (see "environment" section of
container in "docker-compose.yml").


### "jumpbox.int.agency.test"
Basic container that provides the "psql" and curl/HTTPie CLI utilities for managing/querying the
databases. For more information, see "Accessing databases as user/administrator" heading of the
guidance section below.


### "missions.int.agency.test"
Container running the "missions" web application ("missions\_app/server.py") used to submit agent
mission reports. The web application is exposed to the lab system using port forwarding and should
be accessible using the URL "http://127.0.0.1:10006". Credentials for access is available in the
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
system using port forwarding and should be accessible using the URL "http://127.0.0.1:10007".
Credentials for authentication can be found in the environment variables for the
"opensearch.int.agency.test" container/service in "docker-compose.yml"


## Tasks
As this exercise is a practice lab, none of the tasks below are graded. The student should, to the
best of their abilities, try to complete as many of the tasks below during the course.

- Startup lab environment using Docker Compose and validate access to web applications/databases
- Manually or automatically (see "submit\_example\_reports.sh") mission reports for testing
- Perform backup and restore of "missions" index in OpenSearch
  - Configure a "file system based" snapshot repository at "/var/opensearch\_snapshots"
  - Trigger snapshot execution
  - Modify/Delete stored documents
  - Restore snapshot and validate result
  
- Perform backup and restore of "mission\_data" table in PostgreSQL ("sql-database-1")
  - Utilize the "pg\_dump" utility in the "jumpbox" container to perform backup
  - Modify/Delete stored rows
  - Restore backup and validate result
  
- Configure "sql-database-2" as a read replica of "sql-database-1" for high-availability
  - Validate result by disabling "sql-database-1" and executing SELECT queries against the replica


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
- "database/sql-database-1/pg\_hba.conf": Authentication configuration for database container
- "sql-database-2\_shell.sh": Basic script for starting a command-line shell in database container
- "database/opensearch/snapshots": Directory shared with OpenSearch container for snapshot storage
- "jumpbox\_shell.sh": Basic script for starting a command-line shell in jumpbox container
- "jumpbox/share": Directory shared with jumpbox container, available at container path "/share"
- "missions\_app/configuration.yml": Configuration for "missions" web app. Contains credentials
- "submit\_example\_reports.sh": Script to populate databases with example mission reports


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
$ docker compose logs --follow sql-database-1.int.agency.test
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
$ docker volume rm ops_sql_database_1_data
$ docker volume rm ops_sql_database_2_data
$ docker volume rm ops_nosql_database_data
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
$ psql "postgresql://admin:Ct=Snackul4@sql-database-1.int.agency.test/mission_data"
```

Alternatively, additional command-line arguments can be provided to the script which will be
executed directly inside the container:

```
$ ./jumpbox_shell.sh \
  https --verify=no GET "admin:Ct=Snackul4@opensearch.int.agency.test:9200/_cluster/health"
```


### Stopping specific containers/services
In order to selectively stop a specific container in the Compose environment, issue a command
similar to the one demonstrated below:

```
$ docker compose stop sql-database-1.int.agency.test
```


### Restarting/Reloading PostgreSQL
When certain server/authentication configuration options are modified in PostgreSQL, the process
must be reloaded or restarted for the changes to take effect.  
  
Many guides instruct the administrator to restart PostgreSQL using commands like
"systemctl restart postgresql.service" or "/etc/init.d/postgresql restart". These commands are
however not applicable to the lab environment as the PostgreSQL process is directly executed in
the database containers. An equivalent option would be issuing the following command:

```
$ docker compose restart sql-database-1.int.agency.test
```


### Accessing OS shell on sql-database-2
In order to enable easy access to an "operating system" shell for modifying arbitrary files and
issuing commands in the container "sql-database-2.int.agency.test", execute the command below in
the lab directory ("resources/labs/ops"):

```
$ ./sql-database-2_shell.sh
```


### Enabling PostgreSQL on sql-database-2
Backup/Configuration tools like "pg\_basebackup" requires deletion and modification of files
actively utilized by a running PostgreSQL server process. A common practice is to temporarily stop
the server process before executing these types of tools and enabling it afterward.
  
Due to the way PostgreSQL is executed in the lab environment, this is however not trivial and the
server process is therefore not automatically executed in the secondary database container.
In order to enable it, modify "docker-compose.yml" and comment out/remove the "entrypoint" option
for the "sql-database-2.int.agency.test" container/service. After performing changes to the Compose
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
course leader, the student should utter the secret passphrase "hack the planet".


### Links
- [Vagrant port forwards](https://developer.hashicorp.com/vagrant/docs/networking/forwarded_ports)
- ["Compose" getting started guide](https://docs.docker.com/get-started/08_using_compose/)
- ["Compose" networking overview](https://docs.docker.com/compose/networking/)
- [PostgreSQL image on Docker Hub](https://hub.docker.com/_/postgres/)
- ["psql" command documentation](https://www.postgresql.org/docs/current/app-psql.html)
- [PGSQL connection URIs](https://www.prisma.io/dataguide/postgresql/short-guides/connection-uris)
- [HTTPie usage guide](https://httpie.io/docs/cli/usage)
- [OpenSearch "Dev Tools" console](https://opensearch.org/docs/latest/dashboards/dev-tools/index-dev/)
- [OpenSearch - Take/Restore snapshots](https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
- [OpenSearch Dashboards - Snapshot management](https://opensearch.org/docs/latest/dashboards/sm-dashboards/)
- [PostgreSQL documentation - "pg\_dump"](https://www.postgresql.org/docs/current/app-pgdump.html)
- [PostgreSQL documentation - High-availability](https://www.postgresql.org/docs/current/high-availability.html)
- [PostgreSQL documentation - "Warm standby"](https://www.postgresql.org/docs/current/warm-standby.html)
- [PostgreSQL documentation - "pg\_basebackup"](https://www.postgresql.org/docs/current/app-pgbasebackup.html)
- [DO Tutorials - Streaming replication with PostgreSQL](https://www.digitalocean.com/community/tutorials/how-to-set-up-physical-streaming-replication-with-postgresql-12-on-ubuntu-20-04)
