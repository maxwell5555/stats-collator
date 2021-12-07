import csv
import sys
from collections import namedtuple

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

OldSnapshot = namedtuple('Snapshot', 'power kills dead')
NewSnapshot = namedtuple('NewSnapshot', 'power t4kills t5kills dead')

def findGovernorIDMatchByName(row, stats):
    for govID in stats:
        if stats[govID]['name'] == row[2]:
            print(f"Match found! {row[2]} has governorID {govID}")
            return govID
    return 0

def readOriginalData(inFile, stats):
    with open(inFile) as csvFile:
        reader = csv.reader(csvFile)
        next(reader, None) #skip header row
        
        for row in reader:
            stats[row[0]] = {}
            
            try:
                stats[row[0]]['Before_First_War'] = OldSnapshot(int(row[1].replace(',', '')), int(row[3].replace(',', '')), int(row[2].replace(',', '')))
                stats[row[0]]['First_War'] = OldSnapshot(int(row[5].replace(',', '')), int(row[7].replace(',', '')), int(row[6].replace(',', '')))
                stats[row[0]]['First_War_Continued'] = OldSnapshot(int(row[11].replace(',', '')), int(row[13].replace(',', '')), int(row[12].replace(',', '')))
            except ValueError:
                print(f'Error parsing {row[0]} stats') 
            
    return stats

def readBotData(inFile, stats, snapshotName):
    with open(inFile, newline='', encoding="utf-8") as csvFile:
        reader = csv.reader(csvFile)
        next(reader, None) #skip header row
        
        for row in reader:
            governorID = int(row[0])
            if governorID == 0:
                print(f"Error parsing governor {row[2]}, governorID is 0. Searching for match...")
                governorID = findGovernorIDMatchByName(row, stats)
                
                #couldn't find match by name
                if governorID == 0:
                    governorID = input("Couldn't find match. Please enter correct ID: ")
                
                    if governorID == '':
                        print(f"No governor number entered. Skipping...")
                        continue
                    else:
                        governorID = int(governorID)
            
            if governorID not in stats:
                if governorID == 19123275:
                    print("match")
                stats[governorID] = {}
            
            if 'name' in stats[governorID] and stats[governorID]['name'] != row[2]:
                print(f"Updating {stats[governorID]['name']} to {row[2]}")
            stats[governorID]['name'] = row[2]
            
            try:
                stats[governorID][snapshotName] = NewSnapshot(int(row[3]), int(row[4]), int(row[5]), int(row[6]))
            except ValueError:
                print(f'Error parsing governor {row[2]}, stat value not integer') 

def readData(inFile):
    pass

def writeData(stats, outFile):
    pass
    

def main():
    stats = {}
    
    readBotData('sample-files/before_second_war.csv', stats, 'Before_Second_War')
    #print(stats[19123275])
    readBotData('sample-files/after_second_war.csv', stats, 'After_Second_War')
    #print(stats[19123275])

if __name__ == "__main__":
    main()