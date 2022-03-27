CarWager applicaation
====

About
-----

CarWager applicaation.
Auto realization and auction.


Author: Artem Sheibak <sheibakaa@gmail.com>


Requirements:

    Python 3.8, PostgreSql, Docker, Docker-compose, Django, DjangoRQ.


## Setup development environment  

1. Install virtualenv and PostgreSQL

        $ sudo apt install virtualenv
        $ sudo apt install -y postgresql postgresql-contrib
        $ sudo pg_ctlcluster 12 main start
        $ sudo apt install -y libpq-dev python3-dev

2. Install, create and activate virtualenv

        $ pip install virtualenv  
        $ virtualenv -p python3.8 --prompt=carwager- venv/
        $ source venv/bin/activate  

3. Clone sources and install pip packages
  
        $ git clone git@github.com:weibak/carwager.git && cd carwager/
        $ pip install -r requirements.txt

4. Run migration and local dev server

        $ python manage.py migrate
        $ python manage.py runserver

