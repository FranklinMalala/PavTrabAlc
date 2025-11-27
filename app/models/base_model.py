"""
Base Model Module
Contains the base model class with common functionality for all models.
Implements inheritance pattern for OOP requirements.
"""

from datetime import datetime
from app import db


class BaseModel(db.Model):
    """
    Abstract base model class.
    Provides common functionality for all models including:
    - ID field (primary key)
    - Created at timestamp
    - Common methods for serialization and CRUD operations
    
    This class demonstrates inheritance and encapsulation in OOP.
    """
    
    __abstract__ = True
    
    # Common fields for all models
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        """
        Constructor for base model.
        Initializes common attributes.
        
        Args:
            **kwargs: Keyword arguments for model attributes
        """
        super(BaseModel, self).__init__(**kwargs)
    
    def save(self):
        """
        Save the current model instance to the database.
        Encapsulates the database session operations.
        """
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """
        Delete the current model instance from the database.
        Encapsulates the database session operations.
        """
        db.session.delete(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """
        Update model attributes.
        
        Args:
            **kwargs: Attributes to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self
    
    def to_dict(self):
        """
        Convert model to dictionary.
        This method should be overridden by subclasses (polymorphism).
        
        Returns:
            dict: Dictionary representation of the model
        """
        created_at_str = None
        if self.created_at is not None:
            try:
                created_at_str = self.created_at.isoformat()
            except AttributeError:
                created_at_str = str(self.created_at)
        
        return {
            'id': self.id,
            'created_at': created_at_str
        }
    
    @classmethod
    def get_by_id(cls, id):
        """
        Get a model instance by ID.
        
        Args:
            id: Primary key value
            
        Returns:
            Model instance or None
        """
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """
        Get all instances of the model.
        
        Returns:
            List of model instances
        """
        return cls.query.all()
    
    def __repr__(self):
        """String representation of the model."""
        return f'<{self.__class__.__name__} id={self.id}>'
