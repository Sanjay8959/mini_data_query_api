#!/usr/bin/env python
# Simple server entry point for Render

import os

# Import the Flask application
from app import create_app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    # Run the app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
