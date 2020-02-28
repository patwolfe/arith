#!/bin/bash

./utils/deploy/00_init.sh
PATH=$(pipenv --venv)
which mv
mv $PATH /home/ec2-user/.local/share/virtualenvs/ -p
