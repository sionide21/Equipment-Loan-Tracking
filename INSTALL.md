Installation
============

## System Requirements

This app runs on a standard django stack. If you are familiar with django you can use any compatible web and db servers. For this readme, we will assume linux/apache/mysql

### Programs

* Python 2.6 (or 2.7)
* Apache with mod_wsgi
* MySQL

#### Optional but recommended

Though you can do without it, the python package manager `pip` will make setup easier.

### Python Libraries

You will need to install the following python libraries. If you have `pip` you can get all of these by running `pip install -r ./requirements.pip` from project root.

* Django 1.3.1
* MySQL-python 1.2.3
* django-cas 2.0.3

If you are having trouble installing MySQL-python from pip, it is available through your package manager (such as yum).


## Installation

We have included a file call `django.wsgi` that will let apache know about this project. Add the following lines to your apache config to use it.

We will assume that the project is in `/var/www/elt/` please update the code below to match the actual location.

    Alias /static "/var/www/elt/webapp/core/static"
    WSGIScriptAlias / /var/www/elt/webapp/django.wsgi


## Configuration

The primary config file for this project is `webapp/settings.py` when you are instructed to set variables below. They will be present in that file.

### Database Setup

The DATABASES dict in settings controls you connection to the database. Change the `default` database to look like below.

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<name of your database>',
        'USER': '<your database user>',
        'PASSWORD': '<that users password>',
        'HOST': '<database server>',
        'PORT': '',
    }

#### Initial DB Creation

Once you have the database options configured. You will run a django script to create the tables. 

    python webapp/manage.py syncdb

This will ask you to create an initial superuser for this system. This is important as this user will be allowed to grant access to others. 

The username _MUST_ be the users gt account, otherwise CAS will not recognize the user. Email and password are not used since we use CAS for authentication. Set them to whatever you like. 

### Adding Student Assistants

Once the webapp is running, you can add student assistants by logging in and clicking "User Admin" on the left. This option is only available to superuser (such as the one created above.)

### Adding superusers

Superuser management is not exposed in the webapp, you have to do it directly in the database. The easiest way to add a superuser is to add them as a regular user first (User Admin above).

After they have logged in once, there will be a user record for them in the database table `auth_user`. To make a user a superuser, simply set the `superuser` column to 1.

#### A note on superusers

Superusers can log into the system regardless of whether they are on the list in "User Admin".

### Email Reminders

#### Email Gateway

By default (for debugging purposes) we have configured the project to print emails out to the console instead of sending them. You will need to put the configuration for you email server in settings.

Comment out the following line to enable live email:

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

Information for configuring your mail server can be found at https://docs.djangoproject.com/en/dev/ref/settings/#email-backend

#### CRON

Email reminders are sent by a cron task. To setup, add a daily cron task to run `bin/send_reminder_emails.py`.

#### Email Reminder Frequency

By default, reminders are sent 7 days before due and again 2 days before due. This is configurable in settings.

The setting `DUE_REMINDER_DAYS` contains a list of the days to send reminders. They represent the number of days before a given item is due to send an email. An email will be sent once for each of the days in this list but never more than once per item per day.
