#!/bin/sh
ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill