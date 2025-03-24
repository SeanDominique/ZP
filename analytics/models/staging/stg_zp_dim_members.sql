select
  Member_ID,
  Full_Name,
  Date_Registered,
  Is_Active,
  Sex,
  DOB as Date_of_Birth
from {{source('zp', 'dim_members')}}
