-- SQL query used to find the average payload size for LTE in different areas

SELECT location, size, sum(count_s) as frequency FROM 
	(SELECT 
		IIF(size > 0, size, 0) as size, sum(count_s) as count_s, location
	FROM OpenQuery(Eniq,'SELECT
			cast(FLOOR( 4 * cast(pmRadioThpVolUl + pmRadioThpVolDl as Decimal(20, 9)) / cast(pmS1SigConnEstabSucc as Decimal(20,9))) * 32 - 64 as Decimal(20, 0)) as size,
			count(*) as count_s,
			erbs
		FROM dc.DC_E_ERBS_EUTRANCELLFDD_RAW 
			WHERE pmS1SigConnEstabSucc > 0
			AND size is not NULL
		GROUP BY size, erbs') as data
	INNER JOIN (SELECT distinct(RBSName), 
	CASE
		WHEN (Lat > 52.27 and Lat < 52.43 and Lon > 4.76 and Lon < 5.01) THEN 'Amsterdam'
		WHEN (Lat > 51.83 and Lat < 51.97 and Lon > 4.32 and Lon < 4.62) THEN 'Rotterdam'
		WHEN (Lat > 51.99 and Lat < 52.17 and Lon > 4.97 and Lon < 5.22) THEN 'Utrecht'
		WHEN (Lat > 52.30 and Lat < 52.42 and Lon > 5.12 and Lon < 5.39) THEN 'Almere'
		WHEN (Lat > 51.23 and Lat < 51.78 and Lon > 4.65 and Lon < 5.81) THEN 'Brabant'
		WHEN (Lat > 52.55 and Lon > 5.28) THEN 'Friesland, Groningen en Drenthe'
		ELSE 'Rest' 
	END as location
	FROM CM_DB.dbo.tCellID_CellName_LAC_TAC_XY) as locs
	ON data.erbs = locs.RBSName
	GROUP BY size, location) as intermediate
GROUP BY size, location
ORDER BY size, location
