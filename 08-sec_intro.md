---
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0

title: "Database course: Security introduction"
author: "Joel Rangsmo <joel@menacit.se>"
footer: "© Course authors (CC BY-SA 4.0)"
description: "Introduction to security considerations for databases"
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
<!-- _footer: "%ATTRIBUTION_PREFIX% Christian Siedler (CC BY-SA 2.0)" -->
# Database security
### Basics, access control and logging

![bg right:30%](images/08-locks.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Christian Siedler (CC BY-SA 2.0)" -->
Databases are used to store/process
humanity's most precious information.  

Wouldn't it make sense that we try
to keep 'em secure?

![bg right:30%](images/08-locks.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC BY 2.0)" -->
Before we dig into the details of
securing databases, let's have a look at
common considerations for secure systems!

![bg right:30%](images/08-abandoned_chimney.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC BY 2.0)" -->
## The basics of system security
- Minimizing attack surface
- Protecting network communication
- Requiring trustworthy authentication
- Enforcing "principle of least privilege"
- Monitoring security-sensitive activity

![bg right:30%](images/08-abandoned_chimney.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC BY 2.0)" -->
## Why do we log?
- Detection of malicious activity
- Deterrence of bad behavior
- Review and optimization
- Legal/Compliance requirements

![bg right:30%](images/08-birch_forest.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC BY 2.0)" -->
**What makes a good log entry/event?**

![bg right:30%](images/08-birch_forest.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC BY 2.0)" -->
## Operational logs
Enables us to understand what is
happening in a system.

![bg right:30%](images/08-abandoned_factory.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% A Loves DC (CC BY 2.0)" -->
## Audit logs
Enables us to "reenact" events of interest.

![bg right:30%](images/08-steel_w.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% A Loves DC (CC BY 2.0)" -->
**W**hen,  
**W**ho,  
**W**hat, 
**W**here and possibly  
**W**hy?

![bg right:30%](images/08-steel_w.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Freed eXplorer (CC BY 2.0)" -->
**How do these "basics"
apply to databases?**

![bg right:30%](images/08-cave.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Marcin Wichary (CC BY 2.0)" -->
## Minimizing attack surface
Your good old firewall rules!  

Avoid running/exposing
auxiliary services on the database host.  

Don't forget underlying human and
infrastructure dependencies.

![bg right:30%](images/08-radar.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Rising Damp (CC BY 2.0)" -->
## Protecting network communication
The confidentiality of your password
and queries/response is of
uttermost importance.  

Most DBMS support protection of
network traffic using **TLS**.  

Also protects the integrity
of communication!

![bg right:30%](images/08-phone_pole.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Brendan J (CC BY 2.0)" -->
## Requiring trustworthy authentication
Users (unfortunately including DBAs)
have a tendency to choose/reuse
weak passwords.  

Mutual TLS is a safer option
(AKA "client certificate authentication").  

DBMS may support key storage on a
**h**ardware **s**ecurity **m**odule,
further minimizing the risk of leakage.

![bg right:30%](images/08-rusty_key.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Fredrik Rubensson (CC BY-SA 2.0)" -->
### Enforcing "principle of least privilege"
Avoid shared users between applications.  
  
Most DBMS support restricting ("granting")
access to specific tables.  

Some support "column-level" restrictions,
often implemented using "views".  

Others provide "row-level security",
if you wanna get real fancy!

![bg right:30%](images/08-razor_wire.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC0 1.0)" -->
### Monitoring security-sensitive activity
A DBMS typically provide several
"log channels", some of which
are quite interesting from a
security perspective.  

General categories:
- Server operation logs
- Connection logs
- Error logs
- (Slow) query logs
- Dedicated audit logs

![bg right:30%](images/08-forest_log.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Nicholas A. Tonelli (CC0 1.0)" -->
### Monitoring security-sensitive activity
What is important to log?

It depends on your
risk appetite and budget!  

Some DBMS support logging only
queries target specific tables
of interest (with help from plugins).  

![bg right:30%](images/08-forest_log.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Greg Lloy (CC BY 2.0)" -->
## Wrapping up
All DBMS are (unfortunately)
different beasts.  

How you implement these
security restrictions will depend
on the database software chosen.  

Hope you have a foundation to
stand on for further self-studies.

![bg right:30%](images/08-retro_computer.jpg)
