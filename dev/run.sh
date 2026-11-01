unset DATABASE_URL
export LOG_LEVEL=trace
export DEVELOPMENT=True
export FLASK_ENV=development
export FLASK_APP=app:app
flask database init
flask db upgrade
flask run --debug --reload
