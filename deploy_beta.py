#not sure how to run admin commands from python, running them using command line
import sys
import paramiko

from subprocess import call, Popen, PIPE
from datetime import datetime
from getpass import getpass

settingsArgument = '--settings=settings.web4ce'

""" TODO uncomment
print 'Running syncdb...'
call(['python', 'manage.py', 'syncdb', settingsArgument])

print 'Running migrations...'
call(['python', 'manage.py', 'migrate', settingsArgument])

filename = datetime.now().strftime('%Y%m%d_%H%M.json')
print 'Running backup of data files. Saving to file %s...' % filename
#call(['python', 'manage.py', 'dumpdata', settingsArgument, '--exclude=contenttypes', '>', filename])
#backup_data = call(['python', 'manage.py', 'dumpdata', settingsArgument, '--exclude=contenttypes'])
backup_data = Popen(['python', 'manage.py', 'dumpdata', settingsArgument, '--exclude=contenttypes'], stdout=PIPE).communicate()[0]
#print len(backup_data)
backup_file = open(filename, 'w')
backup_file.write(backup_data)
backup_file.close()
"""


#TODO copy data to server - needs paramiko
print 'Copying deployment files to beta deployment...'
print 'Please enter FTP password:'
#password = sys.stdin.readline()
password = getpass()
username = 'edesia_cz'
url = 'sftp.edesia.cz'
port = 22

ftp_directory = '/public_html/beta/'
#http://stackoverflow.com/questions/432385/sftp-in-python-platform-independent
transport = paramiko.Transport((url, port))
transport.connect(username = username, password = password)

#TODO finish
sftp = paramiko.SFTPClient.from_transport(transport)
sftp.rmdir(ftp_directory)
