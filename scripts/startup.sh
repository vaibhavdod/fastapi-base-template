#! /usr/bin/env sh
set -e

# If there's a prestart.sh script in the /app directory or other path specified, run it before starting
PRE_START_PATH=/scripts/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    chmod +x "$PRE_START_PATH"
    echo "Running script $PRE_START_PATH"
    .$PRE_START_PATH
else 
    echo "There is no script $PRE_START_PATH"
fi

# Run migrations
alembic upgrade head

# Start the app
echo "Starting Application for Environment $APP_ENV"

HOST=${HOST:-0.0.0.0}
PORT=${APP_PORT:-80}
LOG_LEVEL=${LOG_LEVEL:-info}
APP_MODULE=${APP_MODULE:-"app.main:app"}

if [ "$APP_ENV" = "dev" ] ; then
    echo "Running Development Server"
    exec uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL $APP_MODULE
else 
    echo "Running Production Server"
    # We just remove the hot reload parameter
    exec uvicorn --host $HOST --port $PORT --log-level $LOG_LEVEL $APP_MODULE
fi