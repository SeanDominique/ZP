select
  DIM_MEMBERS."Full_Name",
  DIM_BIOMARKERS."Biomarker_ID",
  FACT_EXAMINATIONS."Date",
  FACT_DATA_COLLECTED."Value",
  DIM_MEMBERS."Member_ID",
  FACT_EXAMINATIONS."Examination_ID"
from {{ref('stg_zp_fct_data_collected')}} as FCT_DATA_COLLECTED
inner join {{ref('stg_zp_dim_biomarkers')}} as DIM_BIOMARKERS
  on FCT_DATA_COLLECTED."Biomarker_ID" = DIM_BIOMARKERS."Biomarker_ID"
inner join {{ref('stg_zp_fct_examinations')}} as FCT_EXAMINATIONS
  on FCT_DATA_COLLECTED."Examination_ID" = FCT_EXAMINATIONS."Examination_ID"
inner join {{ref('stg_zp_dim_members')}} as DIM_MEMBERS
  on FACT_EXAMINATIONS."Member_ID" = DIM_MEMBERS."Member_ID"
order by FCT_EXAMINATIONS."Date" DESC, DIM_MEMBERS."Full_Name" ASC
