class NoItemsException(BaseException):
    def __init__(self, message="The Youtube API returned 0 result items from the request"):
        self.message = message
        super().__init__(self.message)