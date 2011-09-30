from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from core.models import Loan, LoanForm, Item, ItemForm


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
        try:
            item = Item.objects.get(serial_number=request.POST.get('serial_number'))
            item_form = ItemForm(request.POST, instance=item)
        except Item.DoesNotExist:
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
<<<<<<< HEAD
    return render_to_response('core/loan/view.html', {'loan': loan})


@login_required
def item_description(request):
    if 'serial' not in request.REQUEST:
        raise Http404
    serial = request.REQUEST['serial']
    item = get_object_or_404(Item, serial_number=serial)
    return HttpResponse(item.description)
=======
    return render_to_response('core/loan/view.html',
                              {'loan': loan},
                              context_instance=RequestContext(request))


@login_required
def return_loan(request, loan_id):
    ''' Mark a specific loan as returned'''
    from datetime import datetime
    loan = get_object_or_404(Loan, id=loan_id)
    if request.method == 'POST':
        loan.return_datetime = datetime.now()
        loan.save()
        return HttpResponseRedirect(reverse('view_loan', args=(loan_id,)))
    else:
        raise Http404
>>>>>>> fdffa519a512d273b215e1d85d7f43a19ae42dd8
