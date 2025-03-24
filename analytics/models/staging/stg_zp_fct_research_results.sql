select
  Research_Result_ID,
  Upper_Limit,
  Lower_Limit,
  Population_Size,
  P_Value,
  Confidence_Score,
  Biomarker_ID,
  Research_Study_ID
from {{source('zp', 'fact_research_results')}}
