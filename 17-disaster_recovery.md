---
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0

title: "Database course: Disaster recovery"
author: "Joel Rangsmo <joel@menacit.se>"
footer: "© Course authors (CC BY-SA 4.0)"
description: "Introduction to disaster recovery of databases"
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
<!-- _footer: "%ATTRIBUTION_PREFIX% Ninara (CC BY 2.0)" -->
# Disaster recovery
### Handling backups and restoration

![bg right:30%](images/17-ahmedabad.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Ninara (CC BY 2.0)" -->
When disaster strikes,
you wanna be able to recover your data.  

Neither RAID nor clustering are backups.

![bg right:30%](images/17-ahmedabad.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Eric Savage (CC BY-SA 2.0)" -->
## Full backup
All data is copied and stored
in backup archive.

## Incremental backup
Only data that has been modified
since previous backup is copied
and stored in backup archive.

![bg right:30%](images/17-malachite.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Jonathan Torres (CC BY 4.0)" -->
One does not simply copy files from disk.  

Data may live in off-disk cache or be
changed in the middle of a backup.  

![bg right:30%](images/17-dragon_fighter.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Fredrik Rubensson (CC BY-SA 2.0)" -->
Tools like "mysqldump" and "pg\_dump"
can be utilized to safely backup databases.

![bg right:30%](images/17-barbwire.jpg)
