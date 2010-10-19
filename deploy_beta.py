#not sure how to run admin commands from python, running them using command line
import sys
import os
#import paramiko
import shutil

from subprocess import call, Popen, PIPE
from datetime import datetime
from getpass import getpass
from os import path
from os.path import join

#http://stackoverflow.com/questions/2584414/python-windows-file-copy-with-wildcard-supporthtaccess
def copy_files(src_glob, dst_folder):
    for fname in iglob(src_glob):
        copy(fname, join(dst_folder, fname))


settingsArgument = '--settings=settings.web4ce'

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

print 'Preparing distribution package...'
DIST_DIRECTORY = '_dist'
#remove the directory if it exists
if os.access(DIST_DIRECTORY, os.F_OK):
    shutil.rmtree(DIST_DIRECTORY)


os.mkdir(DIST_DIRECTORY)
os.mkdir(join(DIST_DIRECTORY, 'logs')) #the log directory is not automatically created

shutil.copy(join('deployment', '.htaccess'), DIST_DIRECTORY)
shutil.copy(join('deployment', 'django.wsgi.production'), join(DIST_DIRECTORY, 'django.wsgi'))
shutil.copy(join('deployment', 'google0d1d58e1af972248.html'), DIST_DIRECTORY) #google validation
shutil.copy(join('deployment', 'robots.txt'), DIST_DIRECTORY)
shutil.copy(join('deployment', 'favicon.ico'), DIST_DIRECTORY)

deploy_dir = join(DIST_DIRECTORY, 'edesia')
os.mkdir(deploy_dir)

print 'Copying application files...'
shutil.copy(join('deployment', '__init__.py'), deploy_dir)
shutil.copy('urls.py', deploy_dir)
shutil.copy('manage.py', deploy_dir)

shutil.copytree('comments', join(deploy_dir, 'comments'))
shutil.copytree('contact', join(deploy_dir, 'contact'))
shutil.copytree('core', join(deploy_dir, 'core'))
shutil.copytree('djangoratings', join(deploy_dir, 'djangoratings'))
shutil.copytree('south', join(deploy_dir, 'south'))
shutil.copytree('users', join(deploy_dir, 'users'))
shutil.copytree('statistics', join(deploy_dir, 'statistics'))

print 'Copying media files and templates...'
shutil.copytree('templates', join(deploy_dir, 'templates'))
shutil.copytree('site_media', join(deploy_dir, 'site_media'))

#copy settings correctly - web4ce
print 'Copying settings files...'
settings_dir = join(deploy_dir, 'settings')
os.mkdir(settings_dir)
shutil.copy(join('settings', '__init__.py'), settings_dir)
shutil.copy(join('settings', 'common.py'), settings_dir)
shutil.copy(join(join('settings', 'web4ce'), 'custom.py'), settings_dir)





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
"""
