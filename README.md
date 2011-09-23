Equipment Loan Tracker
======================

## Setup

Below are the basic setups steps. Please be sure to update this as you make changes to setup needs.

### Making CAS Work

In order to make CAS cooperate, you will need to point a gatech subdomain to localhost. Add something like the following to your `/etc/hosts` file:

    127.0.0.1 dev.gatech.edu

Now, instead of developing at `http://localhost:8000`, use `http://dev.gatech.edu:8000`.

### Required Packages

To run the basic dev environment you will need:

* Python 2.6 (or 2.7)
* Django 1.3
* sqlite3
* python-pip
* pep8 (hint: `pip install pep8`)

### Running the Dev Server

The first time you run the dev server, you will need to sync the database. 
From the project root, type:

    python manage.py syncdb

To run the server, simply type:

    python manage.py runserver

Now you can access the site at `http://localhost:8000`. See [Django Docs](https://docs.djangoproject.com/en/1.3/ref/django-admin/) for more details.

### Before Committing

Before you commit, make sure that your code passes pep8.
From your project root, run:

    pep8 core/**.py

## Contributers

* Ben Olive
* Craig Campbell
* Jacob Robertson
* Matthew McCawley
