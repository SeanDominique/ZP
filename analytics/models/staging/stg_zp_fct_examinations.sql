select
  Examination_ID,
  Member_ID,
  Examination_Date,
  Clinician_ID
from {{source('zp', 'fact_examinations')}}
