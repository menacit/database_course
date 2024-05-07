# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Docker file for Pony ORM demo application
FROM docker.io/library/python:3.11.9-bookworm
WORKDIR /usr/src/app

RUN pip install --no-cache-dir pony==0.7.17

COPY demo.py ./

CMD ["python", "demo.py"]
