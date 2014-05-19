'''
Created on May 19, 2014

@author: ERIC
'''
import sqlite3 as lite
import sys, datetime, shutil, os
import Parameters

def DatabaseBackup():
    if not os.path.exists(Parameters.BACKUP_DIR):
        os.mkdir(Parameters.BACKUP_DIR)
        
    backupdir = Parameters.BACKUP_DIR + 'backup_' + str(datetime.date.today()) + '/'    
    if not os.path.exists(backupdir):
        os.mkdir(backupdir)
        
    curtime = str(datetime.datetime.now())        
    backup = backupdir + curtime[curtime.index(' ') + 1:curtime.index('.')].replace(':','-') + ".db"
    print(backup)
    shutil.copyfile(Parameters.DICT_DB, backup)

class PeruDB:
    
    con = None
    
    def __init__(self):
        self.openDB()
    
    def openDB(self):
        try:
            self.con = lite.connect(Parameters.DICT_DB)
            cur = self.con.cursor()
            cur.execute('SELECT SQLITE_VERSION()')
            data = cur.fetchone()
    
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        
    
    def closeDB(self):        
        if self.con:
            self.con.close()

    def commit(self):
        if self.con:
            self.con.commit()
    
    def rollback(self):
        if self.con:
            self.con.rollback()
    
    def querry(self, querryString):
        try:
            cur = self.con.cursor()
            cur.execute(querryString)
            return [0, cur.fetchall()]
        
        except lite.Error, e:
            return [1, "Error %s:" % e.args[0]]
            
        except:
            return [1, "Unexpected Error!"]

    def executeCommand(self, commandString):
        try:
            cur = self.con.cursor()
            cur.execute(commandString)
            return[0, cur.lastrowid]
        
        except lite.Error, e:
            return [1, "Error %s:" % e.args[0]]

    def insert(self, commandString):
        return self.executeCommand(commandString)            

    def update(self, commandString):
        return self.executeCommand(commandString)

    def delete(self, commandString):
        return self.executeCommand(commandString)
