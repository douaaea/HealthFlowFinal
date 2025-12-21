#!/usr/bin/env python3
"""
Fill missing features in dataset_final table
Updates vitals, conditions, medications, labs from FHIR bundles
Much faster than full extraction since demographics + labels already done!
"""

import pandas as pd
from sqlalchemy import create_engine, text
import logging
from tqdm import tqdm
import sys
import os

sys.path.append(os.path.dirname(__file__))
from export_structured_features import StructuredFeatureExtractor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_URI = "postgresql://postgres:qwerty@localhost:5433/healthflow_fhir"

def main():
    logger.info("🔧 Filling missing features in dataset_final table")
    logger.info("=" * 50)
    
    try:
        engine = create_engine(DB_URI)
        
        # Load patient IDs from dataset_final
        logger.info("Loading patient list from dataset_final...")
        patients_df = pd.read_sql("SELECT patient_id FROM dataset_final", engine)
        logger.info(f"Found {len(patients_df)} patients")
        
        # Load FHIR bundles for these patients only
        logger.info("Loading FHIR bundles...")
        query = """
        SELECT patient_id, bundle_data 
        FROM fhir_bundles 
        WHERE patient_id IN (SELECT patient_id FROM dataset_final)
        """
        bundles_df = pd.read_sql(query, engine)
        logger.info(f"Loaded {len(bundles_df)} bundles")
        
        # Extract features
        logger.info("Extracting vitals/conditions/meds from bundles...")
        extractor = StructuredFeatureExtractor(engine)
        
        updates = []
        for _, row in tqdm(bundles_df.iterrows(), total=len(bundles_df), desc="Processing"):
            features = extractor.extract_all_features(row['patient_id'], row['bundle_data'])
            if features:
                updates.append(features)
        
        logger.info(f"Extracted features for {len(updates)} patients")
        
        # Update dataset_final table
        logger.info("Updating dataset_final table...")
        with engine.begin() as conn:
            for feat in tqdm(updates, desc="Updating DB"):
                conn.execute(text("""
                    UPDATE dataset_final SET
                        vit_sys_bp = :vit_sys_bp,
                        vit_dia_bp = :vit_dia_bp,
                        vit_heart_rate = :vit_heart_rate,
                        vit_resp_rate = :vit_resp_rate,
                        vit_temp = :vit_temp,
                        vit_weight = :vit_weight,
                        vit_height = :vit_height,
                        vit_bmi = :vit_bmi,
                        cond_diabetes = :cond_diabetes,
                        cond_hypertension = :cond_hypertension,
                        cond_chf = :cond_chf,
                        cond_copd = :cond_copd,
                        cond_ckd = :cond_ckd,
                        cond_cancer = :cond_cancer,
                        num_conditions = :num_conditions,
                        med_insulin = :med_insulin,
                        med_metformin = :med_metformin,
                        med_statin = :med_statin,
                        med_ace_inhibitor = :med_ace_inhibitor,
                        med_beta_blocker = :med_beta_blocker,
                        num_medications = :num_medications,
                        polypharmacy = :polypharmacy,
                        lab_glucose = :lab_glucose,
                        lab_hba1c = :lab_hba1c,
                        lab_creatinine = :lab_creatinine,
                        lab_cholesterol = :lab_cholesterol,
                        lab_ldl = :lab_ldl,
                        lab_hdl = :lab_hdl
                    WHERE patient_id = :patient_id
                """), feat)
        
        logger.info("✅ Dataset updated successfully!")
        logger.info("\n💡 Next: Export with:")
        logger.info("   psql -h localhost -p 5433 -U postgres -d healthflow_fhir -c \"\\COPY dataset_final TO '../dataset_structured.csv' CSV HEADER\"")
        
        engine.dispose()
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
