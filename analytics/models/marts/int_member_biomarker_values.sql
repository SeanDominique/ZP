-- all member biomarker values ordered by examination date (DESC) and member name (ASC)
SELECT
  MEMBERS.Full_Name,
  BIOMARKERS.Biomarker_ID,
  BIOMARKERS.Biomarker_Name,
  BIOMARKERS.Unit_Measurement,
  EXAMINATIONS.Examination_Date,
  DATA_COLLECTED.Value,
  MEMBERS.Member_ID,
  EXAMINATIONS.Examination_ID,
  EXAMINATIONS.CLINICIAN_ID
FROM {{ref('stg_zp_fct_data_collected')}} AS DATA_COLLECTED
INNER JOIN {{ref('stg_zp_dim_biomarkers')}} AS BIOMARKERS
  ON DATA_COLLECTED.Biomarker_ID = BIOMARKERS.Biomarker_ID
INNER JOIN {{ref('stg_zp_fct_examinations')}} AS EXAMINATIONS
  ON DATA_COLLECTED.Examination_ID = EXAMINATIONS.Examination_ID
INNER JOIN {{ref('stg_zp_dim_members')}} AS MEMBERS
  ON EXAMINATIONS.Member_ID = MEMBERS.Member_ID
ORDER BY EXAMINATIONS.Date DESC, MEMBERS.Full_Name ASC
