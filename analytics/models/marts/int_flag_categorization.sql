-- basic version of biomarker value flagging. Later versions will implement more advanced algorithms to detect if a biomarker value is at risk

-- TODO: when you have collected statistical values from multiple research papers then it would make sense to calculate an aggregated mean and std for each biomarker (probably)
WITH Research_Statistics AS (
  SELECT
      Biomarker_ID,
      Upper_Limit,
      Lower_Limit,
      (Upper_Limit + Lower_Limit) / 2 AS Mean,
      (Upper_Limit - Lower_Limit) / 4 AS Standard_Deviation -- Assuming range covers roughly 4 std deviations
  FROM FACT_RESEARCH_RESULTS
),
Boundaries AS (
    SELECT
      Biomarker_ID,
      Upper_Limit,
      Lower_Limit,
      (Upper_Limit - Standard_Deviation) / 2 AS Orange_Upper,
      (Lower_Limit + Standard_Deviation) / 2 AS Orange_Lower
    FROM Research_Statistics
)

SELECT
  Data_Collected.Biomarker_ID,
  Biomarkers.Biomarker_Name,
  Data_Collected.Value,
  CASE
    WHEN (Data_Collected.Value > Boundaries.Upper_Limit)
          OR (Data_Collected.Value < Boundaries.Lower_Limit) THEN 2 -- value for Red flag
    WHEN (Data_Collected.Value > Boundaries.Orange_Upper)
          OR (Data_Collected.Value < Boundaries.Orange_Lower) THEN 1 -- value for Orange flag
    ELSE 0 -- value for Green flag
    END AS Risk_Flag
FROM FACT_DATA_COLLECTED AS Data_Collected
JOIN DIM_BIOMARKERS AS Biomarkers ON Biomarkers.Biomarker_ID = Data_Collected.Biomarker_ID
JOIN Boundaries ON Boundaries.Biomarker_ID = Data_Collected.Biomarker_ID
