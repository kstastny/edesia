
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
