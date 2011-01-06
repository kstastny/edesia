
def flags(request):
    """
    Flags processor - returns various flags that may change the default behaviour of system.
    """
    #TODO load the flags from database/cache. Different for admin/registered/not registered
    if request.user.is_authenticated():
        return {'flags': {'showAds': False }}
    else:
        return {'flags': {'showAds': True }}
