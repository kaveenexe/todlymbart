from flask import Flask
from routes import api_routes
from utils.errors import APIError, handle_api_error, handle_general_error
# Initialize Flask app
app = Flask(__name__)

# Register routes
app.register_blueprint(api_routes)

# Register error handlers for custom and general errors
app.register_error_handler(APIError, handle_api_error)
app.register_error_handler(Exception, handle_general_error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
