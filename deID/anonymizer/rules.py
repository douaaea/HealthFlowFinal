"""
Règles d'anonymisation FHIR
Conformité RGPD et HIPAA
"""

# Champs à pseudonymiser
FIELDS_TO_PSEUDONYMIZE = {
    'Patient': ['name', 'identifier', 'telecom', 'address'],
    'Observation': ['id', 'subject', 'encounter'],
    'MedicationStatement': ['id', 'subject', 'context']
}

# Champs à supprimer complètement
FIELDS_TO_REMOVE = {
    'Patient': ['photo'],
    'Observation': [],
    'MedicationStatement': []
}

# Extensions sensibles à supprimer
SENSITIVE_EXTENSIONS = [
    'http://hl7.org/fhir/StructureDefinition/patient-mothersMaidenName',
    'http://hl7.org/fhir/StructureDefinition/patient-birthPlace',
    'http://synthetichealth.github.io/synthea/disability-adjusted-life-years',
    'http://synthetichealth.github.io/synthea/quality-adjusted-life-years'
]

# Types d'identifiants à traiter
IDENTIFIER_TYPES = {
    'SS': 'redact',      # Social Security Number - masquer
    'DL': 'pseudonymize', # Driver's License - pseudonymiser
    'PPN': 'pseudonymize', # Passport - pseudonymiser
    'MR': 'pseudonymize'  # Medical Record Number - pseudonymiser
}
