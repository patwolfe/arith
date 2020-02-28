#!/bin/bash

# import env variables if not set
if [[ ! $RDS_HOSTNAME ]] ; then
  sudo sh -c 'cat /opt/elasticbeanstalk/deployment/env > .env'
fi

if ! pipenv run python jumboSmash/manage.py "$@" ; then
  echo "+-------------------------------------------------------+"
  echo "|                                                       |"
  echo "| MAKE SURE TO RUN 00_init TO INSTALL VIRTUAL ENV FIRST |"
  echo "|                                                       |"
  echo "+-------------------------------------------------------+"
fi
