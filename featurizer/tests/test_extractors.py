import pytest
from extractors.patient_features import PatientFeatureExtractor
from extractors.vital_signs_features import VitalSignsFeatureExtractor
from extractors.lab_results_features import LabResultsFeatureExtractor

def test_patient_feature_extractor():
    """Test de l'extracteur de features patient"""
    extractor = PatientFeatureExtractor()
    
    patient_data = {
        'birthDate': '1984-07-02',
        'gender': 'male',
        'address': [{
            'postalCode': '01887',
            'state': 'Massachusetts'
        }]
    }
    
    features = extractor.extract(patient_data)
    
    assert 'age' in features
    assert features['age'] > 0
    assert features['gender'] == 'male'
    assert features['postal_code'] == '018'

def test_vital_signs_extractor():
    """Test de l'extracteur de signes vitaux"""
    extractor = VitalSignsFeatureExtractor()
    
    observations = [
        {
            'code': {'coding': [{'code': '8302-2'}]},
            'valueQuantity': {'value': 168.8}
        },
        {
            'code': {'coding': [{'code': '29463-7'}]},
            'valueQuantity': {'value': 81.7}
        }
    ]
    
    features = extractor.extract(observations)
    
    assert 'height_cm' in features
    assert 'weight_kg' in features
    assert 'bmi' in features
    assert features['bmi'] > 0

def test_lab_results_extractor():
    """Test de l'extracteur de résultats de labo"""
    extractor = LabResultsFeatureExtractor()
    
    observations = [
        {
            'code': {'coding': [{'code': '2093-3'}]},
            'valueQuantity': {'value': 184.8}
        },
        {
            'code': {'coding': [{'code': '2085-9'}]},
            'valueQuantity': {'value': 68.2}
        }
    ]
    
    features = extractor.extract(observations)
    
    assert 'avg_cholesterol' in features
    assert 'avg_hdl' in features
    assert features['avg_cholesterol'] == 184.8
  /F
