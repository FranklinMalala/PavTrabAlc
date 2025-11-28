"""
Dieta Controller Module
Contains the controller for diet operations.
"""

from app import db
from app.models.dieta import Dieta
from app.validators.validators import DietaValidator, ValidationError


class DietaController:
    """
    Controller for Dieta (Diet) model.
    Handles business logic and validation for diet operations.
    
    Demonstrates:
        - Encapsulation of business logic
        - Use of conditions and loops
        - Error handling
    """
    
    def __init__(self):
        """Constructor for DietaController."""
        self._validator = DietaValidator()
    
    def create(self, data):
        """
        Create a new diet.
        
        Args:
            data: Dictionary with diet data
            
        Returns:
            tuple: (Dieta instance, error message or None)
        """
        try:
            # Validate data
            self._validator.validate(data)
            
            # Create diet instance
            dieta = Dieta(
                meta=data.get('meta'),
                descricao=data.get('descricao')
            )
            
            # Save to database
            dieta.save()
            
            return dieta, None
            
        except ValidationError as e:
            return None, e.message
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    def get_all(self):
        """
        Get all diets.
        
        Returns:
            list: List of diet dictionaries
        """
        dietas = Dieta.get_all()
        return [d.to_dict() for d in dietas]
    
    def get_by_id(self, id):
        """
        Get a diet by ID.
        
        Args:
            id: Diet ID
            
        Returns:
            tuple: (Dieta dictionary or None, error message or None)
        """
        dieta = Dieta.get_by_id(id)
        if not dieta:
            return None, f'Dieta com ID {id} não encontrada'
        return dieta.to_dict(include_relations=True), None
    
    def update(self, id, data):
        """
        Update a diet.
        
        Args:
            id: Diet ID
            data: Dictionary with updated data
            
        Returns:
            tuple: (Dieta dictionary or None, error message or None)
        """
        try:
            # Get existing diet
            dieta = Dieta.get_by_id(id)
            if not dieta:
                return None, f'Dieta com ID {id} não encontrada'
            
            # Validate data (only validate fields that are present)
            if 'meta' in data:
                self._validator.validate_not_empty(data['meta'], 'meta')
            
            # Update fields using loop
            allowed_fields = ['meta', 'descricao']
            update_data = {}
            for field in allowed_fields:
                if field in data:
                    update_data[field] = data[field]
            
            # Apply updates
            dieta.update(**update_data)
            
            return dieta.to_dict(), None
            
        except ValidationError as e:
            return None, e.message
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    def delete(self, id):
        """
        Delete a diet.
        
        Args:
            id: Diet ID
            
        Returns:
            tuple: (success boolean, error message or None)
        """
        try:
            dieta = Dieta.get_by_id(id)
            if not dieta:
                return False, f'Dieta com ID {id} não encontrada'
            
            dieta.delete()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def add_refeicao(self, dieta_id, refeicao_id):
        """
        Associate an existing meal with a diet.
        
        Args:
            dieta_id: Diet ID
            refeicao_id: Meal ID
            
        Returns:
            tuple: (success boolean, error message or None)
        """
        try:
            # Get diet
            dieta = Dieta.get_by_id(dieta_id)
            if not dieta:
                return False, f'Dieta com ID {dieta_id} não encontrada'
            
            # Validate and get meal
            refeicao = self._validator.validate_refeicao_exists(refeicao_id, db.session)
            
            # Associate meal with diet
            refeicao.dieta_id = dieta_id
            db.session.commit()
            
            return True, None
            
        except ValidationError as e:
            return False, e.message
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def add_exercicio(self, dieta_id, exercicio_id):
        """
        Associate an existing exercise with a diet.
        
        Args:
            dieta_id: Diet ID
            exercicio_id: Exercise ID
            
        Returns:
            tuple: (success boolean, error message or None)
        """
        try:
            # Get diet
            dieta = Dieta.get_by_id(dieta_id)
            if not dieta:
                return False, f'Dieta com ID {dieta_id} não encontrada'
            
            # Validate and get exercise
            exercicio = self._validator.validate_exercicio_exists(exercicio_id, db.session)
            
            # Associate exercise with diet
            exercicio.dieta_id = dieta_id
            db.session.commit()
            
            return True, None
            
        except ValidationError as e:
            return False, e.message
        except Exception as e:
            db.session.rollback()
            return False, str(e)
