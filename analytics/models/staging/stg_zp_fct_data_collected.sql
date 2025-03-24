select
  Data_Collected_ID,
  Examination_ID,
  Biomarker_ID,
  Medical_Device_ID,
  Value
from {{source('zp', 'fact_data_collected')}}
