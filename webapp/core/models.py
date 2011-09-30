from django.db import models
from django.forms import ModelForm


class Loan(models.Model):
    '''
    Represents an item loaned to an individual.
    '''
    location_field = models.CharField(max_length=100, verbose_name="Location")
    contact_field = models.EmailField(verbose_name="Contact Email")
    notes_field = models.TextField(verbose_name="Notes")
    loan_datetime = models.DateTimeField(auto_now_add=True,
                                         verbose_name="Date Loaned")
    return_datetime = models.DateTimeField(null=True,
                                           verbose_name="Date Returned")

    def __unicode__(self):
        return self.id


class LoanForm(ModelForm):
    class Meta:
        model = Loan
        exclude = ('return_datetime',)
