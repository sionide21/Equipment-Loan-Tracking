#! /usr/bin/env python

'''
This program is intended to be run daily from a cron task.

It will send out reminder emails to anyone whose loan is due soon.

Configuration for how frequently an email is sent can be found in the settings.py file of the webapp.
'''
import sys
import os


def main():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'webapp')))
    os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'
    from core.models import ReminderTask
    from django.conf import settings

    for days in settings.DUE_REMINDER_DAYS:
        ReminderTask(days).send_reminders()


if __name__ == '__main__':
    main()
