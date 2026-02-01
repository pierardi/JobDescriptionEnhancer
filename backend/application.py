"""
WSGI entry point for Elastic Beanstalk deployment (when running from backend folder).
"""

from .app import create_app

# Create application instance for production
application = create_app('production')

if __name__ == '__main__':
    application.run()
