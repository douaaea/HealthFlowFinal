import json
import logging

logger = logging.getLogger(__name__)

class ObservationAnonymizer:
    """Anonymiseur de ressources Observation FHIR"""
    
    def __init__(self, rules, pseudonym_manager):
        self.rules = rules
        self.pm = pseudonym_manager
    
    def anonymize(self, observation_data, patient_id_mapping):
        """Anonymise une observation FHIR"""
        try:
            # Gérer le cas où data est déjà un dict ou une string
            if isinstance(observation_data, str):
                observation = json.loads(observation_data)
            elif isinstance(observation_data, dict):
                observation = observation_data
            else:
                raise ValueError(f"Invalid data type: {type(observation_data)}")
            
            if observation.get('resourceType') != 'Observation':
                raise ValueError(f"Expected Observation, got {observation.get('resourceType')}")
            
            # Anonymiser l'ID
            original_id = observation.get('id')
            observation['id'] = self.pm._generate_hash(original_id)[:16]
            
            # Mettre à jour la référence au patient
            if 'subject' in observation and 'reference' in observation['subject']:
                original_patient_ref = observation['subject']['reference']
                original_patient_id = original_patient_ref.split('/')[-1]
                
                if original_patient_id in patient_id_mapping:
                    anonymized_patient_id = patient_id_mapping[original_patient_id]
                    observation['subject']['reference'] = f"Patient/{anonymized_patient_id}"
            
            # Mettre à jour la référence à l'encounter si présente
            if 'encounter' in observation and 'reference' in observation['encounter']:
                original_encounter_ref = observation['encounter']['reference']
                original_encounter_id = original_encounter_ref.split('/')[-1]
                anonymized_encounter_id = self.pm._generate_hash(original_encounter_id)[:16]
                observation['encounter']['reference'] = f"Encounter/{anonymized_encounter_id}"
            
            logger.info(f"Anonymized observation {original_id} -> {observation['id']}")
            
            return json.dumps(observation, indent=2)
            
        except Exception as e:
            logger.error(f"Error anonymizing observation: {e}")
            raise
