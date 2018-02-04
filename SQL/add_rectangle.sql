INSERT INTO S1138056.PIRATE_OBJECTS VALUES(
/*Rectangle addtion to Pirate_objects*/
  &ObjID,
  MDSYS.SDO_GEOMETRY(
    2003,  
    NULL,
    NULL,
    MDSYS.SDO_ELEM_INFO_ARRAY(1,1003,3), --array [3] has to be 3(square rectangle)
    MDSYS.SDO_ORDINATE_ARRAY(&x1, &y1, &x2, &y2)--- bottom left coord and top right coord
  ),
  2, -- rectangle are icons
  &Selectbetween1and8 -- SVG shape
);