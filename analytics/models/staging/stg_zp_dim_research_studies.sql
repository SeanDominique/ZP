select
  Research_Study_ID,
  URI,
  Disease_Profile_ID
from {{source('zp', 'dim_research_studies')}}
