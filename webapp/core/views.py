from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from core.models import Loan, LoanForm, ItemForm


def index(request):
    '''The homepage'''
    return render_to_response('core/index.html')


@login_required
def secure_page(request):
    '''
    An example of a page that forces login.
    '''
    username = request.user.username
    return render_to_response('core/secure.html', {'username': username})


@login_required
def add_loan(request):
    loan_form = LoanForm()
    item_form = ItemForm()
    if request.method == 'POST':
        item_form = ItemForm(request.POST)
        if item_form.is_valid():
            item = item_form.save()
            loan_form = LoanForm(request.POST)
            if loan_form.is_valid():
                loan = loan_form.save(commit=False)
                loan.item = item
                loan.save()
                return HttpResponseRedirect(reverse('view_loan', args=(loan.id,)))

    return render_to_response('core/loan/add.html',
                              {'loan_form': loan_form,
                               'item_form': item_form},
                              context_instance=RequestContext(request))


@login_required
def view_loan(request, loan_id):
    '''View a specific loan in the system'''
    loan = get_object_or_404(Loan, id=loan_id)
    return render_to_response('core/loan/view.html', {'loan': loan})
