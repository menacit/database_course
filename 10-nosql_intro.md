---
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0

title: "Database course: NoSQL introduction"
author: "Joel Rangsmo <joel@menacit.se>"
footer: "© Course authors (CC BY-SA 4.0)"
description: "Introduction to NoSQL databases"
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
<!-- _footer: "%ATTRIBUTION_PREFIX% Jason Thibault (CC BY 2.0)" -->
# "NoSQL" introduction
### Alternative databases/data stores

![bg right:30%](images/10-biosphere.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Jason Thibault (CC BY 2.0)" -->
SQL/relational databases have been around
since before the dark ages.  

Tables have pre-defined
columns and data is queried
using a _somewhat standardized_ language.  

Did we get everything right
for every use-case?

![bg right:30%](images/10-biosphere.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Pelle Sten (CC BY 2.0)" -->
## Common pain-points
Inflexible data modeling.  

Severe table/JOIN "inflation".  

Performance and scalability challenges.  

Unsuitable query language. 

![bg right:30%](images/10-rusty_silos.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Dennis van Zuijlekom (CC BY-SA 2.0)" -->
Many different approaches and options!  

Haphazardly grouped together under
the term "**N**ot **O**nly SQL".  

![bg right:30%](images/10-lego.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Rod Waddington (CC BY-SA 2.0)" -->
**Query language** VS **Storage method**

![bg right:30%](images/10-wrens.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Jan Hrdina (CC BY-SA 2.0)" -->
**Let's try breaking 'em down!**

![bg right:30%](images/10-optics.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Rod Waddington (CC BY-SA 2.0)" -->
## Some sub-categories
- Key-value stores
- Document databases
- (Wide) column-family stores
- Graph databases

![bg right:30%](images/10-singapore_street.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Wolfgang Stief (CC0 1.0)" -->
## Key-value stores
Provides simple storage of
**key-value pairs**.  

"foo=bar".  
"user\_1234\_session\_token=ef97b59c9b8e62".

Commonly used for distributed caching.

Very performant compared to
traditional relational databases.

**Redis/Valkey** and **etcd**
are popular options.

![bg right:30%](images/10-cooling_system.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC BY 2.0)" -->
## Document databases
A "document" is typically a
JSON-compatible data structure,
think a dictionary containing keys
of various types - like strings and lists.

**Collections** (\~tables) contain
**documents** (\~rows) which consist of several
**fields** (\~columns).

Typically doesn't require pre-defined
or consistent fields ("schema-less").

Provides great flexibility,
for good and bad.

![bg right:30%](images/10-birch_forest.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC BY 2.0)" -->
**_"Data that is accessed together
should be stored together"_**

![bg right:30%](images/10-birch_forest.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC BY 2.0)" -->
## Translating from SQL

<!-- https://www.upwork.com/mc/documents/RD-vs-NRD.png -->

![bg right:30%](images/10-birch_forest.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC BY 2.0)" -->
## MongoDB
Hu**mongo**us **d**ata**b**ase.  

Easy to use/manage, popular among startups.  

Queries can trigger server-side execution
of user-defined JavaScript code.  
  
License change in 2018 affecting adoption.  
  
Many public clouds provide
"MongoDB"-compatible database offerings.

![bg right:30%](images/10-birch_forest.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC BY 2.0)" -->
## Elasticsearch / OpenSearch
Document database heavily focusing on
data search/filtering capabilities.

Entries in query responses gets a "score".  
  
Field-mapping can be provided to "extend"
basic JSON data types, for example
geospatial coordinates.  

Very easy to scale!  

Became closed-source in 2021,
forked into "OpenSearch".  
  
Provides support for queries using SQL.

![bg right:30%](images/10-birch_forest.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Kurayba (CC BY-SA 2.0)" -->
## (Wide) column-family stores
Similar to traditional SQL databases,
but each row has its own "column definition".  

Much easier to horizontally scale
compared to DMBS' like MariaDB/PostgreSQL.

**Apache Cassandra** is typically
considered a wide column database.

![bg right:30%](images/10-snow_spheres.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Pelle Sten (CC BY 2.0)" -->
## Graph databases
Database consists of **nodes**
that have **properties** (KV pairs).  

Nodes may have **relationships** with
other nodes. Relationships may have
**labels** (KV pairs).  

Suitable for highly interconnected
data with deep/complex relationships.  
  
A popular example is **Neo4J**.

![bg right:30%](images/10-spheres.jpg)

<!-- https://images.contentstack.io/v3/assets/blt36c2e63521272fdc/blt1ca2179301629d11/60c14f85d475801b9d54ffae/22.JPG -->

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Scott Merrill (CC BY-SA 2.0)" -->
**What option should I choose?**  

![bg right:30%](images/10-pipes.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Scott Merrill (CC BY-SA 2.0)" -->
**It depends!™**

![bg right:30%](images/10-pipes.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Oklahoma National Guard (CC BY 2.0)" -->
## Important considerations
What type of data am I storing/querying?  
  
How much data do I need to store?  
  
How often do I need to read/write?  

What are my availability requirements?  
  
What ~~am I~~ are we comfortable with?

![bg right:30%](images/10-rappelling_worker.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Kuhnmi (CC BY 2.0)" -->
Hope this piqued your interest!  

We'll revisit these topics/technologies.

![bg right:30%](images/10-bird.jpg)
