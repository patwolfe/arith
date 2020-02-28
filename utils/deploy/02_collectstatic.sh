#!/bin/bash

./utils/deploy/manage.sh collectstatic

exit 0










# activate virtual env
pipenv install --skip-lock

# import env variables if not set
if [[ ! $RDS_HOSTNAME ]] ; then
  sudo sh -c 'cat /opt/elasticbeanstalk/deployment/env > .env'
fi

# run collect static
cd jumboSmash
pipenv run python manage.py collectstatic
