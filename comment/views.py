# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from comment.models import CommentForm
from django.template import RequestContext, Context
from django import forms
from django.forms.widgets import *
from django.core.mail import send_mail, BadHeaderError

def contactview(request):
    #csrf = RequestContext(request)
   # subject = csrf.POST.get('topic', '')
    subject = request.POST.get('topic')
    message = 'adew'
    from_email = 'amit@amit.com'
    #print csrf
    #subject = csrf('topic', '')
    #message = csrf.POST.get('message', '')
    #from_email = csrf.POST.get('email', '')

    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['change@this.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/comment/thankyou/')
    else:
        return render_to_response('comment/comments.html', {'form': CommentForm()})

    return render_to_response('comment/comments.html', {'form': CommentForm()}, RequestContext(request))

def thankyou(request):
    return render_to_response('comment/thankyou.html')
