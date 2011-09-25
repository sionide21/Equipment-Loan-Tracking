from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


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
