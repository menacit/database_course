# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Security lab - Dockerfile for web applications

FROM docker.io/library/python:3.12.3-bookworm
WORKDIR /usr/src/app

COPY shared_python_dependencies.txt ./
RUN pip install --no-cache-dir --requirement shared_python_dependencies.txt

ARG APP_NAME
COPY shared_utilities.py health_check.py base_template.html.jinja ${APP_NAME}/* ./

CMD ["/usr/local/bin/flask", "--app", "/usr/src/app/server.py", "run", "--host", "0.0.0.0"]
HEALTHCHECK --interval=15s --timeout=3s --retries=3 CMD ["/usr/local/bin/python", "health_check.py"]
