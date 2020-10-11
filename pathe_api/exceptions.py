class PatheApiException(Exception):
    """Custom error class for pathe-api"""
    def __init__(self, message="an exception occured"):
        self.message = message
        super().__init__(self.message)


# Error messages
REQUEST_FAILED = "API request gave bad response"
