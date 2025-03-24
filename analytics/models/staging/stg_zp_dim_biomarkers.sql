select
  Biomarker_ID,
  Biomarker_Name,
  Unit_Measurement
from {{source('zp', 'dim_biomarkers')}}
