-- Per pathloss bin calculation of the success rate in connection set up.
-- Uses inverse of variance to weight the values

SELECT * FROM OpenQuery(ENIQ, 'SELECT 
			CAST(SUM(rrc_succ_0 / pathloss_deviation) / SUM(rrc_att_0 / pathloss_deviation) as Decimal(20, 10)) as rrc_0,
			CAST(SUM(rrc_succ_1 / pathloss_deviation) / SUM(rrc_att_1 / pathloss_deviation) as Decimal(20, 10)) as rrc_1,
			CAST(SUM(rrc_succ_2 / pathloss_deviation) / SUM(rrc_att_2 / pathloss_deviation) as Decimal(20, 10)) as rrc_2,
			CAST(SUM((rrc_succ_0 + rrc_succ_1 + rrc_succ_2) / pathloss_deviation) / SUM((rrc_att_2 + rrc_att_1 + rrc_att_0) / pathloss_deviation) as Decimal(20, 10)) as rrc_total,

			CAST(SUM(setup_succ_0 / pathloss_deviation) / SUM(setup_att_0 / pathloss_deviation) as Decimal(20, 10)) as setup_0,
			CAST(SUM(setup_succ_1 / pathloss_deviation) / SUM(setup_att_1 / pathloss_deviation) as Decimal(20, 10)) as setup_1,
			CAST(SUM(setup_succ_2 / pathloss_deviation) / SUM(setup_att_2 / pathloss_deviation) as Decimal(20, 10)) as setup_2,
			CAST(SUM((setup_succ_0 + setup_succ_1 + setup_succ_2) / pathloss_deviation) / SUM((setup_att_1 + setup_att_0 + setup_att_2) / pathloss_deviation) as Decimal(20, 10)) as setup_total,

			floor(pathloss_average * 5) / 5 as bin, 
			count(*) as frequency FROM
		(SELECT 
		
		MAX(CASE WHEN DCVECTOR_INDEX = 0 THEN pmRrcConnEstabAttCe ELSE 0 END) as rrc_att_0,
		MAX(CASE WHEN DCVECTOR_INDEX = 1 THEN pmRrcConnEstabAttCe ELSE 0 END) as rrc_att_1,
		MAX(CASE WHEN DCVECTOR_INDEX = 2 THEN pmRrcConnEstabAttCe ELSE 0 END) as rrc_att_2,

		MAX(CASE WHEN DCVECTOR_INDEX = 0 THEN pmRrcConnEstabSuccCe ELSE 0 END) as rrc_succ_0,
		MAX(CASE WHEN DCVECTOR_INDEX = 1 THEN pmRrcConnEstabSuccCe ELSE 0 END) as rrc_succ_1,
		MAX(CASE WHEN DCVECTOR_INDEX = 2 THEN pmRrcConnEstabSuccCe ELSE 0 END) as rrc_succ_2,

		MAX(CASE WHEN DCVECTOR_INDEX = 0 THEN pmRaSuccNbCbra ELSE 0 END) as setup_succ_0,
		MAX(CASE WHEN DCVECTOR_INDEX = 1 THEN pmRaSuccNbCbra ELSE 0 END) as setup_succ_1,
		MAX(CASE WHEN DCVECTOR_INDEX = 2 THEN pmRaSuccNbCbra ELSE 0 END) as setup_succ_2,

		MAX(CASE WHEN DCVECTOR_INDEX = 0 THEN pmRaMsg3SingleToneDistr + pmRaMsg3SixToneDistr + pmRaMsg3ThreeToneDistr + pmRaMsg3TwelveToneDistr
 ELSE 0 END) as setup_att_0,
		MAX(CASE WHEN DCVECTOR_INDEX = 1 THEN pmRaMsg3SingleToneDistr + pmRaMsg3SixToneDistr + pmRaMsg3ThreeToneDistr + pmRaMsg3TwelveToneDistr
 ELSE 0 END) as setup_att_1,
		MAX(CASE WHEN DCVECTOR_INDEX = 2 THEN pmRaMsg3SingleToneDistr + pmRaMsg3SixToneDistr + pmRaMsg3ThreeToneDistr + pmRaMsg3TwelveToneDistr
 ELSE 0 END) as setup_att_2,

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
		GROUP BY floor(pathloss_average * 5) / 5')
WHERE bin >= 104