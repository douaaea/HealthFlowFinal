#!/usr/bin/env python3
"""
PARALLEL Structured Feature Extraction - 8x faster!
Uses multiprocessing to extract features from FHIR bundles in parallel
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import logging
from datetime import datetime
from typing import Dict, List
from multiprocessing import Pool, cpu_count
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_URI = "postgresql://postgres:qwerty@localhost:5433/healthflow_fhir"

# Import the extractor class from the original script
import sys
import os
sys.path.append(os.path.dirname(__file__))
from export_structured_features import StructuredFeatureExtractor

def process_bundle_worker(args):
    """Worker function to process a single bundle (for multiprocessing)"""
    patient_id, bundle_data = args
    
    # Create extractor instance (each worker needs its own)
    engine = create_engine(DB_URI)
    extractor = StructuredFeatureExtractor(engine)
    
    try:
        features = extractor.extract_all_features(patient_id, bundle_data)
        engine.dispose()
        return features
    except Exception as e:
        engine.dispose()
        return None

def main():
    """Main execution with parallel processing"""
    logger.info("🏥 PARALLEL Structured Feature Extraction")
    logger.info("=" * 50)
    
    OUTPUT_CSV = "../dataset_structured.csv"
    
    try:
        # Connect to database
        logger.info("Connecting to PostgreSQL...")
        engine = create_engine(DB_URI)
        
        # Load FHIR bundles
        logger.info("Loading FHIR bundles from database...")
        query = "SELECT patient_id, bundle_data FROM fhir_bundles ORDER BY patient_id"
        bundles_df = pd.read_sql(query, engine)
        logger.info(f"Loaded {len(bundles_df)} FHIR bundles")
        
        # Prepare data for parallel processing
        bundle_args = [(row['patient_id'], row['bundle_data']) for _, row in bundles_df.iterrows()]
        
        # Parallel extraction
        num_workers = cpu_count()
        logger.info(f"🚀 Using {num_workers} parallel workers")
        logger.info("Extracting structured features in parallel...")
        
        with Pool(num_workers) as pool:
            features_list = []
            failed_count = 0
            
            # Process in chunks with progress
            chunk_size = 50
            for i in range(0, len(bundle_args), chunk_size):
                chunk = bundle_args[i:i+chunk_size]
                results = pool.map(process_bundle_worker, chunk)
                
                for result in results:
                    if result:
                        features_list.append(result)
                    else:
                        failed_count += 1
                
                logger.info(f"   Processed {min(i+chunk_size, len(bundle_args))}/{len(bundle_args)} patients...")
        
        if failed_count > 0:
            logger.warning(f"Failed to process {failed_count} patients")
        
        # Create DataFrame
        features_df = pd.DataFrame(features_list)
        logger.info(f"✅ Extracted features for {len(features_df)} patients")
        
        # Save to CSV
        logger.info(f"Saving to {OUTPUT_CSV}...")
        features_df.to_csv(OUTPUT_CSV, index=False)
        
        # Show statistics
        logger.info("\n📊 Dataset Statistics:")
        logger.info(f"   Total patients: {len(features_df)}")
        logger.info(f"   Total features: {len(features_df.columns)}")
        logger.info(f"\n📝 Sample Features (first patient):")
        for col in list(features_df.columns)[:10]:
            logger.info(f"   {col}: {features_df[col].iloc[0]}")
        
        logger.info("\n🎉 PARALLEL feature extraction complete!")
        logger.info(f"✅ Dataset saved to: {OUTPUT_CSV}")
        logger.info(f"\n💡 Next step: python3 extract_biobert_features.py")
        
        engine.dispose()
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
