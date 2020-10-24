# Author Mark McKinnon
# Email: Mark.McKinnon@gmail.compile
# License: Apache 2.0

import leveldb
import sys
import os
from Database import SQLiteDb

def removeChars(text):
    return ''.join([i if (ord(i) > 31 and ord(i) < 128) else '' for i in text])

args = sys.argv[1:]
if len(args) != 2:
    print ("Wrong Parameters need 2, LevelDB directory and output csv file")
    exit()

levelDbDir = args[0]
outputFile = args[1]

SQLitedb = SQLiteDb()
SQLitedb.RemoveDB_File(outputFile + ".db3")
SQLitedb.Open(outputFile + ".db3")

SQLitedb.CreateTable("Leveldb", 'key text, value text, byte_key text, byte_value text')

try:
    levelDb = leveldb.LevelDB(levelDbDir)
    try:
        print (levelDb.GetStats())
    except:
        print ("No Stats")

    numRecords = 0

    with open(outputFile + ".csv", 'w') as f:
        for key, value in levelDb2.RangeIter():
            key2 = str(key, 'utf-8', 'ignore')
            keyd16 = key.decode('utf-8', "ignore")
            vald16 = value.decode('utf-8', 'ignore')
            newKey = removeChars(keyd16)
            newVal = removeChars(vald16)
            if len(str(newKey)) > 1 and len(str(newVal)) > 1:
                SQLitedb.InsertList("Leveldb", "key, value, byte_key, byte_value", '?, ?, ?, ?', [str(newKey), str(newVal), key, value])
                f.write(str(newKey) + "," + str(newVal) + "\n")
                numRecords = numRecords + 1

    print ("Number of records dumped are ==> " + str(numRecords))
except:
    print ("Attempting to repair DB")
    levelDb = leveldb.RepairDB(levelDbDir)
    levelDb2 = leveldb.LevelDB(os.path.join(levelDbDir, "lost"))
    try:
        print (levelDb2.GetStats())
    except:
        print ("No Stats")
    numRecords = 0  

    with open(outputFile + ".csv", 'w') as f:
        for key, value in levelDb2.RangeIter():
            key2 = str(key, 'utf-8', 'ignore')
            keyd16 = key.decode('utf-8', "ignore")
            vald16 = value.decode('utf-8', 'ignore')
            newKey = removeChars(keyd16)
            newVal = removeChars(vald16)
            if len(str(newKey)) > 1 and len(str(newVal)) > 1:
                SQLitedb.InsertList("Leveldb", "key, value, byte_key, byte_value", '?, ?, ?, ?', [str(newKey), str(newVal), key, value])
                f.write(str(newKey) + "," + str(newVal) + "\n")
                numRecords = numRecords + 1

    print ("Number of records dumped are ==> " + str(numRecords))

SQLitedb.Close()