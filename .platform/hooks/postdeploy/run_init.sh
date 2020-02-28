#!/bin/bash

which pipenv
echo $PWD
./utils/deploy/00_init.sh
pipenv --venv
