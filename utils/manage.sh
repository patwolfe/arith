#!/bin/bash

if [[ $1 = '--usage' ]] ; then
  echo "Use this script to run manage.py in django app"
  echo "$ manage.sh runserver"
  exit 0
fi

if [[ $PWD = /var/app/current ]] ; then
  echo "Executing manage command at root of current app"
else
  echo "MUST BE IN ROOT OF CURRENT APP (/var/app/current)"
  exit 1
fi

# activate virtual env
pipenv install --skip-lock

pipenv run jumboSmash/manage.py $1
