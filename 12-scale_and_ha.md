---
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0

title: "Database course: Scaling and high-availability"
author: "Joel Rangsmo <joel@menacit.se>"
footer: "© Course authors (CC BY-SA 4.0)"
description: "Introduction to scaling and high-availability for databases"
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
<!-- _footer: "%ATTRIBUTION_PREFIX% Austin Design (CC BY-SA 2.0)" -->
# Scaling / High-availability
### A somewhat gentle introduction

![bg right:30%](images/12-crystal_wave.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Austin Design (CC BY-SA 2.0)" -->
Congratulations -
your business is truly booming!  

That database server is starting
to sweat quite a bit. Setting up
indexes and tweaking queries
doesn't seem to be enough.
Have you outgrown it?

What if it breaks?  
How would that affect you?

![bg right:30%](images/12-crystal_wave.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% George N (CC BY 2.0)" -->
How can we scale our DB to
handle more workload _and/or_ be
highly-available if shit hits the fan?

![bg right:30%](images/12-laser.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% OLCF at ORNL (CC BY 2.0)" -->
### Vertical scaling
Add/Remove computing resources like
CPU, RAM and disk to handle more/less workload.  

In the physical context, change or replace
underlying hardware. When using virtualization,
it's a few clicks away.  

Also known as "scaling up".

![bg right:30%](images/12-server_macro.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Thierry Ehrmann (CC BY 2.0)" -->
### Horizontal scaling
Spin up/down multiple servers and
distribute the workload among them.  
  
Also known as "scaling out".

![bg right:30%](images/12-server_rack.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Scott Merrill (CC BY-SA 2.0)" -->
**Wait a second -
what do we mean by "workload"?**

![bg right:30%](images/12-pipes.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Scott Merrill (CC BY-SA 2.0)" -->
The things the database server
is required/suppose to do.

How long are you willing to
wait for a query to complete?
Translated to **latency** in applications.  

How much information must you store?
Affects disk space requirements.

![bg right:30%](images/12-pipes.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Scott Merrill (CC BY-SA 2.0)" -->
Is your workload mainly
compute-intensive or storage-intensive?  

Are you sifting through large amounts of data
or performing complex calculations/filtering?

![bg right:30%](images/12-pipes.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Fredrik Rubensson (CC BY-SA 2.0)" -->
## Vertical scaling
Increasing number of CPU cores may
enable more concurrent queries.
Faster CPU cores can decrease latency.  

Storage throughput and latency tends
to be the main performance bottleneck.  

Spinning rust (traditional hard drive)
is cheap, but incredibly slow compared
to RAM or even SSDs.

Caching, storage tiers and technologies
like RAID will likely help.

![bg right:30%](images/12-skyscraper_construction.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Fredrik Rubensson (CC BY-SA 2.0)" -->
At some point, you won't be able to
just buy a more expensive service.  

Horizontal scaling to the rescue!

![bg right:30%](images/12-skyscraper_construction.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% John K. Thorne (CC0 1.0)" -->
## Basic partitioning
Perhaps we can run a separate database server
per customer or table?  
  
Quite simple setup!  

Affects ability to query data across
customers/tables.  
  
Requires potentially complex capacity planning
and server management overhead.

![bg right:30%](images/12-dome_collage.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Sbmeaper1 (CC0 1.0)" -->
## Read replicas
Additional servers can be configured to
store/serve copies of data from
the primary database server
(AKA master/"source of truth").  

Increases read performance linearly.  
Acts as an online backup of data.

C~~R~~UD queries must be handled by
primary database server, limiting
scalability.

Doesn't increase available storage space.

![bg right:30%](images/12-building_reflection.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% USGS EROS (CC BY 2.0)" -->
**Data sharding is the answer.**

![bg right:30%](images/12-satellite_photo.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Pedro Mendes (CC BY-SA 2.0)" -->
## The tradeoffs
Synchronous or asynchronous replication.  

Do you prioritize performance or
consistency/data availability?  

Are you willing to handle the complexity?
How about the blast radius?

![bg right:30%](images/12-arecibo.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Thierry Ehrmann (CC BY 2.0)" -->
**Complex systems typically rely on
all methods described in combination.**

![bg right:30%](images/12-wheel.jpg)
