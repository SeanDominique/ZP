-- [cursor made baseline -- needs to be reviewed]
with latest_examination as (
  select
    Member_ID,
    max(Examination_Date) as Latest_Examination_Date
  from {{ref('stg_zp_fct_examinations')}}
  group by Member_ID
)

select
  m.Member_ID,
  m.Full_Name,
  m.Date_of_Birth,
  m.Sex,
  m.Date_Registered,
  m.Is_Active,
  le.Latest_Examination_Date,
  count(distinct e.Examination_ID) as Total_Examinations,
  count(distinct dc.Biomarker_ID) as Unique_Biomarkers_Measured,
  -- Count biomarkers by flag category from the latest examination
  sum(case when fc.Flag = 0 then 1 else 0 end) as Green_Biomarkers,
  sum(case when fc.Flag = 1 then 1 else 0 end) as Orange_Biomarkers,
  sum(case when fc.Flag = 2 then 1 else 0 end) as Red_Biomarkers
from {{ref('stg_zp_dim_members')}} as m
left join latest_examination as le
  on m.Member_ID = le.Member_ID
left join {{ref('stg_zp_fct_examinations')}} as e
  on m.Member_ID = e.Member_ID
left join {{ref('stg_zp_fct_data_collected')}} as dc
  on e.Examination_ID = dc.Examination_ID
left join {{ref('int_flag_categorization')}} as fc
  on dc.Biomarker_ID = fc.Biomarker_ID
group by
  m.Member_ID,
  m.Full_Name,
  m.Date_of_Birth,
  m.Sex,
  m.Date_Registered,
  m.Is_Active,
  le.Latest_Examination_Date
