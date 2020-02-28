#!/bin/bash

# import env variables if not set
if [[ ! $RDS_HOSTNAME ]] ; then
  sudo sh -c 'cat /opt/elasticbeanstalk/deployment/env > .env'
fi

pipenv run python jumboSmash/manage.py "$@"

EXIT_CODE=$?
if [ $EXIT_CODE ] ; then
  echo
  echo "+-------------------------------------------------------+"
  echo "|                                                       |"
  echo "| MAKE SURE TO RUN 00_init TO INSTALL VIRTUAL ENV FIRST |"
  echo "|                                                       |"
  echo "+-------------------------------------------------------+"
  exit $EXIT_CODE
fi
