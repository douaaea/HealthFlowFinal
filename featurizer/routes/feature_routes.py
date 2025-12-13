from flask import Blueprint, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.feature_vector import PatientFeatures, Base
from extractors.patient_features import PatientFeatureExtractor
from extractors.vital_signs_features import VitalSignsFeatureExtractor
from extractors.lab_results_features import LabResultsFeatureExtractor
from config import Config
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

feature_bp = Blueprint('features', __name__)

# Initialisation DB
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Initialisation des extracteurs
patient_extractor = PatientFeatureExtractor()
vitals_extractor = VitalSignsFeatureExtractor()
labs_extractor = LabResultsFeatureExtractor()

@feature_bp.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'UP',
        'service': 'Featurizer'
    })

@feature_bp.route('/extract/patient/<patient_id>', methods=['POST'])
def extract_patient_features(patient_id):
    """Extrait les features d'un patient spécifique depuis les données anonymisées"""
    try:
        session = Session()
        
        # Requête pour récupérer le patient anonymisé
        from sqlalchemy import text
        query = text("""
            SELECT resource_data 
            FROM fhir_resources_anonymized 
            WHERE anonymized_fhir_id = :patient_id 
            AND resource_type = 'Patient'
        """)
        
        patient_result = session.execute(query, {'patient_id': patient_id}).fetchone()
        
        if not patient_result:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Parser le JSON
        patient_data = json.loads(patient_result[0]) if isinstance(patient_result[0], str) else patient_result[0]
        
        # Récupérer les observations du patient
        obs_query = text("""
            SELECT resource_data 
            FROM fhir_resources_anonymized 
            WHERE resource_data::json->'subject'->>'reference' = :patient_ref
            AND resource_type = 'Observation'
        """)
        
        obs_results = session.execute(obs_query, {'patient_ref': f'Patient/{patient_id}'}).fetchall()
        observations = [json.loads(row[0]) if isinstance(row[0], str) else row[0] for row in obs_results]
        
        # Extraire les features
        patient_features = patient_extractor.extract(patient_data)
        vitals_features = vitals_extractor.extract(observations)
        labs_features = labs_extractor.extract(observations)
        
        # Calculer les features cliniques
        clinical_features = {}
        if observations:
            clinical_features['total_observations'] = len(observations)
            
            # Calculer la durée d'observation
            dates = []
            for obs in observations:
                if 'effectiveDateTime' in obs:
                    try:
                        date = datetime.fromisoformat(obs['effectiveDateTime'].replace('Z', '+00:00'))
                        dates.append(date)
                    except:
                        pass
            
            if len(dates) > 1:
                dates.sort()
                span = (dates[-1] - dates[0]).days
                clinical_features['observation_span_days'] = span
                clinical_features['consultation_frequency'] = round(len(observations) / max(span, 1), 4)
        
        # Combiner toutes les features
        all_features = {**patient_features, **vitals_features, **labs_features, **clinical_features}
        
        # Sauvegarder dans la base
        existing = session.query(PatientFeatures).filter_by(patient_id=patient_id).first()
        
        if existing:
            # Mettre à jour
            for key, value in all_features.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.features_json = all_features
            existing.extraction_date = datetime.utcnow()
        else:
            # Créer nouveau
            feature_record = PatientFeatures(
                patient_id=patient_id,
                age=all_features.get('age'),
                gender=all_features.get('gender'),
                bmi=all_features.get('bmi'),
                avg_systolic_bp=all_features.get('avg_systolic_bp'),
                avg_diastolic_bp=all_features.get('avg_diastolic_bp'),
                height_cm=all_features.get('height_cm'),
                weight_kg=all_features.get('weight_kg'),
                avg_cholesterol=all_features.get('avg_cholesterol'),
                avg_hdl=all_features.get('avg_hdl'),
                avg_ldl=all_features.get('avg_ldl'),
                avg_triglycerides=all_features.get('avg_triglycerides'),
                avg_hemoglobin=all_features.get('avg_hemoglobin'),
                total_observations=all_features.get('total_observations'),
                observation_span_days=all_features.get('observation_span_days'),
                consultation_frequency=all_features.get('consultation_frequency'),
                features_json=all_features
            )
            session.add(feature_record)
        
        session.commit()
        session.close()
        
        return jsonify({
            'status': 'success',
            'patient_id': patient_id,
            'features': all_features
        }), 200
        
    except Exception as e:
        logger.error(f"Error extracting features: {e}")
        return jsonify({'error': str(e)}), 500

@feature_bp.route('/extract/all', methods=['POST'])
def extract_all_features():
    """Extrait les features de tous les patients anonymisés"""
    try:
        session = Session()
        
        # Récupérer tous les patients anonymisés
        from sqlalchemy import text
        query = text("""
            SELECT anonymized_fhir_id 
            FROM fhir_resources_anonymized 
            WHERE resource_type = 'Patient'
        """)
        
        patients = session.execute(query).fetchall()
        session.close()
        
        results = []
        errors = []
        
        for patient in patients:
            patient_id = patient[0]
            try:
                # Appeler extract_patient_features pour chaque patient
                result = extract_patient_features(patient_id)
                if result[1] == 200:
                    results.append(patient_id)
                else:
                    errors.append({'patient_id': patient_id, 'error': result[0].get_json()})
            except Exception as e:
                errors.append({'patient_id': patient_id, 'error': str(e)})
        
        return jsonify({
            'status': 'success',
            'extracted': len(results),
            'errors': len(errors),
            'patient_ids': results,
            'error_details': errors
        }), 200
        
    except Exception as e:
        logger.error(f"Error in bulk extraction: {e}")
        return jsonify({'error': str(e)}), 500

@feature_bp.route('/features/<patient_id>', methods=['GET'])
def get_patient_features(patient_id):
    """Récupère les features d'un patient"""
    try:
        session = Session()
        features = session.query(PatientFeatures).filter_by(patient_id=patient_id).first()
        session.close()
        
        if not features:
            return jsonify({'error': 'Features not found'}), 404
        
        return jsonify(features.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error retrieving features: {e}")
        return jsonify({'error': str(e)}), 500

@feature_bp.route('/stats', methods=['GET'])
def get_stats():
    """Statistiques sur les features extraites"""
    try:
        session = Session()
        
        from sqlalchemy import func
        
        total = session.query(func.count(PatientFeatures.id)).scalar()
        
        avg_age = session.query(func.avg(PatientFeatures.age)).scalar()
        avg_bmi = session.query(func.avg(PatientFeatures.bmi)).scalar()
        avg_cholesterol = session.query(func.avg(PatientFeatures.avg_cholesterol)).scalar()
        
        session.close()
        
        return jsonify({
            'total_patients': total,
            'average_age': round(avg_age, 1) if avg_age else None,
            'average_bmi': round(avg_bmi, 2) if avg_bmi else None,
            'average_cholesterol': round(avg_cholesterol, 2) if avg_cholesterol else None
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

@feature_bp.route('/features', methods=['GET'])
def list_all_features():
    """Liste toutes les features extraites"""
    try:
        session = Session()
        all_features = session.query(PatientFeatures).all()
        session.close()
        
        return jsonify({
            'total': len(all_features),
            'features': [f.to_dict() for f in all_features]
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing features: {e}")
        return jsonify({'error': str(e)}), 500
 
