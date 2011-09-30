from django.db import models
from django.forms import ModelForm


class Loan(models.Model):
    '''
    Represents an item loaned to an individual.
    '''
    # An example of how to define fields, will be removed once real fields are
    # added
    sample_field = models.CharField(max_length=100, verbose_name="Foo")
    contact_field = models.EmailField(verbose_name="Contact Email")
    notes_field = models.TextField(verbose_name = "Notes")

    def __unicode__(self):
        return self.sample_field


class LoanForm(ModelForm):
    class Meta:
        model = Loan
