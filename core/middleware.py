import logging

class ErrorMiddleware(object):
    """
    logs errors that happen during view calls
    """

    def process_exception(self, request, exception):
        try:
            logging.critical('Critical exception: %s', exception, exc_info=True)
        except:
            pass
