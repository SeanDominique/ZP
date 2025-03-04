select *
from {{ref('stg_zp_fct_examinations')}}
where "Date" is null
      OR "Date" < '2024-10-01' -- first registration date for members as determined in synthetic data generation function
      OR "Date" > CURRENT_DATE()
