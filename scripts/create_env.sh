#!/usr/bin/env bash

set -euo pipefail

touch .env

echo "MYSQL_USER=" | cat >> .env
echo "MYSQL_PASSWORD=" | cat >> .env
echo "MYSQL_HOST=" | cat >> .env
echo "MYSQL_PORT=" | cat >> .env
echo "MYSQL_DATABASE_NAME=" | cat >> .env