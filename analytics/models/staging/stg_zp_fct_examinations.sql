select
  Examination_ID,
  Member_ID,
  Examinations.Date AS Examination_Date,
  Clinician_ID
from {{source('zp', 'fact_examinations')}} as Examinations
