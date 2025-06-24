class RqbitClientError(Exception):
    """Base exception for the rqbit client."""


class RqbitHTTPError(RqbitClientError):
    """Raised when an HTTP request fails."""

    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
