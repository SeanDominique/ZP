select
  CLINICIAN_ID,
  FULL_NAME,
  IS_ZOI_ONBOARDING_COMPLETE as Onboarding_Complete_Date
from {{source('zp', 'dim_clinicians')}}
