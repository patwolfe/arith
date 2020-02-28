#!/bin/bash

# import env variables if not set
if [[ ! $RDS_HOSTNAME ]] ; then
  sudo sh -c 'cat /opt/elasticbeanstalk/deployment/env > .env'
fi

pipenv run python jumboSmash/manage.py "$@"

exit 0










if [[ $1 = '--usage' ]] ; then
  echo "Use this script to run manage.py in django app"
  echo "$ manage.sh runserver"
  exit 0
fi

# ensure command is run in project root for virtual env
if [[ $PWD = /var/app/current ]] ; then
  echo "Executing manage command at root of current app"
else
  echo "MUST BE IN ROOT OF CURRENT APP (/var/app/current)"
  exit 1
fi

# import env variables if not set
if [[ ! $RDS_HOSTNAME ]] ; then
  sudo sh -c 'cat /opt/elasticbeanstalk/deployment/env > .env'
fi

# run commands in virtual env
cd jumboSmash
pipenv install --skip-lock
pipenv run python manage.py $1
