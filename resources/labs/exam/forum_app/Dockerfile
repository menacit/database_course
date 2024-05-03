# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Examination lab - Dockerfile for "forum" web application

FROM docker.io/library/python:3.12.3-bookworm
WORKDIR /usr/src/app

COPY python_dependencies.txt ./
RUN pip install --no-cache-dir --requirement python_dependencies.txt

ADD static ./static
COPY health_check.py server.py ./

CMD ["/usr/local/bin/flask", "--app", "/usr/src/app/server.py", "run", "--host", "0.0.0.0"]
HEALTHCHECK --interval=15s --timeout=3s --retries=3 CMD ["/usr/local/bin/python", "healh_check.py"]
