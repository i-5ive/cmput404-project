static: bash scripts/deploy.sh
release: python manage.py migrate --no-input
web: gunicorn core.wsgi
