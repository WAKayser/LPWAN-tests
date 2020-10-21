-- Simple average of usage of PRBs
-- Formula does not allow to measure values below 5 percent occupancy.
-- NB-IoT does allow this due to a bug/undocumented feature in the software.

SELECT * FROM OpenQuery(ENIQ, 'SELECT 
	CAST(AVG(usage_dl) as Decimal(20, 10)) as use_dl,
	CAST(AVG(usage_ul) as Decimal(20, 10)) as use_ul,
	HOUR_ID,
	MIN_ID 
	FROM (
		SELECT 
			CAST(SUM(pmPrbUtilUl * (5 + DCVECTOR_INDEX * 10)) / SUM(pmPrbUtilUl) as Decimal(20,10)) as usage_ul,
			CAST(SUM(pmPrbUtilDl * (5 + DCVECTOR_INDEX * 10)) / SUM(pmPrbUtilDl) as Decimal(20,10)) as usage_dl,
			HOUR_ID,
			MIN_ID
			FROM DC.DC_E_ERBS_EUTRANCELLFDD_V_RAW
			GROUP BY HOUR_ID, MIN_ID, EUTRANCELLFDD	
	) as inter
	GROUP BY HOUR_ID, MIN_ID')