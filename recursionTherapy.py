from collections import Counter
import pandas as pd
import json,random
import sys

sys.setrecursionlimit(2000) # Set a new limit

#JSON file upload
def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in: {filepath}")
        return None
    except Exception as e:
         print(f"An unexpected error occurred: {e}")
         return None

file_path = "/home/klsegade/repos/Azgaar's Map Gen data/MyrPackCells.json"
json_data = load_json(file_path)

#JSON useful attribute extraction
cellList = {}
try:
    data = json_data['cells']['cells']
    for key in data:         
        index = key['i']
        centroid = key['p']
        nearCells = key['c']
        height = key['h']
        feature = key['f']
        distance = key['t']
        biome = key['biome']
        area = key['area']
        cellList[index] = {'Centroid':centroid,'Nearby Cells':nearCells,'Height':height,'Feature':feature,'Distance':distance,'Biome':biome,'Area/100(mi^2)':area,
                           'Shield Region':[0,0],'Sedimentary Basin':[0,0],'Platform':[0,0],'Rift Valley':[0,0],'Volcanic Arc':[0,0],'Orogenic Belt':[0,0], 'Zone':0}
except (TypeError, KeyError):
    print("could not read the creation time!")

#Define Geologic Zone Assignment
geoZones = {'Shield Region': {
                                "elevBand": [600,2500],
                                "slope": 'low',
                                "size": [300,800],
                                "rockTypes": ['igneous','metamorphic'],
                                "resources": ['gold','silver','copper','iron','sapphires','diamonds','garnets','spinel','quartz','granite'],
                                "rweights" : [0.1,1,5,5,0.1,1,0.5,0.5,5,20],
                                "notes": 'Ancient, exposed continental cores that are very stable and expansive.',
                                "color": "#e8e07d"
            },
            'Sedimentary Basin': {
                                "elevBand": [0,2000],
                                "slope": 'low',
                                "size": [150,400],
                                "rockTypes": ['sedimentary'],
                                "resources": ['coal','oil','fossils','salt','clay','quartz','iron','turquoise','limestone','sandstone'],
                                "rweights" : [5,5,5,1,5,5,5,0.1,20,20],
                                "notes": 'Broad, flat plains or inlands seas formed by subsidence or erosion.',
                                "color": "#7d85e8"
            },
            'Platform': {
                                "elevBand": [2000,10000],
                                "slope": 'low',
                                "size": [300,1000],
                                "rockTypes": ['igneous','metamorphic','sedimentary'],
                                "resources": ['salt','gypsum','quartz','copper','iron','coal','limestone'],
                                "rweights" : [1,1,5,1,5,5,20],
                                "notes": 'Broad, stable crustal areas covered by sedimentary layers.',
                                "color": "#e8b37d"
            },
            'Rift Valley': {
                                "elevBand": [-1300,3000],
                                "slope": 'high',
                                "size": [50,200],
                                "rockTypes": ['igneous','sedimentary'],
                                "resources": ['geodes','gems','geothermal','iron','quartz','gold','copper'],
                                "rweights" : [0.5,0.1,5,5,5,0.1,1],
                                "notes": 'Sunken valleys flanked by uplifted shoulders, stretching along tectonic boundaries.',
                                "color": "#85e87d"
            },
            'Volcanic Arc': {
                                "elevBand": [1500,20000],
                                "slope": 'high',
                                "size": [20,200],
                                "rockTypes": ['igneous'],
                                "resources": ['obsidian','sulfur','gold','silver','geothermal','iron','copper','topaz','amethyst','turquoise','basalt','rhyolite'],
                                "rweights" : [5,5,0.1,1,5,5,1,0.5,0.5,0.5,20,20],
                                "notes": 'Volcanic cones and uplifted regions near subduction zones.',
                                "color": "#e87d7d"
            },
            'Orogenic Belt': {
                                "elevBand": [2000,30000],
                                "slope": 'high',
                                "size": [150,500],
                                "rockTypes": ['igneous','metamorphic','sedimentary'],
                                "resources": ['copper','tin','iron','lead','zinc','silver','quartz','marble','gems','granite'],
                                "rweights" : [1,1,5,0.5,0.5,1,5,5,0.1,20],
                                "notes": 'Young and old regions caused by massive plate collisions.',
                                "color": "#7de8e0"
            }
            }

