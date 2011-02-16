import logging
from cStringIO import StringIO
import sys


from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.management import call_command


#we have to execute commands on the server because MySQL is not remotely accessible
def execute_command(request, command):
    if not request.user.is_staff:
        return HttpResponse('<p>You have to be logged in as administrator to execute commands.</p>')

    #http://stackoverflow.com/questions/1218933/can-i-redirect-the-stdout-in-python-into-some-sort-of-string-buffer
    stdout = sys.stdout
    sys.stdout = f = StringIO()

    call_command(command)

    sys.stdout = stdout

    return HttpResponse('%s' % f.getvalue(), mimetype='text/plain')
