from collections import Counter
import pandas as pd
import json,random

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
zoneList = {}
try:
    data = json_data['cells']['cells']
    for key in data:         
        index = key['i']
        centroid = key['p']
        nearCells = key['c']
        cellList[index] = {'Centroid':centroid,'Nearby Cells':nearCells,'Zone':0}
    data2 = json_data['cells']['zones']
    for key in data2:
        index = key['i']
        zone = key['name']
        cells = key['cells']
        zoneList[index] = {'Zone':zone,'Cells':cells}
except (TypeError, KeyError):
    print("could not read the creation time!")

#Define Geologic Zone Assignment
geoZones = {'Shield Region': {
                                "elevBand": [600,2500],
                                "slope": 'low',
                                "size": [300,800],
                                "rockTypes": ['igneous','metamorphic'],
                                "resources": ['gold','silver','copper','iron','sapphires','diamonds','garnets','spinel','quartz','granite'],
                                "rweights" : [0.5,5,5,5,0.5,1,0.5,0.5,5,20],
                                "notes": 'Ancient, exposed continental cores that are very stable and expansive.',
                                "color": "#e8e07d"
            },
            'Sedimentary Basin': {
                                "elevBand": [0,2000],
                                "slope": 'low',
                                "size": [150,400],
                                "rockTypes": ['sedimentary'],
                                "resources": ['coal','oil','fossils','salt','clay','quartz','iron','turquoise','limestone','sandstone'],
                                "rweights" : [5,5,5,1,5,5,5,0.5,20,20],
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
                                "rweights" : [0.5,0.5,5,5,5,0.5,1],
                                "notes": 'Sunken valleys flanked by uplifted shoulders, stretching along tectonic boundaries.',
                                "color": "#85e87d"
            },
            'Volcanic Arc': {
                                "elevBand": [1500,20000],
                                "slope": 'high',
                                "size": [20,200],
                                "rockTypes": ['igneous'],
                                "resources": ['obsidian','sulfur','gold','silver','geothermal','iron','copper','topaz','amethyst','turquoise','basalt','rhyolite'],
                                "rweights" : [5,5,0.5,1,5,5,1,0.5,0.5,0.5,20,20],
                                "notes": 'Volcanic cones and uplifted regions near subduction zones.',
                                "color": "#e87d7d"
            },
            'Orogenic Belt': {
                                "elevBand": [2000,30000],
                                "slope": 'high',
                                "size": [150,500],
                                "rockTypes": ['igneous','metamorphic','sedimentary'],
                                "resources": ['copper','tin','iron','lead','zinc','silver','quartz','marble','gems','granite'],
                                "rweights" : [1,1,5,0.5,0.5,1,5,5,0.5,20],
                                "notes": 'Young and old regions caused by massive plate collisions.',
                                "color": "#7de8e0"
            }
            }

#Resource Finder
resourceList = {}
bioResources = ['spices','silk','tea','coffee','sugar','tobacco','textiles','porcelain',
                'ivory','furs','dyes','timber','alcohol','fruit','incense','crop','livestock','game']
for key in zoneList:
    zone = zoneList[key]['Zone']
    for cell in zoneList[key]['Cells']:
        res = geoZones[zone]['resources']
        resWeight = geoZones[zone]['rweights']
        rChance = random.random()
        if rChance < .5:
            continue
        elif .5 <= rChance < .75:
            resource = random.choice(bioResources)
            resourceList[cell] = resource
        else:
            resource = random.choices(res,resWeight)
            resourceList[cell] = resource[0]

#Unicode emojis
resourceDict = {'gold':'🪙','silver':'💍','copper':'🟠','iron':'🗡️','tin':'⛃','zinc':'⛃','lead':'⛃','granite':'🪨','limestone':'🪨',
                'sandstone':'🪨','basalt':'🪨','rhyolite':'🪨','coal':'🌑','oil':'🕳️','fossils':'🦴','quartz':'⚱️','sapphires':'💎','diamonds':'💎',
                'topaz':'💎','garnets':'💎','spinel':'💎','amethyst':'💎','turquoise':'💎','gems':'💎','geodes':'🪨','clay':'🏺',
                'marble':'🗿','salt':'🧂','sulfur':'🧨','geothermal':'♨️','obsidian':'🪨','gypsum':'🏺','spices':'🌶️', 'silk':'🥻', 'tea':'🫖',
                'coffee':'☕', 'sugar':'🧊', 'tobacco':'🌿', 'textiles':'🧣', 'porcelain':'⚱️', 'ivory':'🐘', 'furs':'🦦', 'dyes':'🪻', 'timber':'🪵',
                'alcohol':'🍺', 'fruit':'🍊', 'incense':'🪔', 'crop':'🌾', 'livestock':'🐄', 'game':'🦬'}

#Text Output for .map file replacement
textR = ''
count = 77
for key in resourceList:
    textR += '{'
    textR += f'"icon":"{resourceDict[resourceList[key]]}","type":"{resourceList[key]}","x":{cellList[key]['Centroid'][0]},"y":{cellList[key]['Centroid'][1]},"cell":{key},"i":{count}'
    textR += '},'
    count += 1

with open('resourceLayer.txt', 'w') as file:
    print(textR, file=file)