# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Operations lab - Dockerfile for jumpbox container

FROM docker.io/library/postgres:16.2-bookworm

RUN apt-get update \
	&& apt-get install --assume-yes --no-install-recommends \
  bash-completion httpie curl python3-pip vim nano \
	&& rm -rf /var/lib/apt-get/lists/* \
	&& apt-get autoremove --assume-yes \
  && pip3 install --no-cache-dir --break-system-packages \
  opensearch-py==2.5.0 psycopg[binary]==3.1.18

WORKDIR /root
CMD ["/usr/bin/sleep", "infinity"]
