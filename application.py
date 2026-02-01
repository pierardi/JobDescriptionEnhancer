"""
WSGI entry point for Elastic Beanstalk and production deployment.
Imports the Flask app from the backend package.
"""

from backend.app import create_app

# Create application instance for production
application = create_app('production')

if __name__ == '__main__':
    application.run()
