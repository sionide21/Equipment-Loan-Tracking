from django.db import models
from django.forms import ModelForm


class Loan(models.Model):
    '''
    Represents an item loaned to an individual.
    '''
    location_field = models.CharField(max_length=100, verbose_name="Location")

    def __unicode__(self):
        return self.id


class LoanForm(ModelForm):
    class Meta:
        model = Loan
