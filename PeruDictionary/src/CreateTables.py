#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import Parameters

try:
  
    con = lite.connect(Parameters.DICT_DB)
    
    cur = con.cursor()
    cur.executescript(""" 
        
        DROP TABLE IF EXISTS Entry;
        
        CREATE TABLE Entry(EntryId           INTEGER PRIMARY KEY, 
                           Word              TEXT,
                           Source            TEXT,
                           Definition        TEXT,
                           Notes             TEXT)        
        """)
    
    con.commit()
    
except lite.Error as e:
  
    if con:
        con.rollback()
      
    print("Error %s:" % e.args[0])
    sys.exit(1)

finally:
  
    if con:
        con.close()
    
  
