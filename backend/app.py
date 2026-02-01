"""
Flask Application Factory and Initialization.

This module creates and configures the Flask application with all blueprints,
error handlers, and database initialization.
"""

import logging
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .config import config
from .models import db
from .interview_routes import interview_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """
    Application factory function.
    
    Args:
        config_name: Configuration to use ('development', 'testing', 'production')
                     Defaults to FLASK_ENV environment variable or 'development'
    
    Returns:
        Flask application instance
    """
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    logger.info(f"Creating Flask app with configuration: {config_name}")
    
    # Enable CORS for frontend (Amplify)
    # Allow all origins in production, or specify your Amplify domain
    cors_origins = os.getenv('CORS_ORIGINS', '*')
    if cors_origins == '*':
        CORS(app)  # Allow all origins
    else:
        CORS(app, resources={
            r"/api/*": {
                "origins": cors_origins.split(','),
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "X-User-ID", "X-User-Role"]
            },
            r"/health": {
                "origins": cors_origins.split(',')
            }
        })
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(interview_bp)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    # Create database context
    with app.app_context():
        db.create_all()
        logger.info("Database initialized")
    
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'environment': config_name
        }), 200
    
    @app.route('/api/version', methods=['GET'])
    def version():
        """API version endpoint."""
        return jsonify({
            'name': 'TechScreen Interview Generation API',
            'version': '1.0.0',
            'environment': config_name
        }), 200
    
    logger.info(f"Flask app created successfully for {config_name}")
    
    return app


if __name__ == '__main__':
    # For development only - run from backend folder: python -m backend.app
    # Or use root app.py which runs the backend
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
