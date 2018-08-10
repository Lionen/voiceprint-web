#!/bin/bash
nohup python manage.py runserver 192.168.99.54:5000 > logs/`date +%Y%m%d`.log 2>&1 &



