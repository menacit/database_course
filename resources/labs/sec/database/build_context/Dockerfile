# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Security lab - Docker file for PostgreSQL with PGAudit extension

FROM docker.io/library/postgres:16.2-bookworm

# Extended standard Postgres Docker image with "PGAudit" extension for detailed query logging
RUN apt-get update \
		&& apt-get install -y --no-install-recommends postgresql-${PG_MAJOR}-pgaudit \
		&& rm -rf /var/lib/apt-get/lists/* \
    && apt-get autoremove -y \
		&& echo "shared_preload_libraries='pgaudit'" >> /usr/share/postgresql/postgresql.conf.sample