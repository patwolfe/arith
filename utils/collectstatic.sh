#!/bin/bash

cd /var/app/venv

for D in `find . -mindepth 1 -type d`
do
    echo D
done
