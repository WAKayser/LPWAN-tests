-- Get information on the the KPIs that are not in the vector counters for LTE.
-- NB-IoT has for most counters in the standard tables a version in the vector counters.
-- This allows to differentiate over the CE levels. 

SELECT * FROM OpenQuery(ENIQ, 'SELECT 
	HOUR_ID,
	MIN_ID


	CAST(AVG(vol_dl) as Decimal(20, 10)) as vol_dl,
	CAST(AVG(vol_ul) as Decimal(20, 10)) as vol_ul,

	CAST(AVG(connections) as Decimal(20, 10)) as con,

	CAST(SUM(succ_dl) / SUM(total_dl) as Decimal(20, 10)) as sr_dl,
	CAST(SUM(succ_ul) / SUM(total_ul) as Decimal(20, 10)) as sr_ul,

	CAST(SUM(ra_succ) / SUM(ra_att) as Decimal(20, 10)) as sr_ra,
	CAST(SUM(rrc_conn) / SUM(rrc_att) as Decimal(20, 10)) as sr_rrc,

	FROM
		(SELECT 
			pmRadioThpVolDl as vol_dl,
			pmRadioThpVolUl as vol_ul,
			pmS1SigConnEstabSucc as connections, 
			
			pmMacHarqDlAck16qam + pmMacHarqDlAck256qam + pmMacHarqDlAck64qam + pmMacHarqDlAckQpsk as succ_dl,
			pmMacHarqDlNack16qam+ pmMacHarqDlNack256qam+ pmMacHarqDlNack64qam+ pmMacHarqDlNackQpsk + pmMacHarqDlAck16qam + pmMacHarqDlAck256qam + pmMacHarqDlAck64qam + pmMacHarqDlAckQpsk as total_dl,
			pmMacHarqUlSucc16qam + pmMacHarqUlSucc64Qam + pmMacHarqUlSuccQpsk as succ_ul,
			pmMacHarqUlSucc16qam + pmMacHarqUlSucc64Qam + pmMacHarqUlSuccQpsk + pmMacHarqUlFail16qam + pmMacHarqUlFail64Qam + pmMacHarqUlFailQpsk as total_ul,

			pmRaAttCbra as ra_att,
			pmRaSuccCbra as ra_succ,
			pmRrcConnEstabAtt as rrc_att,
			pmRrcConnEstabSucc as rrc_conn,

			HOUR_ID, 
			MIN_ID 
			FROM dc.DC_E_ERBS_EUTRANCELLFDD_RAW
		) as inter_data
	GROUP BY HOUR_ID, MIN_ID
	')