# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import get_current_site
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm
from .models import User
import tasks

def _registration_email_send(request, user):
    data = {
        'ACTIVATECODE' : user.verify_code,
        'SERVERIP' : get_current_site(request).domain
    }
    
    tasks.send_email.delay(
        _('Activation Email'),
        'registration/email.html',
        user.email,
        data)

def register(request):

    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()

        _registration_email_send(request, user)

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user);

        variables = RequestContext( request, {'user': form.instance})
        return render_to_response(
            'registration/register_success.html',
            variables
        )
    variables = RequestContext( request, {'form': form} )

    return render_to_response( 'registration/register.html', variables )

def register_verify(request, verify_code):

    user = get_object_or_404(User, verify_code=verify_code)

    if user.email_verified:
        raise Http404
    else:
        user.email_verified = True
        user.verify_code = None
        user.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user);

        variables = RequestContext( request, {
            'user': user,
        })
        return render_to_response(
            'registration/register_activate.html',
            variables
        )

@login_required
def login_check(request):
        variables = RequestContext( request, {
            'user': request.user,
        })
        return render_to_response(
            'registration/login_check.html',
            variables
        )
