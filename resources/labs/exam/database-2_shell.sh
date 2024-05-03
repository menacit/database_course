#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Examination lab - Wrapper script for access to containerized SQL DB

BASE_COMMAND="docker compose exec --user postgres database-2.int.agency.test"

# If no command-line arguments are provided, spawn a bash shell in container
if [[ -z "${1}" ]]; then
  ${BASE_COMMAND} /bin/bash

# If additional command-line arguments are provided, execute them in container
else
  ${BASE_COMMAND} ${*}

fi
