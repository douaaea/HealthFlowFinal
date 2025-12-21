-- ============================================================================
-- BUILD COMPLETE DATASET FROM RELATIONAL TABLES ONLY
-- 100% SQL - NO Python needed! Ultra-fast!
-- ============================================================================

SET work_mem = '2GB';
SET max_parallel_workers_per_gather = 4;

DROP TABLE IF EXISTS dataset_final CASCADE;

\echo '=== Building complete dataset from relational tables ==='

CREATE TABLE dataset_final AS
WITH 
-- Base demographics
patient_base AS (
    SELECT 
        p.id as patient_id,
        EXTRACT(YEAR FROM age(CURRENT_DATE, p.birthdate))::int AS age,
        CASE WHEN p.gender = 'male' THEN 1 ELSE 0 END AS gender_male,
        CASE WHEN p.gender = 'female' THEN 1 ELSE 0 END AS gender_female,
        CASE WHEN p.race LIKE '%white%' THEN 1 ELSE 0 END AS race_white,
        CASE WHEN p.race LIKE '%black%' OR p.race LIKE '%african%' THEN 1 ELSE 0 END AS race_black,
        CASE WHEN p.race LIKE '%asian%' THEN 1 ELSE 0 END AS race_asian,
        0 AS ethnicity_hispanic
    FROM raw_patients p
),
-- Readmissions
readmissions AS (
    SELECT 
        patient_id,
        MAX(label_readmission) as label_readmission
    FROM patient_readmissions
    GROUP BY patient_id
),
-- Vitals (average per patient) - FIXED CODES
vitals AS (
    SELECT 
        patient_id,
        AVG(CASE WHEN code = '8478-0' THEN value END) as vit_sys_bp,  -- Mean BP (Synthea doesn't have sys/dia separate)
        0 as vit_dia_bp,  -- Not available in Synthea
        AVG(CASE WHEN code = '8867-4' THEN value END) as vit_heart_rate,
        AVG(CASE WHEN code = '9279-1' THEN value END) as vit_resp_rate,
        AVG(CASE WHEN code = '8310-5' THEN value END) as vit_temp,
        AVG(CASE WHEN code = '29463-7' THEN value END) as vit_weight,
        AVG(CASE WHEN code = '8302-2' THEN value END) as vit_height,
        AVG(CASE WHEN code = '39156-5' THEN value END) as vit_bmi
    FROM raw_observations
    GROUP BY patient_id
),
-- Conditions
conditions AS (
    SELECT 
        patient_id,
        MAX(CASE WHEN description ILIKE '%diabetes%' THEN 1 ELSE 0 END) as cond_diabetes,
        MAX(CASE WHEN description ILIKE '%hypertension%' THEN 1 ELSE 0 END) as cond_hypertension,
        MAX(CASE WHEN description ILIKE '%heart failure%' OR description ILIKE '%chf%' THEN 1 ELSE 0 END) as cond_chf,
        MAX(CASE WHEN description ILIKE '%copd%' OR description ILIKE '%chronic obstructive%' THEN 1 ELSE 0 END) as cond_copd,
        MAX(CASE WHEN description ILIKE '%chronic kidney%' OR description ILIKE '%ckd%' THEN 1 ELSE 0 END) as cond_ckd,
        MAX(CASE WHEN description ILIKE '%cancer%' OR description ILIKE '%malignancy%' THEN 1 ELSE 0 END) as cond_cancer,
        COUNT(*) as num_conditions
    FROM raw_conditions
    GROUP BY patient_id
),
-- Medications
medications AS (
    SELECT 
        patient_id,
        MAX(CASE WHEN description ILIKE '%insulin%' THEN 1 ELSE 0 END) as med_insulin,
        MAX(CASE WHEN description ILIKE '%metformin%' THEN 1 ELSE 0 END) as med_metformin,
        MAX(CASE WHEN description ILIKE '%statin%' OR description ILIKE '%atorvastatin%' THEN 1 ELSE 0 END) as med_statin,
        MAX(CASE WHEN description ILIKE '%lisinopril%' OR description ILIKE '%enalapril%' THEN 1 ELSE 0 END) as med_ace_inhibitor,
        MAX(CASE WHEN description ILIKE '%metoprolol%' OR description ILIKE '%atenolol%' THEN 1 ELSE 0 END) as med_beta_blocker,
        COUNT(*) as num_medications,
        CASE WHEN COUNT(*) >= 5 THEN 1 ELSE 0 END as polypharmacy
    FROM raw_medications
    GROUP BY patient_id
),
-- Labs - FIXED CODES
labs AS (
    SELECT 
        patient_id,
        AVG(CASE WHEN code = '2339-0' THEN value END) as lab_glucose,
        AVG(CASE WHEN code = '4548-4' THEN value END) as lab_hba1c,
        AVG(CASE WHEN code = '38483-4' THEN value END) as lab_creatinine,
        AVG(CASE WHEN code = '2093-3' THEN value END) as lab_cholesterol,
        AVG(CASE WHEN code = '18262-6' THEN value END) as lab_ldl,
        AVG(CASE WHEN code = '2085-9' THEN value END) as lab_hdl
    FROM raw_observations
    GROUP BY patient_id
)
SELECT 
    pb.patient_id,
    pb.age,
    pb.gender_male,
    pb.gender_female,
    pb.race_white,
    pb.race_black,
    pb.race_asian,
    pb.ethnicity_hispanic,
    COALESCE(r.label_readmission, 0) as label_readmission,
    COALESCE(v.vit_sys_bp, 0) as vit_sys_bp,
    COALESCE(v.vit_dia_bp, 0) as vit_dia_bp,
    COALESCE(v.vit_heart_rate, 0) as vit_heart_rate,
    COALESCE(v.vit_resp_rate, 0) as vit_resp_rate,
    COALESCE(v.vit_temp, 0) as vit_temp,
    COALESCE(v.vit_weight, 0) as vit_weight,
    COALESCE(v.vit_height, 0) as vit_height,
    COALESCE(v.vit_bmi, 0) as vit_bmi,
    COALESCE(c.cond_diabetes, 0) as cond_diabetes,
    COALESCE(c.cond_hypertension, 0) as cond_hypertension,
    COALESCE(c.cond_chf, 0) as cond_chf,
    COALESCE(c.cond_copd, 0) as cond_copd,
    COALESCE(c.cond_ckd, 0) as cond_ckd,
    COALESCE(c.cond_cancer, 0) as cond_cancer,
    COALESCE(c.num_conditions, 0) as num_conditions,
    COALESCE(m.med_insulin, 0) as med_insulin,
    COALESCE(m.med_metformin, 0) as med_metformin,
    COALESCE(m.med_statin, 0) as med_statin,
    COALESCE(m.med_ace_inhibitor, 0) as med_ace_inhibitor,
    COALESCE(m.med_beta_blocker, 0) as med_beta_blocker,
    COALESCE(m.num_medications, 0) as num_medications,
    COALESCE(m.polypharmacy, 0) as polypharmacy,
    COALESCE(l.lab_glucose, 0) as lab_glucose,
    COALESCE(l.lab_hba1c, 0) as lab_hba1c,
    COALESCE(l.lab_creatinine, 0) as lab_creatinine,
    COALESCE(l.lab_cholesterol, 0) as lab_cholesterol,
    COALESCE(l.lab_ldl, 0) as lab_ldl,
    COALESCE(l.lab_hdl, 0) as lab_hdl
FROM patient_base pb
LEFT JOIN readmissions r ON pb.patient_id = r.patient_id
LEFT JOIN vitals v ON pb.patient_id = v.patient_id
LEFT JOIN conditions c ON pb.patient_id = c.patient_id
LEFT JOIN medications m ON pb.patient_id = m.patient_id
LEFT JOIN labs l ON pb.patient_id = l.patient_id;

CREATE INDEX idx_dataset_final_patient ON dataset_final(patient_id);

-- Statistics
SELECT 
    'Total patients' as metric,
    COUNT(*)::text as value,
    '' as details
FROM dataset_final
UNION ALL
SELECT 
    'With readmissions',
    SUM(label_readmission)::text,
    ROUND(100.0 * SUM(label_readmission) / COUNT(*), 2)::text || '%'
FROM dataset_final
UNION ALL
SELECT
    'With vitals (any)',
    COUNT(CASE WHEN vit_heart_rate > 0 OR vit_weight > 0 OR vit_height > 0 OR vit_bmi > 0 THEN 1 END)::text,
    ''
FROM dataset_final
UNION ALL
SELECT
    'With conditions',
    COUNT(CASE WHEN num_conditions > 0 THEN 1 END)::text,
    ''
FROM dataset_final
UNION ALL
SELECT
    'With medications',
    COUNT(CASE WHEN num_medications > 0 THEN 1 END)::text,
    ''
FROM dataset_final;

\echo '=== ✅ Complete dataset built! Export with: ==='
\echo '\\COPY dataset_final TO ''../dataset_structured.csv'' CSV HEADER'
