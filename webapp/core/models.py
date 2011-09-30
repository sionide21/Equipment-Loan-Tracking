from django.db import models
from django.forms import ModelForm


class Item(models.Model):
    '''
    An item that TSO can loan out.
    '''
    description = models.TextField(blank=False)


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
    returned_to = models.CharField(max_length=30, verbose_name="Returned to")
    item = models.ForeignKey(Item, blank=False)

    def __unicode__(self):
        return self.id


class LoanForm(ModelForm):
    class Meta:
        model = Loan
        exclude = ('item', 'return_datetime', 'returned_to',)


class ItemForm(ModelForm):
    class Meta:
        model = Item
