import logging
import statistics

logger = logging.getLogger(__name__)

class VitalSignsFeatureExtractor:
    """Extracteur de features des signes vitaux"""
    
    # Codes LOINC pour les observations vitales
    LOINC_CODES = {
        'height': '8302-2',
        'weight': '29463-7',
        'bmi': '39156-5',
        'systolic_bp': '8480-6',
        'diastolic_bp': '8462-4',
        'heart_rate': '8867-4',
        'respiratory_rate': '9279-1',
        'body_temp': '8310-5',
        'oxygen_saturation': '2708-6'
    }

    def __init__(self):
        pass

    def extract(self, observations):
        """Extrait les features des observations vitales"""
        try:
            features = {}
            
            # Grouper les observations par code LOINC
            obs_by_code = {}
            for obs in observations:
                if 'code' in obs and 'coding' in obs['code']:
                    code = obs['code']['coding'][0].get('code')
                    if code not in obs_by_code:
                        obs_by_code[code] = []
                    obs_by_code[code].append(obs)
            
            # Extraire la taille (dernière mesure)
            if self.LOINC_CODES['height'] in obs_by_code:
                height_obs = obs_by_code[self.LOINC_CODES['height']]
                if height_obs:
                    features['height_cm'] = height_obs[-1].get('valueQuantity', {}).get('value')
            
            # Extraire le poids (dernière mesure)
            if self.LOINC_CODES['weight'] in obs_by_code:
                weight_obs = obs_by_code[self.LOINC_CODES['weight']]
                if weight_obs:
                    features['weight_kg'] = weight_obs[-1].get('valueQuantity', {}).get('value')
            
            # Calculer l'IMC si on a taille et poids
            if 'height_cm' in features and 'weight_kg' in features:
                height_m = features['height_cm'] / 100
                features['bmi'] = round(features['weight_kg'] / (height_m ** 2), 2)
            
            # Tension artérielle (moyenne)
            systolic_values = []
            diastolic_values = []
            
            for obs in observations:
                if obs.get('code', {}).get('coding', [{}])[0].get('code') == '55284-4':  # Blood Pressure
                    if 'component' in obs:
                        for comp in obs['component']:
                            comp_code = comp.get('code', {}).get('coding', [{}])[0].get('code')
                            value = comp.get('valueQuantity', {}).get('value')
                            if comp_code == self.LOINC_CODES['systolic_bp'] and value:
                                systolic_values.append(value)
                            elif comp_code == self.LOINC_CODES['diastolic_bp'] and value:
                                diastolic_values.append(value)
            
            if systolic_values:
                features['avg_systolic_bp'] = round(statistics.mean(systolic_values), 2)
                features['min_systolic_bp'] = round(min(systolic_values), 2)
                features['max_systolic_bp'] = round(max(systolic_values), 2)
            
            if diastolic_values:
                features['avg_diastolic_bp'] = round(statistics.mean(diastolic_values), 2)
                features['min_diastolic_bp'] = round(min(diastolic_values), 2)
                features['max_diastolic_bp'] = round(max(diastolic_values), 2)
            
            # VALEURS PAR DÉFAUT SI MANQUANTES
            if 'bmi' not in features:
                features['bmi'] = 25.0
                logger.warning("BMI missing, using default value 25.0")
            
            if 'avg_systolic_bp' not in features:
                features['avg_systolic_bp'] = 120.0
                logger.warning("Systolic BP missing, using default value 120.0")
            
            if 'avg_diastolic_bp' not in features:
                features['avg_diastolic_bp'] = 80.0
                logger.warning("Diastolic BP missing, using default value 80.0")
            
            logger.info(f"Extracted vital signs features: BMI={features.get('bmi')}, BP={features.get('avg_systolic_bp')}/{features.get('avg_diastolic_bp')}")
            return features
            
        except Exception as e:
            logger.error(f"Error extracting vital signs features: {e}")
            return {
                'bmi': 25.0,
                'avg_systolic_bp': 120.0,
                'avg_diastolic_bp': 80.0
            }
