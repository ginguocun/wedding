cd /opt/wedding  && source venv/bin/activate
git pull
python3 manage.py migrate
ps auxw | grep wedding_uwsgi
uwsgi --reload /opt/wedding/uwsgi/uwsgi.pid
