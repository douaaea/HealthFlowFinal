import pytest
from calculators.framingham_score import FraminghamCalculator
from calculators.ascvd_calculator import ASCVDCalculator
from models.prediction_model import CVDRiskModel

def test_framingham_male_low_risk():
    """Test Framingham pour homme à faible risque"""
    risk = FraminghamCalculator.calculate(
        age=35,
        gender='male',
        total_cholesterol=180,
        hdl=55,
        systolic_bp=115,
        on_bp_medication=False,
        smoker=False,
        diabetic=False
    )
    assert risk < 5

def test_framingham_male_high_risk():
    """Test Framingham pour homme à haut risque"""
    risk = FraminghamCalculator.calculate(
        age=65,
        gender='male',
        total_cholesterol=260,
        hdl=35,
        systolic_bp=150,
        on_bp_medication=True,
        smoker=True,
        diabetic=True
    )
    assert risk > 15

def test_ascvd_calculator():
    """Test ASCVD calculator"""
    risk = ASCVDCalculator.calculate(
        age=55,
        gender='male',
        race='white',
        total_cholesterol=200,
        hdl=45,
        systolic_bp=130,
        on_bp_medication=False,
        diabetic=False,
        smoker=False
    )
    assert 0 <= risk <= 100

def test_cvd_model():
    """Test du modèle CVD"""
    model = CVDRiskModel()
    
    features = {
        'age': 50,
        'gender': 'male',
        'avg_systolic_bp': 140,
        'avg_cholesterol': 220,
        'bmi': 28,
        'avg_hdl': 45
    }
    
    risk = model.predict(features)
    assert 0 <= risk <= 100
    
    category = model.classify_risk(risk)
    assert category in ['low', 'moderate', 'high']

def test_risk_factors_identification():
    """Test identification des facteurs de risque"""
    model = CVDRiskModel()
    
    features = {
        'age': 65,
        'avg_systolic_bp': 150,
        'avg_cholesterol': 240,
        'bmi': 32,
        'avg_hdl': 35
    }
    
    risk_factors = model.identify_risk_factors(features)
    assert len(risk_factors) > 0
    assert any(rf['factor'] == 'Age' for rf in risk_factors)
    assert any(rf['factor'] == 'Hypertension' for rf in risk_factors)
 
