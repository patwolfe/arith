#!/bin/bash

# get virtual env folder
cd /var/app/venv
DIR=""

for D in `find . -mindepth 1 -maxdepth 1 -type d`
do
    DIR=$D
done

# activate virtual env
source $DIR/bin/activate

# run collect static in staging
cd /var/app/staging/jumboSmash
python manage.py collectstatic
