from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RiskPrediction(Base):
    """Modèle pour stocker les prédictions de risque"""
    __tablename__ = 'risk_predictions'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(String(255), nullable=False)
    
    # Scores de risque
    framingham_score = Column(Float)
    ascvd_10year_risk = Column(Float)
    
    # Classification
    risk_category = Column(String(20))  # low, moderate, high
    
    # Facteurs de risque
    risk_factors = Column(JSON)
    
    # Recommandations
    recommendations = Column(JSON)
    
    # Métadonnées
    prediction_date = Column(DateTime, default=datetime.utcnow)
    model_version = Column(String(20), default='1.0')
    
    def __repr__(self):
        return f"<RiskPrediction(patient_id={self.patient_id}, risk={self.risk_category})>"
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'patient_id': self.patient_id,
            'framingham_score': self.framingham_score,
            'ascvd_10year_risk': self.ascvd_10year_risk,
            'risk_category': self.risk_category,
            'risk_factors': self.risk_factors,
            'recommendations': self.recommendations,
            'prediction_date': self.prediction_date.isoformat() if self.prediction_date else None,
            'model_version': self.model_version
        }
 
