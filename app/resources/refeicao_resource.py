"""
Refeicao Resource Module
Contains Flask-RESTful resources for meal API endpoints.
"""

from flask import request
from flask_restful import Resource
from app.controllers.refeicao_controller import RefeicaoController


class RefeicaoListResource(Resource):
    """
    Resource for meal collection endpoints.
    
    Endpoints:
        - GET /api/refeicoes - List all meals
        - POST /api/refeicoes - Create a new meal
    """
    
    def __init__(self):
        """Constructor for RefeicaoListResource."""
        self._controller = RefeicaoController()
    
    def get(self):
        """
        List all meals.
        
        Query params:
            - dieta_id: Filter by diet ID (optional)
        
        Returns:
            tuple: (list of meals, HTTP status code)
        """
        dieta_id = request.args.get('dieta_id', type=int)
        
        if dieta_id:
            refeicoes = self._controller.get_by_dieta(dieta_id)
        else:
            refeicoes = self._controller.get_all()
        
        return {'data': refeicoes, 'count': len(refeicoes)}, 200
    
    def post(self):
        """
        Create a new meal.
        
        Request body:
            {
                "tipo_refeicao": "string (required)",
                "quantidade": "integer (required)",
                "alimentos": ["string array (required)"],
                "dieta_id": "integer (optional)"
            }
            
        Returns:
            tuple: (created meal or error, HTTP status code)
        """
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados não fornecidos'}, 400
        
        refeicao, error = self._controller.create(data)
        
        if error:
            return {'error': error}, 400
        
        return {'data': refeicao.to_dict(), 'message': 'Refeição criada com sucesso'}, 201


class RefeicaoResource(Resource):
    """
    Resource for single meal endpoints.
    
    Endpoints:
        - GET /api/refeicoes/<id> - Get a specific meal
        - PUT /api/refeicoes/<id> - Update a meal
        - DELETE /api/refeicoes/<id> - Delete a meal
    """
    
    def __init__(self):
        """Constructor for RefeicaoResource."""
        self._controller = RefeicaoController()
    
    def get(self, id):
        """
        Get a specific meal by ID.
        
        Args:
            id: Meal ID
            
        Returns:
            tuple: (meal data or error, HTTP status code)
        """
        refeicao, error = self._controller.get_by_id(id)
        
        if error:
            return {'error': error}, 404
        
        return {'data': refeicao}, 200
    
    def put(self, id):
        """
        Update a meal.
        
        Args:
            id: Meal ID
            
        Request body:
            {
                "tipo_refeicao": "string (optional)",
                "quantidade": "integer (optional)",
                "alimentos": ["string array (optional)"],
                "dieta_id": "integer (optional)"
            }
            
        Returns:
            tuple: (updated meal or error, HTTP status code)
        """
        data = request.get_json()
        
        if not data:
            return {'error': 'Dados não fornecidos'}, 400
        
        refeicao, error = self._controller.update(id, data)
        
        if error:
            if 'não encontrada' in error:
                return {'error': error}, 404
            return {'error': error}, 400
        
        return {'data': refeicao, 'message': 'Refeição atualizada com sucesso'}, 200
    
    def delete(self, id):
        """
        Delete a meal.
        
        Args:
            id: Meal ID
            
        Returns:
            tuple: (success message or error, HTTP status code)
        """
        success, error = self._controller.delete(id)
        
        if not success:
            if 'não encontrada' in error:
                return {'error': error}, 404
            return {'error': error}, 400
        
        return {'message': 'Refeição excluída com sucesso'}, 200
