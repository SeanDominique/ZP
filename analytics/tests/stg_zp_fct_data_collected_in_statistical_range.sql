select *
from {{source('zp', 'fact_data_collected')}} as Data_Collected
join {{source('zp', 'fact_research_results')}} as Research_Results
  on Data_Collected.BIOMARKER_ID = Research_Results.BIOMARKER_ID
where NOT Data_Collected.VALUE BETWEEN Research_Results.LOWER_LIMIT AND Research_Results.UPPER_LIMIT
