class UrbanError(Exception):
    pass


class TooManyRequests(UrbanError):
    pass


class TermNotFound(UrbanError):
    pass