"""tempList = []
count = 0
steepcount = 0
flatcount = 0
for key in cellList:
    if cellList[key]['Height'] >= 20:
        h_val = round(((cellList[key]['Height'] - 18) ** 2)*3.281)
        neighborh = [round(((cellList[n]['Height'] - 18) ** 2)*3.281) for n in cellList[key]['Nearby Cells']]
        slope_val = [abs(h_val- h) for h in neighborh]
        #avgslope = sum(slope_val)/len(slope_val)
        for key2 in geoZones:
            min_val, max_val = geoZones[key2]["elevBand"]
            if min_val <= h_val <= max_val:
                cellList[key][key2] += 1
        #print(cellList[key])
        for slo in slope_val:            
            if slo > 2000:
                geokey2 = ['Rift Valley','Volcanic Arc','Orogenic Belt']
                for key2 in geokey2:
                    min_val, max_val = geoZones[key2]["elevBand"]
                    for temph in neighborh:
                        if min_val <= temph <= max_val:
                            cellList[key][key2] += 1
                cellList[key]['Rift Valley'] += 1
                cellList[key]['Volcanic Arc'] += 1
                cellList[key]['Orogenic Belt'] += 2
                #steepcount += 1
                #print(key,h_val,neighborh,slope_val,cellList[key]['Rift Valley'])
                #print(cellList[key])
            elif slo <2000:
                geokey2 = ['Shield Region','Sedimentary Basin','Platform']
                for key2 in geokey2:
                    min_val, max_val = geoZones[key2]["elevBand"]
                    for temph in neighborh:
                        if min_val <= temph <= max_val:
                            cellList[key][key2] += 1
                cellList[key]['Shield Region'] += 1
                #cellList[key]['Sedimentary Basin'] += 1
                cellList[key]['Platform'] += 1
                #flatcount +=1
           
        listZones = [cellList[n]['Zone'] for n in cellList[key]['Nearby Cells']]
        simpleListZones = [x for x in listZones if x != 0]
        tempCell = {k: cellList[key][k] for k in geoZones}        
        if not any(listZones):
            pass
        elif all(tempCell.get(item) == 0 for item in simpleListZones):
            pass
        else:
            for k,v in tempCell.items():    
                if v != 0:
                    if k in listZones:
                        continue
                    else:
                        tempCell[k] = 0
        zoneWeight = tempCell.values()
        newZone = random.choices(list(geoZones.keys()), weights=zoneWeight)
        cellList[key]['Zone'] = newZone[0]
        '''maxKey = max(tempCell.values())
        highest = [k for k,v in tempCell.items() if v == maxKey]
        for ele in highest:
            tempList.append(ele)
        count += 1'''

#Zone Groupings
skipList = []
zoneList = {}
def zoneCounter(neighborCells):       
    for cell in neighborCells:
        if cell in skipList:
            continue 
        elif cellList[cell]['Zone'] == cellList[key]['Zone']:
            neighborCellList.append(cell)
            skipList.append(cell)
            zoneCounter(cellList[cell]['Nearby Cells'])"""
    
'''for key in cellList:    '''#can I remove this section? I don't remember ...
'''    neighborCellList = []
    count = 0
    tempIndex = len(zoneGroup)
    zoneList[tempIndex] = {'Zone':[],'cells':[]}
    if key in skipList:
        continue       
    if cellList[key]['Height'] >= 20:
        zoneCounter([key])
        zoneList[tempIndex]['Zone'] = random.choice(zoneGroup[tempIndex][1])'''

#Zone Groupings
zoneGroup = {}
skipList = []
zoneList = {}
tempZones = {'Shield Region':0,'Sedimentary Basin':0,'Platform':0,'Rift Valley':0,'Volcanic Arc':0,'Orogenic Belt':0}
def zoneCounter(zoneCell, cellList, tempZones):       
    for cell in zoneCell:
        if cell in skipList or cellList[cell]['Height'] < 20:
            continue 
        else:
            global count
            count +=1         
            h_val = round(((cellList[cell]['Height'] - 18) ** 2)*3.281)
            neighborh = [round(((cellList[n]['Height'] - 18) ** 2)*3.281) for n in cellList[cell]['Nearby Cells']]
            slope_val = [abs(h_val- h) for h in neighborh]
            for key2 in geoZones:
                min_val, max_val = geoZones[key2]["elevBand"]
                if min_val <= h_val <= max_val:
                    cellList[cell][key2][0] += 1
                    tempZones[key2] += 1
            for slo in slope_val:            
                if slo > 2000:
                    cellList[cell]['Rift Valley'][1] += 1
                    cellList[cell]['Volcanic Arc'][1] += 1
                    cellList[cell]['Orogenic Belt'][1] += 1
                elif slo <2000:
                    cellList[cell]['Shield Region'][1] += 1
                    cellList[cell]['Sedimentary Basin'][1] += 1
                    cellList[cell]['Platform'][1] += 1
            if not any(tempZones[zone] == count for zone in geoZones):
                count -= 1
                set1 = {zone for zone in tempZones if tempZones[zone] == count}
                tempIndex = len(zoneGroup)
                zoneGroup[tempIndex] = [count,set1]
                for zone in tempZones:
                        tempZones[zone] = 0
                count = 0
                continue
            else:
                tempIndex = len(zoneGroup)
                if tempIndex not in zoneList:
                    zoneList[tempIndex] = {'Zone':[],'cells':[]}
                zoneList[tempIndex]['cells'].append(cell)   
                set1 = {zone for zone in tempZones if tempZones[zone] == count}
                if set1 <= {'Rift Valley','Volcanic Arc'} and count == 200:
                    tempIndex = len(zoneGroup)
                    zoneGroup[tempIndex] = [count,set1]
                    for zone in tempZones:
                        tempZones[zone] = 0
                    count = 0
                    continue
                elif set1 <= {'Orogenic Belt','Sedimentary Basin'} and count == 500:
                    tempIndex = len(zoneGroup)
                    zoneGroup[tempIndex] = [count,set1]
                    for zone in tempZones:
                        tempZones[zone] = 0
                    count = 0
                    continue
                elif set1 <= {'Platform','Shield Region'} and count == 800:
                    tempIndex = len(zoneGroup)
                    zoneGroup[tempIndex] = [count,set1]
                    for zone in tempZones:
                        tempZones[zone] = 0
                    count = 0
                    continue
                else:
                    if count > 500:
                        if 'Orogenic Belt' in set1:
                            tempZones['Orogenic Belt'] = 0
                        elif 'Sedimentary Basin' in set1:
                            tempZones['Sedimentary Basin'] = 0
                    elif count > 200:
                        if 'Rift Valley' in set1:
                            tempZones['Rift Valley'] = 0
                        elif 'Volcanic Arc' in set1:
                            tempZones['Volcanic Arc'] = 0

            skipList.append(cell)
            if len(zoneList[tempIndex]['cells']) == 199 or len(zoneList[tempIndex]['cells']) == 300:
                pass
            if count == 1:
                pass
            zoneCounter(cellList[cell]['Nearby Cells'], cellList, tempZones)
    
