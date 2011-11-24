from django.db import models
from django.forms import ModelForm, ModelChoiceField, HiddenInput
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django import forms
from datetime import date, datetime, time, timedelta


def validate_past(value):
    from django.core.exceptions import ValidationError
    from datetime import datetime
    #Dont allow due dates to be in the past
    if value < datetime.now():
        raise ValidationError('Due Date must be in the future')


class Person(models.Model):
    '''
    A person capable of borrowing.
    '''
    gtid = models.CharField(max_length=9, blank=False, unique=True, verbose_name="GT ID")
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(blank=False)


class Item(models.Model):
    '''
    An item that TSO can loan out.
    '''
    serial_number = models.CharField(blank=True, null=True, max_length=255, unique=True)
    description = models.TextField(blank=False)

    def save(self, *args, **kwargs):
        '''Null out serial number if blank, make it all caps otherwise'''
        if not self.serial_number:
            self.serial_number = None
        else:
            self.serial_number = self.serial_number.upper()
        super(Item, self).save(*args, **kwargs)


class Loan(models.Model):
    '''
    Represents an item loaned to an individual.
    '''
    location = models.CharField(max_length=100)
    date_loaned = models.DateTimeField(auto_now_add=True)
    date_due = models.DateTimeField(validators=[validate_past])
    date_returned = models.DateTimeField(null=True)
    returned_to = models.ForeignKey(User, blank=True, null=True, related_name="accepted_returns")
    item = models.ForeignKey(Item, blank=False)
    loaned_by = models.ForeignKey(User, related_name="created_loans")
    loaned_to = models.ForeignKey(Person, blank=False)

    def __unicode__(self):
        return unicode(self.id)


class Comment(models.Model):
    '''
    A comment on a loan
    '''
    user = models.ForeignKey(User)
    loan = models.ForeignKey(Loan)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()


class EmailRecord(models.Model):
    '''
    A record that an email has been sent to a user.
    '''
    loan = models.ForeignKey(Loan, blank=False, related_name="emails")
    date = models.DateTimeField(blank=False, auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)


class ItemDueEmail(EmailMessage):
    '''
    An email about a loan being due shortly.
    '''
    def __init__(self, loan, send_desc="", **kwargs):
        self.loan = loan
        self.send_desc = send_desc
        kwargs['subject'] = "Equipment Due Reminder"
        template = get_template("item_due_email.txt")
        ctx = Context({'loan': loan})
        kwargs['body'] = template.render(ctx)
        kwargs['to'] = [loan.loaned_to.email] + list(kwargs.get('to', []))
        super(ItemDueEmail, self).__init__(**kwargs)

    def send(self, *args, **kwargs):
        super(ItemDueEmail, self).send(*args, **kwargs)
        EmailRecord(loan=self.loan, description=self.send_desc).save()


class ReminderTask:
    '''
    A task that finds any loans due soon and sends out a reminder.

    This will generally be run via a cron script.
    '''
    def __init__(self, remaining_time):
        self.remaining_time = remaining_time
        self.due_date = date.today() + timedelta(days=remaining_time)

    def send_reminders(self):
        loans = Loan.objects.filter(date_returned__isnull=True, date_due=self.due_date)
        today = [datetime.combine(date.today(), t) for t in (time.min, time.max)]
        for loan in loans:
            # Only send one email a day about a loan
            if not loan.emails.filter(date__range=today).exists():
                ItemDueEmail(loan, send_desc="%d day reminder." % self.remaining_time).send()


class DivFormMixin:
    '''
    Mix this into a django.forms.Form to enable a new output method 'as_div' that
    will output divs for use with blueprint.css
    '''
    def as_div(self):
        "Returns this form rendered as HTML <divs>s"
        return self._html_output(
            normal_row=u'<div class="span-13 last"><div class="span-3">%(label)s</div><div class="span-10 last">%(field)s</div>%(help_text)s</div>',
            error_row=u'<div class="error span-13 last">%s</div>',
            row_ender=u'</div>',
            help_text_html=u'<div class="quiet legend prepend-3 span-10 last">%s</div>',
            errors_on_separate_row=False)


class LoanForm(ModelForm, DivFormMixin):
    class Meta:
        model = Loan
        exclude = ('item', 'date_returned', 'returned_to', 'loaned_by',)
    loaned_to = ModelChoiceField(queryset=Person.objects, widget=HiddenInput)


class ItemForm(ModelForm, DivFormMixin):
    class Meta:
        model = Item


class PersonForm(ModelForm, DivFormMixin):
    class Meta:
        model = Person


class CommentForm(ModelForm, DivFormMixin):
    class Meta:
        model = Comment
        widgets = {
          'comment': forms.Textarea(attrs={'rows': 2, 'style': "width:720px"})
        }
        exclude = ('user', 'loan',)
