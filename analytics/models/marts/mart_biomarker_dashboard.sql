-- [cursor made baseline -- needs to be reviewed]
with biomarker_stats as (
  select
    b.Biomarker_ID,
    b.Biomarker_Name,
    b.Unit_Measurement,
    count(distinct dc.Data_Collected_ID) as Measurement_Count,
    count(distinct e.Member_ID) as Patient_Count,
    min(dc.Value) as Min_Value,
    max(dc.Value) as Max_Value,
    avg(dc.Value) as Avg_Value,
    percentile_cont(0.5) within group (order by dc.Value) as Median_Value,
    stddev(dc.Value) as Std_Dev_Value,
    rr.Lower_Limit,
    rr.Upper_Limit,
    count(case when dc.Value < rr.Lower_Limit then 1 end) as Below_Range_Count,
    count(case when dc.Value between rr.Lower_Limit and rr.Upper_Limit then 1 end) as Within_Range_Count,
    count(case when dc.Value > rr.Upper_Limit then 1 end) as Above_Range_Count
  from {{ref('stg_zp_dim_biomarkers')}} as b
  left join {{ref('stg_zp_fct_data_collected')}} as dc
    on b.Biomarker_ID = dc.Biomarker_ID
  left join {{ref('stg_zp_fct_examinations')}} as e
    on dc.Examination_ID = e.Examination_ID
  left join {{ref('stg_zp_fct_research_results')}} as rr
    on b.Biomarker_ID = rr.Biomarker_ID
  group by
    b.Biomarker_ID,
    b.Biomarker_Name,
    b.Unit_Measurement,
    rr.Lower_Limit,
    rr.Upper_Limit
)

select
  bs.*,
  case
    when bs.Patient_Count > 0 then
      (bs.Below_Range_Count + bs.Above_Range_Count) / bs.Patient_Count
    else 0
  end as Abnormal_Rate
from biomarker_stats bs
