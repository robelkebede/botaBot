#!/usr/bin/env bash
set -eu
echo "Starting MONGOD and Telegram_bot ...."
mongod & python new_server.py
