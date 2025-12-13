import json
from datetime import datetime, timedelta
import logging
from anonymizer.pseudonym_manager import PseudonymManager

logger = logging.getLogger(__name__)

class PatientAnonymizer:
    """Anonymiseur de ressources Patient FHIR"""
    
    def __init__(self, rules, pseudonym_manager):
        self.rules = rules
        self.pm = pseudonym_manager
    
    def anonymize(self, patient_data):
        """Anonymise un patient FHIR"""
        try:
            # Gérer le cas où data est déjà un dict ou une string
            if isinstance(patient_data, str):
                patient = json.loads(patient_data)
            elif isinstance(patient_data, dict):
                patient = patient_data
            else:
                raise ValueError(f"Invalid data type: {type(patient_data)}")
            
            if patient.get('resourceType') != 'Patient':
                raise ValueError(f"Expected Patient, got {patient.get('resourceType')}")
            
            # Pseudonymiser le nom
            if 'name' in patient:
                patient['name'] = self._anonymize_names(
                    patient['name'], 
                    patient.get('gender', 'unknown')
                )
            
            # Masquer les identifiants
            if 'identifier' in patient:
                patient['identifier'] = self._anonymize_identifiers(patient['identifier'])
            
            # Pseudonymiser les contacts
            if 'telecom' in patient:
                patient['telecom'] = self._anonymize_telecom(patient['telecom'])
            
            # Pseudonymiser les adresses
            if 'address' in patient:
                patient['address'] = self._anonymize_addresses(patient['address'])
            
            # Décaler la date de naissance
            if 'birthDate' in patient and self.rules.get('shift_dates'):
                patient['birthDate'] = self._shift_date(patient['birthDate'])
            
            # Supprimer les extensions sensibles
            patient = self._remove_sensitive_extensions(patient)
            
            # Générer un nouvel ID anonyme
            original_id = patient.get('id')
            patient['id'] = self.pm._generate_hash(original_id)[:16]
            
            logger.info(f"Anonymized patient {original_id} -> {patient['id']}")
            
            return json.dumps(patient, indent=2)
            
        except Exception as e:
            logger.error(f"Error anonymizing patient: {e}")
            raise
    
    def _anonymize_names(self, names, gender):
        """Anonymise les noms"""
        anonymized_names = []
        for name in names:
            original_family = name.get('family', '')
            pseudonym = self.pm.get_pseudonym_name(original_family, gender)
            
            anonymized_name = {
                'use': name.get('use', 'official'),
                'family': pseudonym['last'],
                'given': [pseudonym['first']]
            }
            
            if 'prefix' in name:
                anonymized_name['prefix'] = name['prefix']
            
            anonymized_names.append(anonymized_name)
        
        return anonymized_names
    
    def _anonymize_identifiers(self, identifiers):
        """Anonymise les identifiants"""
        anonymized_ids = []
        
        for identifier in identifiers:
            id_type = identifier.get('type', {}).get('coding', [{}])[0].get('code', '')
            
            if id_type == 'SS' and self.rules.get('redact_ssn'):
                # Masquer SSN
                identifier['value'] = self.pm.redact_ssn(identifier.get('value', ''))
            elif id_type in ['SS', 'DL', 'PPN']:
                # Pseudonymiser autres identifiants sensibles
                original_value = identifier.get('value', '')
                identifier['value'] = self.pm._generate_hash(original_value)[:12]
            elif id_type == 'MR':
                # Pseudonymiser numéro dossier médical
                original_value = identifier.get('value', '')
                identifier['value'] = self.pm._generate_hash(original_value)[:16]
            
            anonymized_ids.append(identifier)
        
        return anonymized_ids
    
    def _anonymize_telecom(self, telecoms):
        """Anonymise les contacts téléphoniques"""
        anonymized_telecoms = []
        
        for telecom in telecoms:
            if telecom.get('system') == 'phone':
                original_phone = telecom.get('value', '')
                telecom['value'] = self.pm.get_pseudonym_phone(original_phone)
            elif telecom.get('system') == 'email':
                # Anonymiser email
                telecom['value'] = f"{self.pm.faker.user_name()}@{self.pm.faker.free_email_domain()}"
            
            anonymized_telecoms.append(telecom)
        
        return anonymized_telecoms
    
    def _anonymize_addresses(self, addresses):
        """Anonymise les adresses"""
        anonymized_addresses = []
        
        for address in addresses:
            original_address_str = json.dumps(address, sort_keys=True)
            pseudonym_address = self.pm.get_pseudonym_address(original_address_str)
            
            anonymized_address = {
                'line': pseudonym_address['line'],
                'city': pseudonym_address['city'],
                'state': pseudonym_address['state'],
                'country': pseudonym_address['country']
            }
            
            # Garder les 3 premiers chiffres du code postal si activé
            if self.rules.get('keep_zip_code_prefix') and 'postalCode' in address:
                original_zip = address['postalCode']
                if len(original_zip) >= 3:
                    anonymized_address['postalCode'] = original_zip[:3] + 'XX'
                else:
                    anonymized_address['postalCode'] = pseudonym_address['postalCode']
            else:
                anonymized_address['postalCode'] = pseudonym_address['postalCode']
            
            anonymized_addresses.append(anonymized_address)
        
        return anonymized_addresses
    
    def _shift_date(self, date_str):
        """Décale une date de manière aléatoire mais cohérente"""
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Utiliser le hash de la date pour un décalage déterministe
            hash_value = int(self.pm._generate_hash(date_str)[:8], 16)
            shift_days = (hash_value % (self.rules['date_shift_days'] * 2)) - self.rules['date_shift_days']
            
            shifted_date = date + timedelta(days=shift_days)
            
            # Garder l'année si la règle est activée
            if self.rules.get('keep_birth_year'):
                shifted_date = shifted_date.replace(year=date.year)
            
            return shifted_date.strftime('%Y-%m-%d')
        except Exception as e:
            logger.warning(f"Could not shift date {date_str}: {e}")
            return date_str
    
    def _remove_sensitive_extensions(self, patient):
        """Supprime les extensions sensibles"""
        sensitive_urls = [
            'http://hl7.org/fhir/StructureDefinition/patient-mothersMaidenName',
            'http://hl7.org/fhir/StructureDefinition/patient-birthPlace',
            'http://synthetichealth.github.io/synthea/disability-adjusted-life-years',
            'http://synthetichealth.github.io/synthea/quality-adjusted-life-years'
        ]
        
        if 'extension' in patient:
            patient['extension'] = [
                ext for ext in patient['extension']
                if ext.get('url') not in sensitive_urls
            ]
        
        return patient
