-- view research results for each (biomarker, disease) pairing
-- [cursor made baseline -- needs to be reviewed]
SELECT
  Research_Studies.Research_Study_ID,
  Research_Studies.URI,
  Disease_Profiles.Disease_Name,
  Biomarkers.Biomarker_Name,
  Disease_Profiles.DISEASE_PROFILE_ID,
  Research_Results.Biomarker_ID,
  Biomarkers.Unit_Measurement,
  Research_Results.Upper_Limit,
  Research_Results.Lower_Limit,
  Research_Results.Population_Size,
  Research_Results.P_Value,
  Research_Results.Confidence_Score
FROM {{ref('stg_zp_dim_research_studies')}} AS Research_Studies
INNER JOIN {{ref('stg_zp_dim_disease_profiles')}} AS Disease_Profiles
  ON Research_Studies.Disease_Profile_ID = Disease_Profiles.DISEASE_PROFILE_ID
INNER JOIN {{ref('stg_zp_fct_research_results')}} AS Research_Results
  ON Research_Studies.Research_Study_ID = Research_Results.Research_Study_ID
INNER JOIN {{ref('stg_zp_dim_biomarkers')}} AS Biomarkers
  ON Research_Results.Biomarker_ID = Biomarkers.Biomarker_ID