for key in cellList:
    #neighborCellList = []
    count = 0
    tempIndex = len(zoneGroup)
    zoneList[tempIndex] = {'Zone':[],'cells':[]}
    if key in skipList:
        continue       
    if cellList[key]['Height'] >= 20:
        zoneCounter([key],cellList,tempZones)
        set1 = {zone for zone in tempZones if tempZones[zone] == count}
        tempIndex = len(zoneGroup)
        zoneGroup[tempIndex] = [count,set1]
        for zone in tempZones:
                tempZones[zone] = 0
        count = 0
        #zoneList[tempIndex]['Zone'] = random.choice(zoneGroup[tempIndex][1])

zoneList.popitem()    

for index in zoneList:      #I think this just needs to change from index to key?
    if index != 441:            #additional line
        newZone = random.choice(list(zoneGroup[index][1]))  #this is an additional line
        zoneList[index]['Zone'] = newZone
    for cell in zoneList[index]['cells']:
        cellList[cell]['Zone'] = newZone
    neighborCellList = []
    #if key in skipList or cellList[key]['Zone']==0:
        #continue 
    #skipList.append(key)    
    #zoneList[count] = {'Zone':[],'cells':[]}
    #zoneList[count]['Zone'] = cellList[key]['Zone']
    #neighborCellList.append(key)
    #zoneCounter(cellList[key]['Nearby Cells'])
    #zoneList[count]['cells'] = neighborCellList
    #count += 1

#Resource Finder
resourceList = {}
for key in cellList:
    if cellList[key]['Zone'] == 0:
        continue
    zone = cellList[key]['Zone']
    res = geoZones[zone]['resources']
    resWeight = geoZones[zone]['rweights']
    pnone = 0.75
    if random.random() < pnone:
        continue
    else:
        resource = random.choices(res,resWeight)
        resourceList[key] = resource[0]

#Unicode emojis
resourceDict = {'gold':'🪙','silver':'💍','copper':'🟠','iron':'🗡️','tin':'⛃','zinc':'⛃','lead':'⛃','granite':'🪨','limestone':'🪨',
                'sandstone':'🪨','basalt':'🪨','rhyolite':'🪨','coal':'🌑','oil':'🕳️','fossils':'🦴','quartz':'⚱️','sapphires':'💎','diamonds':'💎',
                'topaz':'💎','garnets':'💎','spinel':'💎','amethyst':'💎','turquoise':'💎','gems':'💎','geodes':'🪨','clay':'🏺',
                'marble':'🗿','salt':'🧂','sulfur':'🧨','geothermal':'♨️','obsidian':'🪨','gypsum':'🏺'}

#Text Output for .map file replacement
textZ = ''
for key in zoneList:
    colorZone = zoneList[key]['Zone']
    textZ += '{'
    textZ += f'"i":{key},"name":"{zoneList[key]['Zone']}","type":"{zoneList[key]['Zone']}","cells":{zoneList[key]['cells']},"color":"{geoZones[colorZone]["color"]}"' 
    textZ += '},'
textR = ''
count = 77
for key in resourceList:
    textR += '{'
    textR += f'"icon":"{resourceDict[resourceList[key]]}","type":"{resourceList[key]}","x":{cellList[key]['Centroid'][0]},"y":{cellList[key]['Centroid'][1]},"cell":{key},"i":{count}'
    textR += '},'
    count += 1

with open('zoneLayer.txt', 'w') as file:
    print(textZ, file=file)
with open('resourceLayer.txt', 'w') as file:
    print(textR, file=file)