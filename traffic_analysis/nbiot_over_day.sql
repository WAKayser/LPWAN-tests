--  SQL query to find the usage over the day.
-- Some interesting parts are the usage formulas, being the same as in the documentation. 
-- However they show different behavior which allows for more precise measurements. 
-- At moments of inactivity, no update will be given, so not even 0 will be given. 

SELECT * FROM OpenQuery(ENIQ, 'SELECT 

	CAST(AVG(volume_dl) as Decimal(20, 10)) as vol_dl,
	CAST(AVG(volume_ul) as Decimal(20, 10)) as vol_ul,

	CAST(AVG(connections) as Decimal(20, 10)) as con,

	CAST(AVG(usage_dl) as Decimal(20, 10)) as use_dl,
	CAST(AVG(usage_ul) as Decimal(20, 10)) as use_ul,

	CAST(SUM(succ_dl) / SUM(total_dl) as Decimal(20, 10)) as sr_dl,
	CAST(SUM(succ_ul) / SUM(total_ul) as Decimal(20, 10)) as sr_ul,

	CAST(SUM(ra_succ) / SUM(ra_att) as Decimal(20, 10)) as sr_ra,
	CAST(SUM(rrc_conn) / SUM(rrc_att) as Decimal(20, 10)) as sr_rrc,

	HOUR_ID,
	MIN_ID

	FROM
		(SELECT 
			SUM(pmRadioThpVolDlCe) as volume_dl,
			SUM(pmRadioThpVolUlCe) as volume_ul, 

			SUM(pmS1SigConnEstabSuccCe) as connections,

		    CAST(SUM(pmNpuschUtilDistr * (2.5 + DCVECTOR_INDEX * 5)) / 900 as Decimal(20,10)) as usage_ul,
			CAST(SUM((pmNpdcchCceUtil + pmNpdschUtilDistr) * (2.5 + DCVECTOR_INDEX * 5)) / 900 as Decimal(20,10)) as usage_dl,

			SUM(pmMacHarqDlAckQpskCe) as succ_dl,
			SUM(pmMacHarqDlNackQpskCe + pmMacHarqDlAckQpskCe) as total_dl,
			SUM(pmMacHarqUlSuccBpskCe + pmMacHarqUlSuccQpskCe) as succ_ul,
			SUM(pmMacHarqUlFailBpskCe + pmMacHarqUlFailQpskCe + pmMacHarqUlSuccBpskCe + pmMacHarqUlSuccQpskCe) as total_ul,

			SUM(pmRaSuccNBCbra) as ra_att,
			SUM(pmRrcConnEstabAttCe + pmRrcConnEstabAttReattCe) as ra_succ,
			SUM(pmRrcConnEstabAttCe) as rrc_att,
			SUM(pmRrcConnEstabSuccCe) as rrc_conn,

			HOUR_ID, 
			MIN_ID 
			FROM dc.DC_E_ERBS_NBIOTCELL_V_RAW
			GROUP BY nbiotcell, datetime_id, hour_id, min_id
		) as inter_data
	GROUP BY HOUR_ID, MIN_ID
')