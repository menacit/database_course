#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - NoSQL lab - Wrapper script for access to containerized jumpbox

# If no command-line arguments are provided, spawn a bash shell in container
if [[ -z "${1}" ]]; then
  docker compose exec jumpbox.int.agency.test /bin/bash

# If additional command-line arguments are provided, execute them in container
else
  docker compose exec jumpbox.int.agency.test ${*}

fi
