---
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0

title: "Database course: Introduction"
author: "Joel Rangsmo <joel@menacit.se>"
footer: "© Course authors (CC BY-SA 4.0)"
description: "Introduction to database course"
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
<!-- _footer: "%ATTRIBUTION_PREFIX% Dennis van Zuijlekom (CC BY-SA 2.0)" -->
# Database course
### Welcome and thanks for joining!

![bg right:30%](images/00-core_memory.jpg)

<!--
Welcome participants and wait for everyone to get settled.
-->

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Kristina Hoeppner (CC BY-SA 2.0)" -->
## \$ whoami
Extroverted nerd who enjoys security,
devops and most humans.  

\>10 years in the salt mines of IT.  

Been doing system admin/automation,
software development and lots of
security/penetration testing.  
  
Happily teaching since 2022.

![bg right:30%](images/00-llama.jpg)

<!--
Introduction of the lecturers and their background.
-->

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Steve Jurvetson (CC BY 2.0)" -->
In my spare time, I particularly enjoy
playing with computers, eating strange things,
nerding out on modern history (~1850-2000)
and live music/festivals.

![bg right:30%](images/00-pyramid.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% RoboticSpider (CC BY 4.0)" -->
**Thanks in advance for
your patience with me!**

![bg right:30%](images/00-please_robot.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Jason Thibault (CC BY 2.0)" -->
## Grandiose mission statement
Help you gain the knowledge required to
design, build, secure and maintain databases.

![bg right:30%](images/00-palais_des_congres.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Thierry Ehrmann (CC BY 2.0)" -->
## Breaking it down
- Choosing the right DBMS for the job
- Structuring/Grouping data properly
- Implementing auth**N**, auth**Z** and logging
- Improving performance/availability
- Handling disasters

![bg right:30%](images/00-man_thinking.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Martin Fisch (CC BY 2.0)" -->
**We'll revisit topics, if needed!**

![bg right:30%](images/00-seal.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Qubodup (CC BY 2.0)" -->
## Requires basic knowledge of...
- Python
- OS and application management
- Networking
- The Linux shell
- Docker and Docker Compose

![bg right:30%](images/00-glitch_globe.jpg)

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Meddygarnet (CC BY 2.0)" -->
## How we will do it
- Lectures (\~45 + \~15) and Q&A
- (Group) presentations
- Focused/Rolling labs
- Continuous reflection
- Non-graded quizzes
- Open-hours

![bg right:30%](images/00-soldering_robot.jpg)

<!--
- We'll cover lots of things in a short amount of time

- In order to be able to do this we'll use scientifically proven methods to Make It Stick

- Basically what the slide says

- Don't forget to have fun!

- If available, show detailed course schedule
-->

---
For detailed notes, glossary, labs and similar, see:   
**[%RESOURCES_DOMAIN%/db.zip](%RESOURCES_ARCHIVE%)**.  
  
These resources should be seen
as a complement to an
instructor-lead course,
not a replacement.

![bg right 90%](qr_codes/presentation_zip.link.svg)

<!--
- There are several resources to help you learn

- Speaker notes in slides are heavily recommended for recaps/deep diving

- May also be available through LMS, depending on how the course is consumed

- The course is designed to be instructor lead, won't make the most of it on your own, see as aid

- Presentations may be recorded
-->

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Helsinki Hacklab (CC BY 2.0)" -->
## Acknowledgements
Thanks to [Chas Academy](https://chasacademy.se/) and [Särimner](https://www.sarimner.com/)
for enabling development of the course.
  
Hats off to all FOSS developers and
free culture contributors making it possible.

![bg right:30%](images/00-umbrellas.jpg)

<!--
The course wouldn't be available if it wasn't for financial support - Thanks!
-->

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Martin Fisch (CC BY 2.0)" -->
## Free as in beer and speech
Is anything unclear?  
Got ideas for improvements?  
Don't fancy the animals in the slides?  
  
Create an issue or submit a pull request to
[the repository on Github](https://github.com/menacit/database_course)!

![bg right:30%](images/00-bees.jpg)

<!--
- Encourage participants to make the course better

- Learners are likely the best to provide critique, lecturers are likely a bit home-blind

- No cats or dogs allowed!

- Feel free to share it with friends or use it yourself later in your career
-->

---
<!-- _footer: "%ATTRIBUTION_PREFIX% Rod Waddington (CC BY-SA 2.0)" -->
**Let us get to work!**

![bg right:30%](images/00-green_cabling.jpg)
