import time
import logging
import os
import urllib
from os import stat, path
from multiprocessing import Lock

from django.utils import simplejson
from settings.common import PROJECT_PATH

from django.conf import settings


def flags(request):
    """
    Flags processor - returns various flags that may change the default behaviour of system.
    """
    #TODO load the flags from database/cache. Different for admin/registered/not registered
    flags = {}
    flags['showAds'] = not request.user.is_authenticated()
    
    if request.user.is_authenticated():
        if request.user.is_staff:
            flags['user'] = 'admin'
        else:
            flags['user'] = 'auth'
    else:
        flags['user'] = 'noauth'



    return {'flags': flags }


lock = Lock()

def ads_ranky_cz(request):

    if request.user.is_authenticated():
        return {'ads_ranky_cz': [] }

    cache_file = settings.ADS_CACHE_FILE

    #TODO lock object - handle multithreading
    if path.exists(cache_file):
        created = stat(cache_file).st_ctime
        #if the cached file is older than a few hours, delete it
        if time.time() - created > settings.MAX_ADS_CACHE_TIME:
            logging.info('Removing ads.ranky.cz cache file because it expired...')
            os.remove(cache_file)

    if not path.exists(cache_file):
        lock.acquire()
        try:
            if not path.exists(cache_file):
                logging.info('ads.ranky.cz cache file does not exist - downloading anew...')
                urllib.urlretrieve(settings.ADS_URL, cache_file)
        except IOError, e:
            logging.error('Error loading advertisement', e)
        finally:
            lock.release()

    if path.exists(cache_file):
        f = open(cache_file)
        ads = simplejson.loads(f.read())
        f.close()
    else:
        ads = {}


    return {'ads_ranky_cz': ads }
