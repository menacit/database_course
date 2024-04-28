---
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0

title: "Database course: NoSQL lab review"
author: "Joel Rangsmo <joel@menacit.se>"
footer: "© Course authors (CC BY-SA 4.0)"
description: "Review of NoSQL lab in the database course"
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
<!-- _footer: "%ATTRIBUTION_PREFIX% Marcin Wichary (CC BY 2.0)" -->
# NoSQL lab
### Exercise review / walk-through

![bg right:30%](images/16-abandoned_factory.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Marcin Wichary (CC BY 2.0)" -->
## Learning objectives
> Practical knowledge of
> the NoSQL datastore "OpenSearch"
> and its query/visualization capabilities.

_From "resources/labs/nosql/README.md"._

![bg right:30%](images/16-abandoned_factory.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Mauricio Snap (CC BY 2.0)" -->
## TL;DR
We got a Python web app for
submission of mission reports.  
  
Reports are currently stored in
PostgreSQL, but should be migrated
to the OpenSearch datastore.  

Once migrated, we need to develop
queries/visualizations for the
mission report data.

![bg right:30%](images/16-eye.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Scott McCallum (CC BY-SA 2.0)" -->
## Lab tasks summarized
1. Start/test lab environment
2. Migrate from PostgreSQL to OpenSearch
3. Develop query to filter/sort reports
4. Query/Visualize data from reports in specific geographic region

![bg right:30%](images/16-turtle.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Wolfgang Stief (CC0 1.0)" -->
## Starting up lab environment

### Host computer
```
$ cd database_course/resources/labs
$ vagrant up && vagrant ssh
```

### Lab system (guest)
```
$ cd /course_data/labs/nosql
$ docker compose up --build --detach
```

![bg right:30%](images/16-apple_ii_inside.jpg)

---
![bg center 30%](images/16-missions_app.png)

---
## Accessing the SQL database
```
$ ./jumpbox_shell.sh psql \
  "postgresql://admin:Ct=Snackul4@legacy-database.int.agency.test/missions"

psql (16.2 (Debian 16.2-1.pgdg120+2))
Type "help" for help.

missions=#
```

---
![bg center 75%](images/16-opensearch_01.png)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Scott McCallum (CC BY-SA 2.0)" -->
## Lab tasks summarized
1. ~~Start/test lab environment~~
2. Migrate from PostgreSQL to OpenSearch
3. Develop query to filter/sort reports
4. Query/Visualize data from reports in specific geographic region

![bg right:30%](images/16-turtle.jpg)

---
### Heading of "missions\_app/server.py"

```json
'''
missions - Web application to submit mission logs.

Expects missions report in JSON format subbmitted to the "/submit_report" end-point.
Example report data:

{
  "code_name":"Bum Fight At Night",
  "start_datetime":"2024-12-02T01:00", "end_datetime":"2024-12-02T03:30",
  "budget": 500, "cost": 861,
  "report":"Everything went as expected - the subjects started to brawl in the alley.",
  "location":{"lat":"40.783679409824956","lon":"-77.85092353820802"},
  "participants":[
    "Duchess",
    "Gilles de Rais"
  ],
  "used_gadgets":[
    "Fake mustache",
    "Stinky overcoat",
    "Bottle of brandy"
  ]
}
'''
```

---
### Handling received reports
```python
[...]
@app.route('/submit_report', methods=['POST'])
@authentication.login_required
def handle_report_submission():
    app_user = authentication.current_user()
    _log.info(f'Handling mission report submission from user "{app_user}"')

[...]
```

---
### Validating request data
```python
[...]
_log.debug('Checking content type of received request')
if request.headers.get('Content-Type').lower().lower() != 'application/json; charset=utf-8':
    _log.warning(f'User "{app_user}" tried submitting a report with an invalid content type')
    return 'Invalid content type!', 400
    
_log.debug('Trying to parse request body data as JSON')
request_data = request.json
_log.debug('Parsed request data: ' + repr(request_data))

_log.debug('Performing very rudimental validation of received report data structure')
if not isinstance(request_data, dict):
    _log.warning(f'User "{app_user}" submitted report that was not parsable as a dictionary')
    return 'Invalid report format!', 400 

[...]
```

_(Check that the submitted report matches expected format)_

---
### Storing report data in PostgreSQL
```python
[...]
_log.info('Storing received report in PostgreSQL database')
s = request_data

try:
    with postgresql_client.cursor() as cursor:
        _log.debug('Inserting data in "missions" table"')
        cursor.execute(
            'INSERT INTO missions ('
            '    submission_datetime, start_datetime, end_datetime,'
            '    code_name, budget, cost, location_latitude, location_longitude,'
            '    report_author, report'
            ') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id', (
                time.ctime(), s['start_datetime'], s['end_datetime'], s['code_name'],
                s['budget'], s['cost'], s['location']['lat'], s['location']['lon'],
                app_user, s['report']))
        
        mission_id = cursor.fetchone()[0]
        _log.debug(f'Submitted mission report ID in database: #{mission_id}')

[...]
```

---
### Storing report data in PostgreSQL
```python
[...]
        for name in s['participants']:
            _log.debug(f'Inserting participant "{name}" for mission #{mission_id} in DB')
            cursor.execute(
                'INSERT INTO participants (mission_id, name) VALUES (%s, %s)',
                (mission_id, name))

        for name in s['used_gadgets']:
            _log.debug(f'Inserting used gadget "{name}" for mission #{mission_id} in DB')
            cursor.execute(
                'INSERT INTO used_gadgets (mission_id, name) VALUES (%s, %s)',
                (mission_id, name))
                
        _log.debug('Commiting database changes')
        postgresql_client.commit()
[...]
```

---
### Migrating report storage to OpenSearch
```python
[...]
_log.info('Storing received report in OpenSearch')

document_data = request_data
document_data['submission_datetime'] = time.ctime()

try:
    opensearch_client.index(index='missions', body=document_data)

[...]
```

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Scott McCallum (CC BY-SA 2.0)" -->
## Lab tasks summarized
1. ~~Start/test lab environment~~
2. ~~Migrate from PostgreSQL to OpenSearch~~
3. Develop query to filter/sort reports
4. Query/Visualize data from reports in specific geographic region

![bg right:30%](images/16-turtle.jpg)

---
![bg center 75%](images/16-opensearch_01.png)

---
![bg center 75%](images/16-opensearch_02.png)

---
![bg center 75%](images/16-opensearch_03.png)

---
![bg center 75%](images/16-opensearch_04.png)

---
![bg center 75%](images/16-opensearch_05.png)

---
![bg center 75%](images/16-opensearch_06.png)

---
![bg center 75%](images/16-opensearch_07.png)

---
![bg center 75%](images/16-opensearch_08.png)

---
![bg center 75%](images/16-opensearch_09.png)

---
![bg center 75%](images/16-opensearch_10.png)

---
![bg center 75%](images/16-opensearch_11.png)

---
![bg center 75%](images/16-opensearch_12.png)

---
![bg center 75%](images/16-opensearch_13.png)

---
![bg center 75%](images/16-opensearch_14.png)

---
![bg center 75%](images/16-opensearch_15.png)

---
![bg center 75%](images/16-opensearch_16.png)

---
![bg center 75%](images/16-opensearch_17.png)

---
![bg center 75%](images/16-opensearch_18.png)

---
![bg center 75%](images/16-opensearch_19.png)

---
![bg center 75%](images/16-opensearch_20.png)

---
![bg center 75%](images/16-opensearch_21.png)

---
![bg center 75%](images/16-opensearch_22.png)

---
```json
GET missions/_search
{
  "query": {
    "terms": {
      "used_gadgets.keyword": [
        "Holographic projector"
      ]
    }
  }
}
```

---
## Query requirements from README
- Must have ended within the last year
- Must include the agent "Monster Hands" _or_ "Duchess" as participant
- Should include the agent "Gilles de Rais" as participant
- Should have a mission cost above 6000 USD
- Should include the term "expense" in report text

---
![bg center 75%](images/16-opensearch_23.png)

---
```json
GET missions/_search
{
  "query": {
    "bool": {
      "must": [
        {"range": {
          "end_datetime": {"gte": "now-1y"}}
        },
        {"terms": {
          "participants.keyword": ["Duchess", "Monster Hands"]}
        }
      ],
      "should": [
        {"terms": {
          "participants.keyword": ["Gilles de Rais"]}
        },
        {"range": {
          "cost": {"gt": 6000}}
        },
        {"match": {
          "report": {"query": "expense"}}
        }
      ]
    }
  }
}
```

---
```json
{
  "query": {
    "bool": {
      "must": [
        {"range": {
          "end_datetime": {"gte": "now-1y"}}
        },
        {"terms": {
          "participants.keyword": ["Duchess", "Monster Hands"]}
        }
      ],

[...]
```

---
```json
[...]
      "should": [
        {"terms": {
          "participants.keyword": ["Gilles de Rais"]}
        },
        {"range": {
          "cost": {"gt": 6000}}
        },
        {"match": {
          "report": {"query": "expense"}}
        }
      ]

[...]
```

---
![bg center 75%](images/16-opensearch_24.png)

---
![bg center 75%](images/16-opensearch_25.png)

---
```json
[...]
  "filter": [
    {"script": {
      "script": { 
        "lang": "painless",
        "source": "doc['cost'].value > doc['budget'].value"}
      }
    }
  ]
[...]
```

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Scott McCallum (CC BY-SA 2.0)" -->
## Lab tasks summarized
1. ~~Start/test lab environment~~
2. ~~Migrate from PostgreSQL to OpenSearch~~
3. ~~Develop query to filter/sort reports~~
4. Query/Visualize data from reports in specific geographic region

![bg right:30%](images/16-turtle.jpg)

---
![bg center 75%](images/16-opensearch_26.png)

---
![bg center 75%](images/16-opensearch_27.png)

---
![bg center 75%](images/16-opensearch_28.png)

---
![bg center 75%](images/16-opensearch_29.png)

---
![bg center 75%](images/16-opensearch_30.png)

---
![bg center 75%](images/16-opensearch_31.png)

---
![bg center 75%](images/16-opensearch_32.png)

---
![bg center 75%](images/16-opensearch_33.png)

---
![bg center 75%](images/16-opensearch_34.png)

---
![bg center 75%](images/16-opensearch_35.png)

---
![bg center 75%](images/16-opensearch_36.png)

---
![bg center 75%](images/16-opensearch_37.png)

---
![bg center 75%](images/16-opensearch_38.png)

---
![bg center 75%](images/16-opensearch_39.png)

---
![bg center 75%](images/16-opensearch_40.png)

---
![bg center 75%](images/16-opensearch_41.png)

---
![bg center 75%](images/16-opensearch_42.png)

---
![bg center 75%](images/16-opensearch_43.png)

---
![bg center 75%](images/16-opensearch_44.png)

---
![bg center 75%](images/16-opensearch_45.png)

---
![bg center 75%](images/16-opensearch_46.png)

---
![bg center 75%](images/16-opensearch_47.png)

---
![bg center 75%](images/16-opensearch_48.png)

---
![bg center 75%](images/16-opensearch_49.png)

---
![bg center 75%](images/16-opensearch_50.png)

---
![bg center 75%](images/16-opensearch_51.png)

---
![bg center 75%](images/16-opensearch_52.png)

---
![bg center 75%](images/16-opensearch_53.png)

---
![bg center 75%](images/16-opensearch_54.png)

---
![bg center 75%](images/16-opensearch_55.png)

---
![bg center 75%](images/16-opensearch_56.png)

---
![bg center 75%](images/16-opensearch_57.png)

---
![bg center 75%](images/16-opensearch_58.png)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Scott McCallum (CC BY-SA 2.0)" -->
## Lab tasks summarized
1. ~~Start/test lab environment~~
2. ~~Migrate from PostgreSQL to OpenSearch~~
3. ~~Develop query to filter/sort reports~~
4. ~~Query/Visualize data from reports in specific geographic region~~

![bg right:30%](images/16-turtle.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC0 1.0)" -->
## Remaining challenges
Restricting privileges for
the app's OpenSearch user.   
  
Data migration script from
PostgreSQL to OpenSearch.  
  
(Modify the missions app
to query/display reports
from OpenSearch.)

![bg right:30%](images/16-forest_log.jpg)
