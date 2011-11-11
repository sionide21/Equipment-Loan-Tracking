from django.forms.models import modelformset_factory
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response as render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from core.models import Loan, LoanForm, Item, ItemForm, Person, PersonForm, Comment, CommentForm


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
    loans = Loan.objects.filter(date_returned__isnull=True)
    return render_to_response(request, 'core/current.html', {'loans': loans})


@login_required
def find_person(request):
    qs = None
    if request.method == 'POST':
        terms = request.POST['q']
        query = Q(gtid=terms)
        for field in ['name', 'email']:
            # case insensitive contains for each of the above fields
            field_query = '%s__icontains' % field
            query |= Q(**{field_query: terms})
        qs = Person.objects.filter(query)

    return render_to_response(request, 'core/loan/person.html',
                              {'results': qs})


@login_required
def add_person(request):
    person_form = PersonForm()
    if request.method == 'POST':
        person_form = PersonForm(request.POST)
    if person_form.is_valid():
        person = person_form.save()
        return render_to_response(request, 'core/person/select.html',
                                  {'person': person})

    return render_to_response(request, 'core/person/add.html',
                            {'person_form': person_form})


def handle_modify_loan(request, loan=None):
    '''Takes care of saving OR updating a loan'''
    if loan:
        loan_form = LoanForm(instance=loan)
        item_form = ItemForm(instance=loan.item)
        loaned_to = loan.loaned_to
    else:
        loan_form = LoanForm()
        item_form = ItemForm()
        loaned_to = None

    if request.method == 'POST':
        loan_form = LoanForm(request.POST, instance=loan)
        loaned_to = loan_form.fields['loaned_to'].to_python(request.POST['loaned_to'])

        try:
            item = Item.objects.get(serial_number__iexact=request.POST.get('serial_number'))
            item_form = ItemForm(request.POST, instance=item)
        except Item.DoesNotExist:
            item_form = ItemForm(request.POST)
        if item_form.is_valid():
            item = item_form.save()
            if loan_form.is_valid():
                loan = loan_form.save(commit=False)
                loan.item = item
                loan.save()
                return HttpResponseRedirect(reverse('view_loan', args=(loan.id,)))
    ctx = {
        'loaned_to': loaned_to,
        'loan_form': loan_form,
        'item_form': item_form,
        'add': loan == None
    }
    return render_to_response(request, 'core/loan/add_edit.html', ctx)


@login_required
def edit_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    if loan.date_returned:
        # Don't edit returned loans
        return HttpResponseRedirect(reverse('view_loan', args=(loan.id,)))
    return handle_modify_loan(request, loan)


@login_required
def add_loan(request):
    return handle_modify_loan(request)


@login_required
def view_loan(request, loan_id):
    '''View a specific loan in the system'''
    loan = get_object_or_404(Loan, id=loan_id)
    comment_form = CommentForm()
    comments = loan.comment_set.order_by('date')
    return render_to_response(request, 'core/loan/view.html',
                              {'loan': loan, 'comment_form': comment_form, 'comments': comments},
                              context_instance=RequestContext(request))


@login_required
def view_person(request, person_id):
    person = get_object_or_404(Person, gtid=person_id)
    person_form = PersonForm(instance=person)
    if request.method == 'POST':
        person_form = PersonForm(request.POST, instance=person)
        if person_form.is_valid():
            person = person_form.save()
            loans = Loan.objects.filter(date_returned__isnull=True)
            return render_to_response(request, 'core/current.html', {'loans': loans})
    return render_to_response(request, 'core/person/edit.html',
                              {'person_form': person_form},
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
        loan.date_returned = datetime.now()
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
