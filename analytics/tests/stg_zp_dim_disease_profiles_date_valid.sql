select *
from {{ref('stg_zp_dim_disease_profiles')}}
where LAST_REVIEWED is null
      OR LAST_REVIEWED < CURRENT_DATE() - interval '3 years' -- make sure the disease profile was reviewed less than 3 years ago
      OR LAST_REVIEWED > CURRENT_DATE()
