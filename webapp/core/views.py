from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from core.models import Loan, LoanForm


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
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/secure')
    else:
        form = LoanForm()
    return render_to_response('core/addloan.html',
                              {'form': form, },
                              context_instance=RequestContext(request))


def view_loan(request, loan_id):
    '''View a specific loan in the system'''
    loan = get_object_or_404(Loan, id=loan_id)
    return render_to_response('core/loan/view.html', {'loan': loan})
