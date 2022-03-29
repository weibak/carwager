release: python carwager/manage.py migrate
web: python carwager/manage.py runserver 0.0.0.0:$PORT
worker: python carwager/manage.py rqworker
scheduler: python carwager/manage.py rqscheduler