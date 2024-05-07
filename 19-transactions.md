---
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0

title: "Database course: Database transactions"
author: "Joel Rangsmo <joel@menacit.se>"
footer: "© Course authors (CC BY-SA 4.0)"
description: "Introduction to transactions in database course"
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
<!-- _footer: "%ATTRIBUTION_PREFIX% Halfrain (CC BY-SA 2.0)" -->
# Database transactions
### Ensuring data consistency

![bg right:30%](images/19-vintage_machine.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Halfrain (CC BY-SA 2.0)" -->
Imagine that you're running a bank.  

Customers can transfer money
between accounts. Basic stuff!  

Customer **14** wants to transfer
**42** funny-money to
customer **919**.

![bg right:30%](images/19-vintage_machine.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Halfrain (CC BY-SA 2.0)" -->
## Any potential problems?
```sql
SELECT balance
FROM bank_accounts
WHERE customer_id = 14
```

```sql
UPDATE bank_accounts
SET balance -= 42
WHERE customer_id = 14
```

```sql
UPDATE bank_accounts
SET balance += 42
WHERE customer_id = 919
```

![bg right:30%](images/19-vintage_machine.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Andrew Hart (CC BY-SA 2.0)" -->
What happens if the DBMS crashes
between the two UPDATEs?

What happens if a customer
performs hundres of transfers
at the \~exact same time?

![bg right:30%](images/19-broken_glass.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Rod Waddington (CC BY-SA 2.0)" -->
## Introducing transactions
Ability to group together multiple
SQL statements in a "single unit of work".  

If one of the statment fails to execute,
the previous ones are rolled back.  

Enables locking of tables and rows
to prevent interference/race conditions.

Starts with `BEGIN`, ends with `COMMIT`.  

![bg right:30%](images/19-lemur.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Yellowcloud (CC BY 2.0)" -->
```sql
BEGIN;

SELECT balance
FROM bank_accounts
WHERE customer_id = 14
FOR UPDATE;

-- Do something resonable if
-- balance is insufficient!

UPDATE bank_accounts
SET balance -= 42
WHERE customer_id = 14;

UPDATE bank_accounts
SET balance += 42
WHERE customer_id = 919;

COMMIT;
```

![bg right:30%](images/19-nixie_tube.jpg)

<!--
Bitcoin 24 woes (comment #9 / 3):
https://stackoverflow.com/questions/15026825/php-mysql-how-to-prevent-two-requests-update
-->
