from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PatientFeatureExtractor:
    """Extracteur de features démographiques des patients"""
    
    def __init__(self):
        pass
    
    def extract(self, patient_data):
        """Extrait les features d'un patient"""
        try:
            features = {}
            
            # Age
            if 'birthDate' in patient_data:
                birth_date = datetime.strptime(patient_data['birthDate'], '%Y-%m-%d')
                age = (datetime.now() - birth_date).days // 365
                features['age'] = age
            
            # Genre
            if 'gender' in patient_data:
                features['gender'] = patient_data['gender']
            
            # Code postal (région)
            if 'address' in patient_data and len(patient_data['address']) > 0:
                address = patient_data['address'][0]
                if 'postalCode' in address:
                    features['postal_code'] = address['postalCode'][:3]  # 3 premiers chiffres
                if 'state' in address:
                    features['state'] = address['state']
            
            logger.info(f"Extracted patient features: age={features.get('age')}, gender={features.get('gender')}")
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting patient features: {e}")
            return {}
 
