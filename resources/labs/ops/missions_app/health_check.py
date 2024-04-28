# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Operations lab - Health check script for missions app

try:
    import sys
    import requests

except Exception as error_message:
    raise Exception(f'Failed to import required Python dependencies: {error_message}')

# Performs a HTTP request against the default "health check" URL.
# If HTTP request succeedes, exit with return code 0. If not, exit with return code 1.
try:
    response = requests.get('http://127.0.0.1:5000/is_the_server_up_and_running')
    response.raise_for_status()

except:
    sys.exit(1)

sys.exit(0)
