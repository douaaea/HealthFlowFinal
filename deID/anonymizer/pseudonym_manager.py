from faker import Faker
import hashlib
import json
import logging

logger = logging.getLogger(__name__)

class PseudonymManager:
    """Gestionnaire de pseudonymes cohérents"""
    
    def __init__(self, seed=None):
        self.faker = Faker('en_US')
        if seed:
            Faker.seed(seed)
        
        # Cache des pseudonymes pour cohérence
        self._name_cache = {}
        self._ssn_cache = {}
        self._phone_cache = {}
        self._address_cache = {}
        
    def _generate_hash(self, value):
        """Génère un hash stable pour un identifiant"""
        return hashlib.sha256(str(value).encode()).hexdigest()
    
    def get_pseudonym_name(self, original_name, gender='male'):
        """Génère un pseudonyme de nom cohérent"""
        cache_key = self._generate_hash(original_name)
        
        if cache_key not in self._name_cache:
            if gender.lower() in ['male', 'm']:
                first_name = self.faker.first_name_male()
            elif gender.lower() in ['female', 'f']:
                first_name = self.faker.first_name_female()
            else:
                first_name = self.faker.first_name()
            
            last_name = self.faker.last_name()
            self._name_cache[cache_key] = {
                'first': first_name,
                'last': last_name,
                'full': f"{first_name} {last_name}"
            }
        
        return self._name_cache[cache_key]
    
    def get_pseudonym_ssn(self, original_ssn):
        """Génère un pseudonyme de SSN"""
        cache_key = self._generate_hash(original_ssn)
        
        if cache_key not in self._ssn_cache:
            self._ssn_cache[cache_key] = self.faker.ssn()
        
        return self._ssn_cache[cache_key]
    
    def get_pseudonym_phone(self, original_phone):
        """Génère un pseudonyme de téléphone"""
        cache_key = self._generate_hash(original_phone)
        
        if cache_key not in self._phone_cache:
            self._phone_cache[cache_key] = self.faker.phone_number()
        
        return self._phone_cache[cache_key]
    
    def get_pseudonym_address(self, original_address):
        """Génère un pseudonyme d'adresse"""
        cache_key = self._generate_hash(json.dumps(original_address, sort_keys=True))
        
        if cache_key not in self._address_cache:
            self._address_cache[cache_key] = {
                'line': [self.faker.street_address()],
                'city': self.faker.city(),
                'state': self.faker.state(),
                'postalCode': self.faker.zipcode(),
                'country': 'US'
            }
        
        return self._address_cache[cache_key]
    
    def redact_ssn(self, ssn):
        """Masque complètement un SSN"""
        return "XXX-XX-XXXX"
    
    def get_cache_stats(self):
        """Statistiques du cache"""
        return {
            'names': len(self._name_cache),
            'ssn': len(self._ssn_cache),
            'phones': len(self._phone_cache),
            'addresses': len(self._address_cache)
        }
 
