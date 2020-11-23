class ApiException(Exception):

    def __init__(self, message, status_code=400):
        super(ApiException, self).__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {'message': self.message}
