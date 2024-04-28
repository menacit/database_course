#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Operations lab - Script for submitting example mission reports

echo 'Submitting example reports from directory "example_reports"'

IFS=$'\n'
for REPORT_FILE in example_reports/*.json; do
  echo "Submitting example report from \"${REPORT_FILE}\""
  curl \
    --request POST --header 'Content-Type: application/json; charset=utf-8' \
    --data "@${REPORT_FILE}" http://malory:h3art_varma@127.0.0.1:10006/submit_report

  echo
  sleep 1s

done