class DateFormatNotValidException(Exception):

    def __init__(self):
        super().__init__('Format of date is not correct.')

class TimeFormatNotValidException(Exception):

    def __init__(self):
        super().__init__('Time format is not correct.')


class FeatureNotAvailableException(Exception):

    def __init__(self, *args):
        message = args[0]
        super().__init__(message or 'This feature is still not available.')


class CantBookVariablePricing(FeatureNotAvailableException):

    def __init__(self):
        super().__init__('Can\'t yet book with variable pricing timings.')


class CantBookFacility(FeatureNotAvailableException):

    def __init__(self):
        super().__init__('Can\'t book the facility for given timings.')
