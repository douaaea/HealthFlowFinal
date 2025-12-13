import numpy as np
from datetime import datetime

class CVDRiskModel:
    """Modèle de prédiction de risque cardiovasculaire"""
    
    def __init__(self):
        self.version = "1.0"
    
    def predict(self, features):
        """Prédit le risque cardiovasculaire basé sur les features"""
        
        # Vérifier les features requises
        required = ['age', 'gender', 'avg_systolic_bp', 'avg_cholesterol', 'bmi']
        missing = [f for f in required if f not in features or features[f] is None]
        
        if missing:
            raise ValueError(f"Missing required features: {missing}")
        
        # Extraire les features
        age = features['age']
        gender = features['gender']
        systolic_bp = features['avg_systolic_bp']
        cholesterol = features['avg_cholesterol']
        bmi = features['bmi']
        hdl = features.get('avg_hdl', 50)
        
        # Calculer le score de risque (simplifié)
        risk_score = 0
        
        # Age (0-30 points)
        if age < 35:
            risk_score += 0
        elif age < 45:
            risk_score += 5
        elif age < 55:
            risk_score += 10
        elif age < 65:
            risk_score += 20
        else:
            risk_score += 30
        
        # Genre (hommes +5)
        if gender == 'male':
            risk_score += 5
        
        # Tension artérielle (0-20 points)
        if systolic_bp < 120:
            risk_score += 0
        elif systolic_bp < 130:
            risk_score += 5
        elif systolic_bp < 140:
            risk_score += 10
        elif systolic_bp < 160:
            risk_score += 15
        else:
            risk_score += 20
        
        # Cholestérol total (0-15 points)
        if cholesterol < 200:
            risk_score += 0
        elif cholesterol < 240:
            risk_score += 5
        elif cholesterol < 280:
            risk_score += 10
        else:
            risk_score += 15
        
        # HDL (protecteur)
        if hdl > 60:
            risk_score -= 5
        elif hdl < 40:
            risk_score += 5
        
        # IMC (0-10 points)
        if bmi < 25:
            risk_score += 0
        elif bmi < 30:
            risk_score += 3
        elif bmi < 35:
            risk_score += 7
        else:
            risk_score += 10
        
        # Convertir en pourcentage de risque sur 10 ans
        risk_percentage = min(max(risk_score, 0), 100)
        
        return risk_percentage
    
    def classify_risk(self, risk_percentage):
        """Classifie le niveau de risque"""
        if risk_percentage < 7.5:
            return 'low'
        elif risk_percentage < 20:
            return 'moderate'
        else:
            return 'high'
    
    def identify_risk_factors(self, features):
        """Identifie les facteurs de risque présents"""
        risk_factors = []
        
        age = features.get('age', 0)
        systolic_bp = features.get('avg_systolic_bp', 0)
        cholesterol = features.get('avg_cholesterol', 0)
        bmi = features.get('bmi', 0)
        hdl = features.get('avg_hdl', 50)
        
        if age >= 45:
            risk_factors.append({
                'factor': 'Age',
                'value': age,
                'severity': 'high' if age >= 65 else 'moderate'
            })
        
        if systolic_bp >= 130:
            risk_factors.append({
                'factor': 'Hypertension',
                'value': systolic_bp,
                'severity': 'high' if systolic_bp >= 140 else 'moderate'
            })
        
        if cholesterol >= 200:
            risk_factors.append({
                'factor': 'High Cholesterol',
                'value': cholesterol,
                'severity': 'high' if cholesterol >= 240 else 'moderate'
            })
        
        if bmi >= 25:
            risk_factors.append({
                'factor': 'Overweight/Obesity',
                'value': bmi,
                'severity': 'high' if bmi >= 30 else 'moderate'
            })
        
        if hdl < 40:
            risk_factors.append({
                'factor': 'Low HDL Cholesterol',
                'value': hdl,
                'severity': 'moderate'
            })
        
        return risk_factors
    
    def generate_recommendations(self, risk_category, risk_factors):
        """Génère des recommandations personnalisées"""
        recommendations = []
        
        if risk_category == 'high':
            recommendations.append({
                'priority': 'urgent',
                'action': 'Consult cardiologist',
                'description': 'Schedule an appointment with a cardiologist within 2 weeks'
            })
        
        # Recommandations basées sur les facteurs de risque
        factor_types = [rf['factor'] for rf in risk_factors]
        
        if 'Hypertension' in factor_types:
            recommendations.append({
                'priority': 'high',
                'action': 'Blood pressure management',
                'description': 'Monitor blood pressure daily, consider medication'
            })
        
        if 'High Cholesterol' in factor_types:
            recommendations.append({
                'priority': 'high',
                'action': 'Cholesterol management',
                'description': 'Low-fat diet, consider statin therapy'
            })
        
        if 'Overweight/Obesity' in factor_types:
            recommendations.append({
                'priority': 'moderate',
                'action': 'Weight loss program',
                'description': 'Aim for 5-10% weight reduction through diet and exercise'
            })
        
        # Recommandations générales
        recommendations.append({
            'priority': 'moderate',
            'action': 'Lifestyle modifications',
            'description': 'Regular exercise (150 min/week), Mediterranean diet, smoking cessation'
        })
        
        recommendations.append({
            'priority': 'low',
            'action': 'Regular monitoring',
            'description': 'Annual health check-up with lipid panel and blood pressure monitoring'
        })
        
        return recommendations
 
