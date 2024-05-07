---
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0

title: "Database course: Introducing ORM"
author: "Joel Rangsmo <joel@menacit.se>"
footer: "© Course authors (CC BY-SA 4.0)"
description: "Introduction to ORMs in database course"
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
  table strong {
    color: #d63030;
  }
  table em {
    color: #2ce172;
  }

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Lisa Brewster (CC BY-SA 2.0)" -->
# Introducing ORM
### Object-Relational Mapping

![bg right:30%](images/18-cabling.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Lisa Brewster (CC BY-SA 2.0)" -->
Databases are great backing stores
for our applications' persistent data.  

Much of our code is just used to
retrieve/store information to/from
objects or other data structures.

![bg right:30%](images/18-cabling.jpg)

---
```python
[...]

_log.info('Querying gadgets available for agents')
available_gadgets = []

cursor.execute('SELECT id, name, price FROM gadgets ORDER by price ASC')
available_gadget_query_results = cursor.fetchall()

for available_gadget_query_result in available_gadget_query_results:
    available_gadgets.append({
        'gadget_id': available_gadget_query_result[0],
        'name': available_gadget_query_result[1],
        'price': available_gadget_query_result[2]
    })

[...]
```

---
```python
[...]

_log.info(f'"{app_user}" added newgadget')

database_handle.execute(
  'INSERT INTO gadgets (name, price) VALUES (%s, %s)',
  (gadget['name'], gadget['price']))

[...]
```

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Raphaël Vinot (CC BY 2.0)" -->
Becomes repetitive and quite boring.  

Don't even get me started on relations!

Wouldn't it be great if we somehow could
map attributes/fields in our data structures
to tables and colums in a SQL database?

![bg right:30%](images/18-arecibo_dish.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Bixentro (CC BY 2.0)" -->
## Object-Relational Mapping
Technique/Tools used in programming to
automatically convert data structures
to database entries on read/write.  

Especially popular in
object-oritented programming laguages.  

You don't need to care about
database queries (and injection flaws)\*,
for good and bad.

![bg right:30%](images/18-pcb_baby.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Rod Waddington (CC BY-SA 2.0)" -->
Programming in Python?

[Pony](https://docs.ponyorm.org) or [SQLAlchemy](https://www.sqlalchemy.org/)
are two decent options.  

Let's take Pony for a ride!

![bg right:30%](images/18-adis_bar.jpg)

---
```python
from pony.orm import *

db = Database()

class Agent(db.Entity):
    name = Required(str)
    code_name = Optional(str, unique=True)
    salary = Required(int)
    gadgets = Set('Gadget')
    missions = Set('Mission')

class Gadget(db.Entity):
    name = Required(str)
    price = Required(int)
    owner = Optional(Agent)

class Mission(db.Entity):
    code_name = Required(str)
    participants = Set(Agent)

[...]
```

---
```python
[...]

db.bind(
    provider='sqlite',
    filename=':sharedmemory:')

set_sql_debug(True)
db.generate_mapping(create_tables=True)
```

---
```sql
BEGIN IMMEDIATE TRANSACTION

CREATE TABLE "Agent" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "name" TEXT NOT NULL,
  "code_name" TEXT UNIQUE,
  "salary" INTEGER NOT NULL
)

CREATE TABLE "Gadget" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "name" TEXT NOT NULL,
  "price" INTEGER NOT NULL,
  "owner" INTEGER REFERENCES "Agent" ("id") ON DELETE SET NULL
)

CREATE INDEX "idx_gadget__owner" ON "Gadget" ("owner")

CREATE TABLE "Mission" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "code_name" TEXT NOT NULL
)

[...]
```


---
```sql
[...]

CREATE TABLE "Agent_Mission" (
  "agent" INTEGER NOT NULL REFERENCES "Agent" ("id") ON DELETE CASCADE,
  "mission" INTEGER NOT NULL REFERENCES "Mission" ("id") ON DELETE CASCADE,
  PRIMARY KEY ("agent", "mission")
)

CREATE INDEX "idx_agent_mission" ON "Agent_Mission" ("mission")

COMMIT
```

---
```python
with db_session:
    spy_watch = Gadget(
        name='Omicron Spymaster watch',
        price=92500) 
    
    madam = Agent(
        name='Malory Archer',
        code_name='Madam', salary=55000)
    
    duchess = Agent(
        name='Sterling Archer',
        code_name='Duchess', salary=42000)
    
    theft_mission = Mission(
        code_name='Cracked Meatball')
    
    duchess.gadgets.add(spy_watch)
    theft_mission.participants.add(duchess)
```

---
```sql
BEGIN IMMEDIATE TRANSACTION

INSERT INTO "Agent" ("name", "code_name", "salary") VALUES (?, ?, ?)
['Sterling Archer', 'Duchess', 42000]

INSERT INTO "Gadget" ("name", "price", "owner") VALUES (?, ?, ?)
['Omicron Spymaster watch', 92500, 1]

INSERT INTO "Agent" ("name", "code_name", "salary") VALUES (?, ?, ?)
['Malory Archer', 'Madam', 55000]

INSERT INTO "Mission" ("code_name") VALUES (?)
['Cracked Meatball']

INSERT INTO "Agent_Mission" ("agent", "mission") VALUES (?, ?)
[1, 1]

COMMIT
```

---
```python
with db_session:
    for name in select(a.name for a in Agent):
        print(name)
```

---
```sql
SWITCH TO AUTOCOMMIT MODE

SELECT DISTINCT "a"."name"
FROM "Agent" "a"
```

---
```python
with db_session:
    print(Agent.get(code_name='Madam').name)
```

---
```sql
SWITCH TO AUTOCOMMIT MODE

SELECT "id", "name", "code_name", "salary"
FROM "Agent"
WHERE "code_name" = ?
['Madam']
```

---
```python
with db_session:
    for gadget in Agent.get(
        code_name='Duchess').gadgets:

        print(gadget.name)
```

---
```sql
SWITCH TO AUTOCOMMIT MODE

SELECT "id", "name", "code_name", "salary"
FROM "Agent"
WHERE "code_name" = ?
['Duchess']

SELECT "id", "name", "price", "owner"
FROM "Gadget"
WHERE "owner" = ?
[1]
```

---
```python
with db_session:
    for expensive_agent in select(
        a for a in Agent
            if a.salary > 8000 and
            a.name != 'Malory Archer' ):

        print(expensive_agent.name)
        expensive_agent.salary -= 1000
```

---
```sql
SWITCH TO AUTOCOMMIT MODE

SELECT "a"."id", "a"."name", "a"."code_name", "a"."salary"
FROM "Agent" "a"
WHERE "a"."salary" > 8000
  AND "a"."name" <> 'Malory Archer'

BEGIN IMMEDIATE TRANSACTION

UPDATE "Agent"
SET "salary" = ?
WHERE "id" = ?
  AND "name" = ?
  AND "code_name" = ?
  AND "salary" = ?
[41000, 1, 'Sterling Archer', 'Duchess', 42000]

COMMIT
```

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Tim Green (CC BY 2.0)" -->
## The downsides
Database structure and queries
may not be optimal for your use-case.  

Fancy DBMS-specific features may
be inacessible through ORM.  

Other layer of abstraction and
complex software dependencies
that can introduce bugs.

![bg right:30%](images/18-moss_face.jpg)
