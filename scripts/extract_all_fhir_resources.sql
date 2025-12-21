-- ============================================================================
-- COMPLETE FHIR EXTRACTION TO RELATIONAL TABLES
-- Extracts ALL resources: Patients, Encounters, Observations, Conditions, Medications
-- 100% SQL - NO JSON parsing needed!
-- ============================================================================

SET work_mem = '2GB';
SET max_parallel_workers_per_gather = 4;

\echo '=== Extracting ALL FHIR resources to relational tables ==='

-- Drop existing tables
DROP TABLE IF EXISTS raw_observations CASCADE;
DROP TABLE IF EXISTS raw_conditions CASCADE;
DROP TABLE IF EXISTS raw_medications CASCADE;

-- 1. Observations (vitals + labs)
\echo '... Extracting Observations (vitals + labs) ...'
CREATE TABLE raw_observations AS
WITH obs_resources AS (
    SELECT 
        patient_id,
        jsonb_array_elements(bundle_data::jsonb->'entry') as entry
    FROM fhir_bundles
)
SELECT 
    patient_id,
    entry->'resource'->>'id' as observation_id,
    (entry->'resource'->'effectiveDateTime')::text as observation_date,
    entry->'resource'->'code'->>'text' as code_text,
    entry->'resource'->'code'->'coding'->0->>'code' as code,
    (entry->'resource'->'valueQuantity'->>'value')::float as value,
    entry->'resource'->'valueQuantity'->>'unit' as unit
FROM obs_resources
WHERE entry->'resource'->>'resourceType' = 'Observation'
AND entry->'resource'->'valueQuantity'->>'value' IS NOT NULL;

CREATE INDEX idx_raw_obs_patient ON raw_observations(patient_id);
CREATE INDEX idx_raw_obs_code ON raw_observations(code);

-- 2. Conditions (diagnoses)
\echo '... Extracting Conditions (diagnoses) ...'
CREATE TABLE raw_conditions AS
WITH cond_resources AS (
    SELECT 
        patient_id,
        jsonb_array_elements(bundle_data::jsonb->'entry') as entry
    FROM fhir_bundles
)
SELECT 
    patient_id,
    entry->'resource'->>'id' as condition_id,
    entry->'resource'->'code'->>'text' as description,
    entry->'resource'->'code'->'coding'->0->>'code' as code,
    (entry->'resource'->'onsetDateTime')::text as onset_date
FROM cond_resources
WHERE entry->'resource'->>'resourceType' = 'Condition';

CREATE INDEX idx_raw_cond_patient ON raw_conditions(patient_id);

-- 3. Medications
\echo '... Extracting Medications ...'
CREATE TABLE raw_medications AS
WITH med_resources AS (
    SELECT 
        patient_id,
        jsonb_array_elements(bundle_data::jsonb->'entry') as entry
    FROM fhir_bundles
)
SELECT 
    patient_id,
    entry->'resource'->>'id' as medication_id,
    entry->'resource'->'medicationCodeableConcept'->>'text' as description,
    entry->'resource'->'medicationCodeableConcept'->'coding'->0->>'code' as code
FROM med_resources
WHERE entry->'resource'->>'resourceType' = 'MedicationRequest';

CREATE INDEX idx_raw_med_patient ON raw_medications(patient_id);

-- Statistics
\echo '=== Extraction Statistics ==='
SELECT 'Patients' as resource, COUNT(DISTINCT id)::text as count FROM raw_patients
UNION ALL
SELECT 'Encounters', COUNT(*)::text FROM raw_encounters
UNION ALL
SELECT 'Observations', COUNT(*)::text FROM raw_observations
UNION ALL
SELECT 'Conditions', COUNT(*)::text FROM raw_conditions
UNION ALL
SELECT 'Medications', COUNT(*)::text FROM raw_medications;

\echo '=== ✅ All FHIR resources extracted to relational tables! ==='
