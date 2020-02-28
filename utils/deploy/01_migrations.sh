#!/bin/bash

if [[ $MIGRATIONS = true ]] ; then
  ./utils/deploy/manage.sh makemigrations users swipe chat report
  ./utils/deploy/manage.sh migrate
fi

exit 0










# activate virtual env
pipenv install --skip-lock

# import env variables if not set
if [[ ! $RDS_HOSTNAME ]] ; then
  sudo sh -c 'cat /opt/elasticbeanstalk/deployment/env > .env'
fi

# run db migrate
cd jumboSmash
if [[ $RESETDB = true ]] ; then
  pipenv run python manage.py makemigrations users swipe chat report
  pipenv run python manage.py migrate
fi
