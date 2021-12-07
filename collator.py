import csv
import sys

#Data schema
#
# snapshot = (power, kills, dead)
#
#Governor:
#   snapshot0 - Before_First_War
#   snapshot1 - First_War
#   snapshot2 - First_War_Continued
#   snapshot3 - Before_Second_War
#   snapshot4 - After_Second_War

stats = {}
Snapshot = namedtuple('Snapshot', 'power kills dead')

def readOriginalData(csvFile):
     with open(sys.argv[1]) as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            next(reader, None)
            stats[row[0]] = Snapshot(int(row[1]), int(row[3]), int(row[2]))
    return stats
    
def readIncrementalData(csvFile):
    pass

def readData(inFile):
    pass

def writeData(stats, outFile):
    pass