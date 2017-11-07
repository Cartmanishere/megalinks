#!/bin/bash
NAME="Megalinks"
DJANGODIR=/var/www/html/megalinks/
SOCKFILE=/var/www/html/megalinks/mediashare/gunicorn.sock
USER=ubuntu
GROUP=ubuntu
NUM_WORKERS=5
DJANGO_SETTINGS_MODULE=mediashare.settings
DJANGO_WSGI_MODULE=mediashare.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/ubuntu/python3/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/ubuntu/python3/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
