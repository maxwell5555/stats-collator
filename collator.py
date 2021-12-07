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

def findGovernorIDMatchByName(name, stats):
    for govID in stats:
        if stats[govID]['name'] == name:
            print(f"Match found! {name} has governorID {govID}")
            return govID
    return 0

def readOriginalData(inFile, stats):
    count = 0
    with open(inFile) as csvFile:
        reader = csv.reader(csvFile)
        next(reader, None) #skip header row
        
        for row in reader:
            governorID = findGovernorIDMatchByName(row[0], stats)
            
            if governorID == 0:
                print(f"Couldn't find match for {row[0]}")
                count += 1
                continue
            
            try:
                stats[governorID]['Before_First_War'] = OldSnapshot(int(row[1].replace(',', '')), int(row[3].replace(',', '')), int(row[2].replace(',', '')))
                stats[governorID]['First_War'] = OldSnapshot(int(row[5].replace(',', '')), int(row[7].replace(',', '')), int(row[6].replace(',', '')))
                stats[governorID]['First_War_Continued'] = OldSnapshot(int(row[11].replace(',', '')), int(row[13].replace(',', '')), int(row[12].replace(',', '')))
            except ValueError:
                print(f'Error parsing {row[0]} stats') 
    
    print(count)
    return stats

def readBotData(inFile, stats, snapshotName):
    with open(inFile, newline='', encoding="utf-8") as csvFile:
        reader = csv.reader(csvFile)
        next(reader, None) #skip header row
        
        for row in reader:
            governorID = int(row[0])
            if governorID == 0:
                print(f"Error parsing governor {row[2]}, governorID is 0. Searching for match...")
                governorID = findGovernorIDMatchByName(row[2], stats)
                
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

def exportCSV(stats, outFile):
    with open(outFile, 'w', newline='', encoding="utf-8") as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for govID in stats:
            #construct table row
            row = []
            row.append(stats[govID]['name'])
            # try:
                # row.extend(stats[govID]['Before_First_War'])
            # except KeyError:
                # row.extend(['missing', 'missing', 'missing'])
            
            # try:
                # row.extend(stats[govID]['First_War'])
            # except KeyError:
                # row.extend(['missing', 'missing', 'missing'])

            # try:
                # row.extend(stats[govID]['First_War_Continued'])
            # except KeyError:
                # row.extend(['missing', 'missing', 'missing'])
                
            try:
                row.extend(stats[govID]['Before_Second_War'])
            except KeyError:
                row.extend(['missing', 'missing', 'missing', 'missing'])
                
            try:
                row.extend(stats[govID]['After_Second_War'])
            except KeyError:
                row.extend(['missing', 'missing', 'missing', 'missing'])
                
            csvWriter.writerow(row)
        
    

def main():
    stats = {}
    
    readBotData('sample-files/before_second_war.csv', stats, 'Before_Second_War')
    
    readBotData('sample-files/after_second_war.csv', stats, 'After_Second_War')
    
    #readOriginalData('sample-files/icky_stats.csv', stats)
    
    exportCSV(stats, 'sample-files/output.csv')

if __name__ == "__main__":
    main()