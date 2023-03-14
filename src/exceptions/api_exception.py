class APIException(BaseException):

    def __init__(self, error_code, description=None, status_code=500):
        self.error_code = error_code
        self.description = description
        self.status_code = status_code

    def __str__(self):
        return f"ApiException(error_code={self.error_code}, " \
               f"description={self.description}, " \
               f"status_code={self.status_code})"
