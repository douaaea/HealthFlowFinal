import logging
import statistics

logger = logging.getLogger(__name__)

class LabResultsFeatureExtractor:
    """Extracteur de features des résultats de laboratoire"""
    
    # Codes LOINC pour les résultats de labo
    LOINC_CODES = {
        'cholesterol': '2093-3',
        'hdl': '2085-9',
        'ldl': '18262-6',
        'triglycerides': '2571-8',
        'hemoglobin': '718-7',
        'hematocrit': '4544-3',
        'wbc': '6690-2',
        'rbc': '789-8',
        'platelets': '777-3',
        'glucose': '2345-7'
    }

    def __init__(self):
        pass

    def extract(self, observations):
        """Extrait les features des résultats de laboratoire"""
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
            
            # Cholestérol total
            if self.LOINC_CODES['cholesterol'] in obs_by_code:
                values = [obs.get('valueQuantity', {}).get('value')
                         for obs in obs_by_code[self.LOINC_CODES['cholesterol']]
                         if obs.get('valueQuantity', {}).get('value')]
                if values:
                    features['avg_cholesterol'] = round(statistics.mean(values), 2)
                    features['latest_cholesterol'] = values[-1]
            
            # HDL
            if self.LOINC_CODES['hdl'] in obs_by_code:
                values = [obs.get('valueQuantity', {}).get('value')
                         for obs in obs_by_code[self.LOINC_CODES['hdl']]
                         if obs.get('valueQuantity', {}).get('value')]
                if values:
                    features['avg_hdl'] = round(statistics.mean(values), 2)
                    features['latest_hdl'] = values[-1]
            
            # LDL
            if self.LOINC_CODES['ldl'] in obs_by_code:
                values = [obs.get('valueQuantity', {}).get('value')
                         for obs in obs_by_code[self.LOINC_CODES['ldl']]
                         if obs.get('valueQuantity', {}).get('value')]
                if values:
                    features['avg_ldl'] = round(statistics.mean(values), 2)
                    features['latest_ldl'] = values[-1]
            
            # Triglycérides
            if self.LOINC_CODES['triglycerides'] in obs_by_code:
                values = [obs.get('valueQuantity', {}).get('value')
                         for obs in obs_by_code[self.LOINC_CODES['triglycerides']]
                         if obs.get('valueQuantity', {}).get('value')]
                if values:
                    features['avg_triglycerides'] = round(statistics.mean(values), 2)
                    features['latest_triglycerides'] = values[-1]
            
            # Hémoglobine
            if self.LOINC_CODES['hemoglobin'] in obs_by_code:
                values = [obs.get('valueQuantity', {}).get('value')
                         for obs in obs_by_code[self.LOINC_CODES['hemoglobin']]
                         if obs.get('valueQuantity', {}).get('value')]
                if values:
                    features['avg_hemoglobin'] = round(statistics.mean(values), 2)
                    features['latest_hemoglobin'] = values[-1]
            
            # VALEURS PAR DÉFAUT SI MANQUANTES
            if 'avg_cholesterol' not in features:
                features['avg_cholesterol'] = 200.0
                logger.warning("Cholesterol missing, using default value 200.0")
            
            if 'avg_hdl' not in features:
                features['avg_hdl'] = 50.0
                logger.warning("HDL missing, using default value 50.0")
            
            if 'avg_ldl' not in features:
                features['avg_ldl'] = 100.0
                logger.warning("LDL missing, using default value 100.0")
            
            if 'avg_triglycerides' not in features:
                features['avg_triglycerides'] = 150.0
                logger.warning("Triglycerides missing, using default value 150.0")
            
            logger.info(f"Extracted lab features: Cholesterol={features.get('avg_cholesterol')}, HDL={features.get('avg_hdl')}")
            return features
            
        except Exception as e:
            logger.error(f"Error extracting lab results features: {e}")
            return {
                'avg_cholesterol': 200.0,
                'avg_hdl': 50.0,
                'avg_ldl': 100.0,
                'avg_triglycerides': 150.0
            }
