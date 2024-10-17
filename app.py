from flask import Flask
from routes import api_routes

# Initialize Flask app
app = Flask(__name__)

# Register routes
app.register_blueprint(api_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
