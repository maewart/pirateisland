INSERT INTO PIRATE_LEVELS VALUES(
		'&LevID',
		'&Level_name',
		MDSYS.SDO_GEOMETRY(
			2001,
			NULL,
			MDSYS.SDO_POINT_TYPE('&start_X', '&start_Y', NULL),
			NULL,
			NULL
		),
		MDSYS.SDO_GEOMETRY(
			2003,
			NULL,
			NULL,
			MDSYS.SDO_ELEM_INFO_ARRAY(1, 1003, 3),
			MDSYS.SDO_ORDINATE_ARRAY(0,0,20,20)
		)
	)
	/
