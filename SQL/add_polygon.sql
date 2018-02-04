INSERT INTO S1138056.PIRATE_OBJECTS VALUES(
/*Polygon addtion to Pirate_objects*/
  &ObjID,
  MDSYS.SDO_GEOMETRY(
    2003,  
    NULL,
    NULL,
    MDSYS.SDO_ELEM_INFO_ARRAY(1,1003,1), 
    MDSYS.SDO_ORDINATE_ARRAY(&PolyCoords)
  ),
  1, -- island are 1
  10 -- Sanpattern for island
);