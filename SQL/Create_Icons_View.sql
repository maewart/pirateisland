CREATE VIEW PIRATE_ICONS_VIEW
AS  
SELECT m.LEVEL_ID, a.OBJECT_ID,c.FILL_NAME,d.TYPE_NAME, min(b.X) as MIN_X, min(b.Y) as MIN_Y, max(b.X) as MAX_X, max(b.Y) as MAX_Y 
   FROM S1138056.PIRATE_OBJECTS a
   join S1138056.PIRATE_MAPPING m on a.OBJECT_ID = m.OBJECT_ID
   join S1138056.PIRATE_FILL c on a.FILL_ID = c.FILL_ID
   join S1138056.PIRATE_TYPES d on a.TYPE_ID = d.TYPE_ID,
   TABLE(SDO_UTIL.GETVERTICES(a.OBJECT)) b
   Where d.TYPE_NAME != 'island'
   GROUP BY m.LEVEL_ID,a.OBJECT_ID,c.FILL_NAME,d.TYPE_NAME Order by m.LEVEL_ID,a.OBJECT_ID;