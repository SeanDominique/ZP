select
  MEDICAL_DEVICE_ID,
  NAME as Device_Name,
  LAST_SERVICED as Last_Service_Date,
  PURCHASED_DATE
from {{source('zp', 'dim_medical_devices')}}
