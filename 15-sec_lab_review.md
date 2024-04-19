---
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0

title: "Database course: Security lab review"
author: "Joel Rangsmo <joel@menacit.se>"
footer: "© Course authors (CC BY-SA 4.0)"
description: "Review of security lab in the database course"
keywords:
  - "database"
  - "db"
  - "sql"
  - "nosql"
  - "course"
color: "#ffffff"
class:
  - "invert"
style: |
  section.center {
    text-align: center;
  }

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Brendan J (CC BY 2.0)" -->
# Security lab
### Exercise review / walk-through

![bg right:30%](images/15-cyberpunk_wall.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Brendan J (CC BY 2.0)" -->
## Learning objectives
> Practical knowledge of
> access/privilege control, logging and
> injection mitigation in SQL databases.

_From "resources/labs/sec/README.md"._

![bg right:30%](images/15-cyberpunk_wall.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% William Warby (CC BY 2.0)" -->
## TL;DR
We got three web applications,
"agents", "gadgets" and "payroll".  

They all utilize the same user account
in a PostgreSQL database (bad!).  

There is no logging enabled and one of
the apps has a "SQL injection" flaw.  

The web applications and database are
packaged in Docker containers and
run using "Docker Compose".

![bg right:30%](images/15-dummy.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Jan Helebrant (CC0 1.0)" -->
## Lab tasks summarized
1. Start/test lab environment
2. Restrict database access for apps
3. Enable basic query logging
4. Fix SQL injection vulnerability
5. Configure fine-grained logging

![bg right:30%](images/15-ancient_stairs.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Todd Van Hoosear (CC BY-SA 2.0)" -->
## Starting up lab environment

### Host computer
```
$ cd database_course/resources/labs
$ vagrant up && vagrant ssh
```

### Lab system (guest)
```
$ cd /course_data/labs/sec
$ docker compose up --build --detach
```

![bg right:30%](images/15-engine.jpg)

---
![bg center 75%](images/15-sec_lab_agents_index.png)

---
![bg center 75%](images/15-sec_lab_agents_profile.png)

---
![bg center 75%](images/15-sec_lab_gadgets_index.png)

---
![bg center 75%](images/15-sec_lab_payroll_index.png)

---
![bg center 75%](images/15-sec_lab_payroll_salary.png)

---
## Accessing the database
```
$ ./postgres_client.sh \
  "postgresql://db_admin:Ct=Snackul4@database.int.agency.test/agency_data"

psql (16.2 (Debian 16.2-1.pgdg120+2))
Type "help" for help.

agency_data=#
```

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Jan Helebrant (CC0 1.0)" -->
## Lab tasks summarized
1. ~~Start/test lab environment~~
2. Restrict database access for apps
3. Enable basic query logging
4. Fix SQL injection vulnerability
5. Configure fine-grained logging

![bg right:30%](images/15-ancient_stairs.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Jeena Paradies (CC BY 2.0)" -->
## Creating per-app users
```sql
CREATE ROLE app_agents WITH
LOGIN PASSWORD 'arandompassword';
```

(and update "app\_configuration/agents.yml")

![bg right:30%](images/15-stones.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Edenpictures (CC BY 2.0)" -->
## Privilege requirements
Which parts of the database do
each application really need?  

High-level analysis based on
purpose/functionality.  

Low-level analysis using
source-code review or
query logging.

![bg right:30%](images/15-abstract_house.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Rob Hurson (CC BY-SA 2.0)" -->
## Privileges for agents app
```sql
GRANT SELECT ON
	agents, gadgets, gadget_assignments
TO app_agents;

GRANT INSERT
ON gadget_assignments
TO app_agents;

GRANT UPDATE
ON gadget_assignments_id_seq
TO app_agents;
```

![bg right:30%](images/15-bunker_tower.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Pyntofmyld (CC BY 2.0)" -->
## Privileges for gadgets app
```sql
GRANT SELECT, INSERT
ON gadgets
TO app_gadgets;

GRANT UPDATE
ON gadgets_id_seq
TO app_gadgets;
```

![bg right:30%](images/15-bubbles.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC BY 2.0)" -->
## Privileges for payroll app
```sql
CREATE VIEW salaries AS
SELECT id, name, salary
FROM agents;

GRANT SELECT, UPDATE
ON salaries
TO app_payroll;
```

![bg right:30%](images/15-swaths.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC BY 2.0)" -->
## Modifying payroll app
```
$ sed -i \
  's/FROM agents/FROM salaries/g' \
  app_code/payroll/server.py
```

![bg right:30%](images/15-swaths.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Kārlis Dambrāns (CC BY 2.0)" -->
## Revoking access
```sql
REVOKE ALL PRIVILEGES
ON ALL TABLES IN SCHEMA public
FROM shared_app_user;

REVOKE ALL PRIVILEGES
ON ALL SEQUENCES IN SCHEMA public
FROM shared_app_user;

DROP ROLE shared_app_user;
```

![bg right:30%](images/15-fire.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Jan Helebrant (CC0 1.0)" -->
## Lab tasks summarized
1. ~~Start/test lab environment~~
2. ~~Restrict database access for apps~~
3. Enable basic query logging
4. Fix SQL injection vulnerability
5. Configure fine-grained logging

![bg right:30%](images/15-ancient_stairs.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Fredrik Rubensson (CC BY-SA 2.0)" -->
## Enabling query logging
Append to "database/postgresql.conf":

```
log_statement = 'all'
log_destination = 'stderr'
```

Restart containers:

```
$ docker compose restart 
```

![bg right:30%](images/15-log_on_log.jpg)

---
## Reviewing query logs
```
$ docker compose logs database.int.agency.test --follow

[...]
database.int.agency.test-1  |
2024-04-16 14:42:39.870 GMT [1212]
LOG:  execute <unnamed>:
SELECT id, name, code_name, salary FROM agents WHERE id = $1         

database.int.agency.test-1  |
2024-04-16 14:42:39.870 GMT [1212]
DETAIL:  parameters: $1 = '5'
```

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Jan Helebrant (CC0 1.0)" -->
## Lab tasks summarized
1. ~~Start/test lab environment~~
2. ~~Restrict database access for apps~~
3. ~~Enable basic query logging~~
4. Fix SQL injection vulnerability
5. Configure fine-grained logging

![bg right:30%](images/15-ancient_stairs.jpg)
