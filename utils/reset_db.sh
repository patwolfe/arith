#!/bin/bash

find . -name migrations -type d -exec rm -rf {} \;
rm db.sqlite3
./manage.py migrate --run-syncdb
