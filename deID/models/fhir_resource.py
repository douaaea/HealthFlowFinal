from sqlalchemy import Column, Integer, String, DateTime, Text
from database.connection import Base
from datetime import datetime

class FhirResource(Base):
    """Modèle pour la table fhir_resources"""
    __tablename__ = 'fhir_resources'
    
    id = Column(Integer, primary_key=True)
    fhir_id = Column(String(255), unique=True, nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_data = Column(Text, nullable=False)
    version_id = Column(String(50))
    last_updated = Column(DateTime)
    sync_date = Column(DateTime, default=datetime.utcnow)
    source_url = Column(String(500))
    
    def __repr__(self):
        return f"<FhirResource(id={self.id}, type={self.resource_type}, fhir_id={self.fhir_id})>"

class FhirResourceAnonymized(Base):
    """Modèle pour la table fhir_resources_anonymized"""
    __tablename__ = 'fhir_resources_anonymized'
    
    id = Column(Integer, primary_key=True)
    original_fhir_id = Column(String(255), unique=True, nullable=False)
    anonymized_fhir_id = Column(String(255), unique=True, nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_data = Column(Text, nullable=False)
    anonymization_date = Column(DateTime, default=datetime.utcnow)
    anonymization_method = Column(String(100), default='faker_pseudonymization')
    
    def __repr__(self):
        return f"<FhirResourceAnonymized(id={self.id}, type={self.resource_type})>"
