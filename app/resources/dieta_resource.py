"""
Dieta Resource Module
Contains Flask-RESTful resources for diet API endpoints.
"""

from flask import request
from flask_restful import Resource
from app.controllers.dieta_controller import DietaController


class DietaListResource(Resource):
    """
    Resource for diet collection endpoints.
    
    Endpoints:
        - GET /api/dietas - List all diets
        - POST /api/dietas - Create a new diet
    """
    
    def __init__(self):
        """Constructor for DietaListResource."""
        self._controller = DietaController()
    
    def get(self):
        """
        List all diets.
        
        Returns:
            tuple: (list of diets, HTTP status code)
        """
        dietas = self._controller.get_all()
        return {'data': dietas, 'count': len(dietas)}, 200
    
    def post(self):
        """
        Create a new diet.
        
        Request body:
            {
                "meta": "string (required)",
                "descricao": "string (optional)"
            }
            
        Returns:
            tuple: (created diet or error, HTTP status code)
        """
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados não fornecidos'}, 400
        
        dieta, error = self._controller.create(data)
        
        if error:
            return {'error': error}, 400
        
        return {'data': dieta.to_dict(), 'message': 'Dieta criada com sucesso'}, 201


class DietaResource(Resource):
    """
    Resource for single diet endpoints.
    
    Endpoints:
        - GET /api/dietas/<id> - Get a specific diet
        - PUT /api/dietas/<id> - Update a diet
        - DELETE /api/dietas/<id> - Delete a diet
    """
    
    def __init__(self):
        """Constructor for DietaResource."""
        self._controller = DietaController()
    
    def get(self, id):
        """
        Get a specific diet by ID.
        
        Args:
            id: Diet ID
            
        Returns:
            tuple: (diet data or error, HTTP status code)
        """
        dieta, error = self._controller.get_by_id(id)
        
        if error:
            return {'error': error}, 404
        
        return {'data': dieta}, 200
    
    def put(self, id):
        """
        Update a diet.
        
        Args:
            id: Diet ID
            
        Request body:
            {
                "meta": "string (optional)",
                "descricao": "string (optional)"
            }
            
        Returns:
            tuple: (updated diet or error, HTTP status code)
        """
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados não fornecidos'}, 400
        
        dieta, error = self._controller.update(id, data)
        
        if error:
            if 'não encontrada' in error:
                return {'error': error}, 404
            return {'error': error}, 400
        
        return {'data': dieta, 'message': 'Dieta atualizada com sucesso'}, 200
    
    def delete(self, id):
        """
        Delete a diet.
        
        Args:
            id: Diet ID
            
        Returns:
            tuple: (success message or error, HTTP status code)
        """
        success, error = self._controller.delete(id)
        
        if not success:
            if 'não encontrada' in error:
                return {'error': error}, 404
            return {'error': error}, 400
        
        return {'message': 'Dieta excluída com sucesso'}, 200
