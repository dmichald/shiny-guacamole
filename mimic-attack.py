import random

class LogRecord:
    def __init__(self,time,duration,srcDevice,dstDevice,protocol,srcPort,dstPort,srcPackets,dstPackets,srcBytes,dstBytes):
        self.time = time
        self.duration = duration
        self.srcDevice = srcDevice
        self.dstDevice = dstDevice
        self.protocl = protocol
        self.srcPort = srcPort
        self.dstPort = dstPort
        self.srcPackets = srcPackets
        self.dstPackets = dstPackets
        self.srcBytes = srcBytes
        self.dstPackets = dstBytes
    
    def toString(self):
        list = []
        list.append(self.time)
        list.append(self.duration)
        list.append(self.srcDevice)
        list.append(self.dstDevice)
        list.append(self.protocl)
        list.append(self.srcPort)
        list.append(self.dstPort)
        list.append(self.srcPackets)
        list.append(self.dstPackets)
        list.append(self.srcBytes)
        list.append(self.dstPackets)
        stringList = [str(el) for el in list]
        string = ','.join(stringList)
        return string + " generated" + "\n" 
            
    
def getHeadOfFile(filePath, numberOfLines):
    with open(filePath) as myfile:
        head = [next(myfile) for x in range(numberOfLines)]
        return head

def writeToFile(path, data):
    with open(path, 'w') as f:
         f.writelines(data)

def generateDdosRecords(startTime,endTime,amount):
    step = (endTime - startTime )/amount
    duration = 2
    time = startTime
    dstDevice = 'EnterpriseAppServer'
    udpProtocol = 17
    dstPort = 1433 # sql server connection
    
    fakeData = []
    
    for i in range(amount):
        srcDevice = "IP4" + str(random.randrange(202946,902946))
        srcPOrt = "Port" + str(random.randrange(10,65533))
        srcPackets = str(random.randrange(2,10))
        dstPackets = 0
        srcBytes =  65535
        dstBytes = 0
        time = time + step
        logRecord = LogRecord(int(time),duration, srcDevice,dstDevice,udpProtocol,srcPOrt,dstPort,srcPackets,dstPackets,srcBytes,dstBytes)
        
        if(i % 1000 == 0):
            duration = duration + 10
            
        fakeData.append(logRecord)
    
    return fakeData

def combineLists(org, toInsert):
    orgSize = len(org)
    toInsertSize = len(toInsert)
    newList = []
    i,j = 0,0
    
    while i < orgSize and j < toInsertSize:
        orgTime = int(org[i].split(",")[0])
        generatedRecordTime = int(toInsert[j].time)
        if(generatedRecordTime > orgTime):
            newList.append(org[i])
            i += 1
    
        else:
            newList.append(toInsert[j].toString())
            j += 1
    newList = newList + org[i:]
        
    for x in range(j,toInsertSize):
        newList.append(toInsert[x].toString())
    return newList
    
def removeRecordsAfterAttack(lines, attackEndTime):
    newLines = []
    for line in lines:
        time = int(line.split(",")[0])
        srcDevice = line.split(",")[2]
        if(time > attackEndTime and srcDevice =="EnterpriseAppServer"):
            continue
        else:
            newLines.append(line)
    
    return newLines
        
filePath = r'C:\Users\Michal\Downloads\netflow\netflow_day-02'
outputFilePath = r'C:\Users\Michal\Downloads\netflow\gen.txt'
data = getHeadOfFile(filePath, 1000000)

genData = generateDdosRecords(118781,120973,100000)
combinedLists = combineLists(data,genData)
finalList = removeRecordsAfterAttack(combinedLists,120973)
writeToFile(outputFilePath,finalList)