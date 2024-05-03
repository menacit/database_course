# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Examination lab - Dockerfile for jumpbox container

FROM docker.io/library/postgres:16.2-bookworm

RUN apt-get update \
	&& apt-get install --assume-yes --no-install-recommends \
  bash-completion httpie curl python3-requests python3-yaml vim nano jq \
	&& rm -rf /var/lib/apt-get/lists/* \
	&& apt-get autoremove --assume-yes

COPY forum_test_script.py /usr/local/bin/forum_test_script.py

WORKDIR /root
CMD ["/usr/bin/sleep", "infinity"]
