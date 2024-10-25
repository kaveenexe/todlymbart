from flask import jsonify

class APIError(Exception):
    """Custom exception class for handling API errors with messages and status codes."""
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

def handle_api_error(error):
    """Handles API errors and returns JSON response."""
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response

def handle_general_error(error):
    """Handles general errors and returns a standardized JSON response."""
    response = jsonify({"error": "An unexpected error occurred. Please try again later."})
    response.status_code = 500
    return response
