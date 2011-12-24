# Create your views here.
from django.shortcuts import render_to_response
from forms import ContactForm
from django.template import RequestContext
from django.core.context_processors import csrf

def contact(request):
    #c = {}
    #c.update(csrf(request))
    print "Amit "
    if request.method == 'POST':
        #csrf = RequestContext(request)
        #c = {}
        #c.update(csrf(request))
        topic = request.POST.get('topic')
        message = request.POST.get('message')
        sender = request.POST.get('sender', 'noreply@example.com')
        print topic, message, sender
        return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(initial={'sender': 'user@example.com'})
        return render_to_response('contacts/contact.html', {'form': form}, context_instance=RequestContext(request))

