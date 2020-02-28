#!/bin/bash

if [[ $MIGRATE = true ]] ; then
  ./utils/deploy/manage.sh makemigrations users swipe chat report
  ./utils/deploy/manage.sh migrate
fi
