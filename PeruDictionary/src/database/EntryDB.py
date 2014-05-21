import DictDB
import DictConstants

def EntryInsertFromList(entries):
    resultString = ""
    
    for entry in entries:
        result = EntryInsertStatement(entry)
        if result == -1:
            return result
        resultString += result
    
    return resultString

def EntryReadSingleStatement(EntryID):    
    return("SELECT * FROM ENTRY WHERE " + DictConstants.ENTRY_FIELDS[0] + " = '" + str(EntryID) + "';\n")

def EntryReadAllStatement():
    return("SELECT * FROM ENTRY ORDER BY Word")

def EntryInsertStatement(fields):
    
    if len(fields) > len(DictConstants.ENTRY_FIELDS) or len(fields) < (len(DictConstants.ENTRY_FIELDS) - 1):
        return -1
    
    strFields = [str(field) for field in fields]
    
    if len(fields) == (len(DictConstants.ENTRY_FIELDS) - 1):
        return ("INSERT INTO " + DictConstants.ENTRY + 
                "(" + ",".join(DictConstants.ENTRY_FIELDS[1:]) + ")" +
                " VALUES(" + "\',\'".join(strFields) + ");\n")
    else:
        return "INSERT INTO " + DictConstants.ENTRY + " (" + ",".join(DictConstants.ENTRY_FIELDS[1:]) + ")" + " VALUES('" + "','".join(strFields[1:]) + "');\n"

def EntryUpdateStatement(fields):
    
    if len(fields) != len(DictConstants.ENTRY_FIELDS):
        return -1
    
    strFields = [(DictConstants.ENTRY_FIELDS[i] + " = '" + str(fields[i]) + "'")  for i in range(1, len(fields))]
    
    return ("UPDATE ENTRY" +
            " SET " + ",".join(strFields) + 
            " WHERE " + DictConstants.ENTRY_FIELDS[0] + " = " + str(fields[0]) + ";\n")

def EntryDeleteStatement(fields):    
    return("DELETE FROM ENTRY WHERE " + DictConstants.ENTRY_FIELDS[0] + " = " + fields[0] + ";\n")

def ReadEntry(EntryID):
    database = DictDB.DictDB()
    output = database.querry(EntryReadSingleStatement(EntryID));
    database.closeDB()
    return output

def ReadEntries():
    database = DictDB.DictDB()
    output = database.querry(EntryReadAllStatement());
    database.closeDB()
    return output    
    
def InsertUpdateEntry(database, fields):
    if fields[0] != '':
        return UpdateEntry(database, fields)
    else:
        return InsertEntry(database, fields)
        

def InsertEntry(database, fields):
    output = database.insert(EntryInsertStatement(fields))
    return output

def UpdateEntry(database, fields):
    output = database.update(EntryUpdateStatement(fields))
    return output

def DeleteEntry(database, fields):    
    output = database.delete(EntryDeleteStatement(fields))
    return output
