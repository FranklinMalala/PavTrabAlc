"""
Diet Management Application - Main Package
A complete diet management application with REST API and GUI.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()


def create_app(config_class=None):
    """
    Application factory function.
    Creates and configures the Flask application.
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_class:
        app.config.from_object(config_class)
    else:
        from app.config import Config
        app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Create API instance for this app
    api = Api(app)
    
    # Import and register resources
    from app.resources.dieta_resource import DietaResource, DietaListResource
    from app.resources.refeicao_resource import RefeicaoResource, RefeicaoListResource
    from app.resources.exercicio_resource import ExercicioResource, ExercicioListResource
    
    # Register endpoints
    api.add_resource(DietaListResource, '/api/dietas')
    api.add_resource(DietaResource, '/api/dietas/<int:id>')
    api.add_resource(RefeicaoListResource, '/api/refeicoes')
    api.add_resource(RefeicaoResource, '/api/refeicoes/<int:id>')
    api.add_resource(ExercicioListResource, '/api/exercicios')
    api.add_resource(ExercicioResource, '/api/exercicios/<int:id>')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
