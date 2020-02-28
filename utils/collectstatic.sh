#!/bin/bash

# get virtual env folder
# cd /var/app/venv
# for D in `find . -mindepth 1 -maxdepth 1 -type d`
# do
#     DIR=$D
# done

# activate virtual env
# source $DIR/bin/activate
cd /var/app/staging
pipenv install --skip-lock

# run collect static in staging
cd /var/app/staging/jumboSmash
pipenv run python manage.py collectstatic

# run db migrate for sqlite
if [[ $RESETDB = true ]] ; then
  pipenv run python manage.py makemigrations users swipe chat report
  pipenv run python manage.py migrate
fi
