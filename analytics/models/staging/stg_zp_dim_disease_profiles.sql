select
  DISEASE_PROFILE_ID,
  NAME as Disease_Name,
  LAST_REVIEWED
from {{source('zp', 'dim_disease_profiles')}}
