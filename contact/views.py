import logging

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from contact.forms import ContactForm
from django.template import RequestContext, Context
from django.core.mail import send_mail, BadHeaderError
from django.core.urlresolvers import reverse


def contactview(request):
        message = request.POST.get('message', '')
        from_email = request.POST.get('email', '')
        name = request.POST.get('name', '')

        if message and from_email:
                try:
                    logging.info('Sending email from %s (%s), message: %s', name, from_email, message)
                    send_mail('Webova zprava', message, from_email, ['info@edesia.cz'])
                except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                return HttpResponseRedirect(reverse('contact_thankyou'))
        else:
            return render_to_response('contact/contact.html', {'form': ContactForm()},
                    context_instance=RequestContext(request))
    
        return render_to_response('contact/contact.html', {'form': ContactForm()},
            context_instance=RequestContext(request))

def thankyou(request):
        return render_to_response('contact/thankyou.html',
                context_instance=RequestContext(request))

