-- Per pathloss bin calculation of the success rate in transmissions
-- Uses inverse of variance to weight the values

SELECT * FROM OpenQuery(ENIQ, 'SELECT 
			CAST(SUM(dl_succ_0 / pathloss_deviation) / SUM((dl_succ_0 + dl_fail_0) / pathloss_deviation) as Decimal(20, 10)) as dl_0,
			CAST(SUM(dl_succ_1 / pathloss_deviation) / SUM((dl_succ_1 + dl_fail_1) / pathloss_deviation) as Decimal(20, 10)) as dl_1,
			CAST(SUM(dl_succ_2 / pathloss_deviation) / SUM((dl_succ_2 + dl_fail_2) / pathloss_deviation) as Decimal(20, 10)) as dl_2,
			CAST(SUM((dl_succ_0 + dl_succ_1 + dl_succ_2) / pathloss_deviation) / SUM(((dl_succ_0 + dl_succ_1 + dl_succ_2) + (dl_fail_0 + dl_fail_1 + dl_fail_2)) / pathloss_deviation) as Decimal(20, 10)) as dl_total,

			CAST(SUM(ul_succ_0 / pathloss_deviation) / SUM((ul_succ_0 + ul_fail_0) / pathloss_deviation) as Decimal(20, 10)) as ul_0,
			CAST(SUM(ul_succ_1 / pathloss_deviation) / SUM((ul_succ_1 + ul_fail_1) / pathloss_deviation) as Decimal(20, 10)) as ul_1,
			CAST(SUM(ul_succ_2 / pathloss_deviation) / SUM((ul_succ_2 + ul_fail_2) / pathloss_deviation) as Decimal(20, 10)) as ul_2,
			CAST(SUM((ul_succ_0 + ul_succ_1 + ul_succ_2) / pathloss_deviation) / SUM(((ul_succ_0 + ul_succ_1 + ul_succ_2) + (ul_fail_0 + ul_fail_1 + ul_fail_2)) / pathloss_deviation) as Decimal(20, 10)) as ul_total,

			floor(pathloss_average) as bin
			FROM
		(SELECT 
		
		MAX(CASE WHEN DCVECTOR_INDEX = 0 THEN pmMacHarqDlNackQpskCe ELSE 0 END) as dl_fail_0,
		MAX(CASE WHEN DCVECTOR_INDEX = 1 THEN pmMacHarqDlNackQpskCe ELSE 0 END) as dl_fail_1,
		MAX(CASE WHEN DCVECTOR_INDEX = 2 THEN pmMacHarqDlNackQpskCe ELSE 0 END) as dl_fail_2,

		MAX(CASE WHEN DCVECTOR_INDEX = 0 THEN pmMacHarqDlAckQpskCe ELSE 0 END) as dl_succ_0,
		MAX(CASE WHEN DCVECTOR_INDEX = 1 THEN pmMacHarqDlAckQpskCe ELSE 0 END) as dl_succ_1,
		MAX(CASE WHEN DCVECTOR_INDEX = 2 THEN pmMacHarqDlAckQpskCe ELSE 0 END) as dl_succ_2,

		MAX(CASE WHEN DCVECTOR_INDEX = 0 THEN pmMacHarqUlSuccQpskCe + pmMacHarqUlSuccBpskCe ELSE 0 END) as ul_succ_0,
		MAX(CASE WHEN DCVECTOR_INDEX = 1 THEN pmMacHarqUlSuccQpskCe + pmMacHarqUlSuccBpskCe ELSE 0 END) as ul_succ_1,
		MAX(CASE WHEN DCVECTOR_INDEX = 2 THEN pmMacHarqUlSuccQpskCe + pmMacHarqUlSuccBpskCe ELSE 0 END) as ul_succ_2,

		MAX(CASE WHEN DCVECTOR_INDEX = 0 THEN pmMacHarqUlFailQpskCe + pmMacHarqUlFailBpskCe ELSE 0 END) as ul_fail_0,
		MAX(CASE WHEN DCVECTOR_INDEX = 1 THEN pmMacHarqUlFailQpskCe + pmMacHarqUlFailBpskCe ELSE 0 END) as ul_fail_1,
		MAX(CASE WHEN DCVECTOR_INDEX = 2 THEN pmMacHarqUlFailQpskCe + pmMacHarqUlFailBpskCe ELSE 0 END) as ul_fail_2,

		CAST(SUM(pmUlPathlossNbDistr * CASE
			WHEN DCVECTOR_INDEX = 0 THEN 50
			WHEN DCVECTOR_INDEX = 24 THEN 165
			ELSE 47.5 + (5 * DCVECTOR_INDEX)
		END) / SUM(pmUlPathlossNbDistr) as Decimal(20,10)) as pathloss_average,

		SQRT(
		SUM(pmUlPathlossNbDistr * POWER(CASE   -- This should be E[x^2]
			WHEN DCVECTOR_INDEX = 0 THEN 50
			WHEN DCVECTOR_INDEX = 24 THEN 165
			ELSE 47.5 + (5 * DCVECTOR_INDEX)
		END, 2)) / SUM(pmUlPathlossNbDistr) - 

		POWER(SUM(pmUlPathlossNbDistr * CASE -- this is E[x]^2
			WHEN DCVECTOR_INDEX = 0 THEN 50
			WHEN DCVECTOR_INDEX = 24 THEN 165
			ELSE 47.5 + (5 * DCVECTOR_INDEX)
		END) / SUM(pmUlPathlossNbDistr), 2)
		) as pathloss_deviation
		
		FROM dc.DC_E_ERBS_NBIOTCELL_V_RAW
		GROUP BY nbiotcell, datetime_id) as data
		GROUP BY floor(pathloss_average)')
WHERE bin >= 104