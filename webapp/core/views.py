from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response as render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from core.models import Loan, LoanForm, Item, ItemForm, Comment, CommentForm


def render_to_response(req, *args, **kwargs):
    '''Ensure we always use a RequestContext as our context'''
    kwargs['context_instance'] = RequestContext(req)
    return render(*args, **kwargs)


def index(request):
    '''The homepage, show a login page or redirect to current'''
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('current_loans'))
    return render_to_response(request, 'core/index.html')


@login_required
def current_loans(request):
    username = request.user.username
    return render_to_response(request, 'core/current.html', {'username': username})


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

    return render_to_response(request, 'core/loan/add.html',
                              {'loan_form': loan_form,
                               'item_form': item_form})


@login_required
def view_loan(request, loan_id):
    '''View a specific loan in the system'''
    loan = get_object_or_404(Loan, id=loan_id)
    comment_form = CommentForm()
    comments = loan.comment_set.order_by('-date')
    return render_to_response(request, 'core/loan/view.html',
                              {'loan': loan, 'comment_form': comment_form, 'comments': comments},
                              context_instance=RequestContext(request))


@login_required
def item_description(request):
    if 'serial' not in request.REQUEST:
        raise Http404
    serial = request.REQUEST['serial']
    item = get_object_or_404(Item, serial_number__iexact=serial)
    return HttpResponse(item.description)


@login_required
def return_loan(request, loan_id):
    ''' Mark a specific loan as returned'''
    from datetime import datetime
    loan = get_object_or_404(Loan, id=loan_id)
    if request.method == 'POST':
        loan.return_datetime = datetime.now()
        loan.returned_to = request.user
        loan.save()
        return HttpResponseRedirect(reverse('view_loan', args=(loan_id,)))
    else:
        raise Http404


@login_required
def comment_loan(request, loan_id):
    '''Comment on a loan'''
    from datetime import datetime
    loan = get_object_or_404(Loan, id=loan_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.loan = loan
            comment.save()
        return HttpResponseRedirect(reverse('view_loan', args=(loan.id,)))
    else:
        raise Http404
