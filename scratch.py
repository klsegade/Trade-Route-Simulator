import csv

def nationProfile(climate,geographicFeatures,resources,trait,additional):
    economy = 0
    military = 5
    biome = climate.split(",")
    terrain = geographicFeatures.split(",")
    res = resources.replace(" ","")
    resList = res.split(",")
    traitList = trait.lower().split(",")
    notes = additional.split(",")
    for zone in biome:
        match zone:
            case 'subtropical':
                economy += 2
            case 'savannah':
                economy += 2
            case 'temperate deciduous':
                economy += 2        
            case 'temperate rainforest':
                economy += 1
            case 'grassland':
                economy += 1
            case 'desert':
                economy -= 1
            case 'taiga':
                economy -= 1
            case 'tundra':
                economy -= 1
    for feature in terrain:
        match feature:
            case 'mountains':
                military += 1
                economy -= 1
            case 'small coastline':
                economy += 1
            case 'large coastline':
                economy += 2
                military += 1   
    for item in resList:
        match item:
            case 'gold'|'silver'|'diamonds'|'emeralds'|'sapphires'|'rubies'|'turquoise'|'topaz'|'amethyst':
                economy += 3
            case 'garnet'|'spinel'|'sugar'|'salt'|'spices'|'coffee'|'tea'|'tobacco'|'silk'|'ivory'|'incense':
                economy += 2
            case 'textiles'|'fruit'|'crop'|'alcohol'|'furs'|'timber':
                economy += 1 
            case 'copper'|'tin':
                military += 1
            case 'iron':
                military += 2
    match traitList:
        case ['agrarian']:
            economy += 1
        case ['industrial']:
            economy += 1
            military += 1
        case ['nomadic']:
            military -= 1
        case ['isolationist']:
            economy -= 1
        case ['open']:
            economy += 1
            military -= 1
    for item in notes:
        if item != '':
            economy += 1
    economy = economy/2
    return (economy,military)

newData = []
with open('Nation_Profile_Template.csv', 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader, None) # Gets the first row and advances the iterator
    for row in csv_reader:        
        nationEcon,nationMil = nationProfile(row[3],row[4],row[5],row[6],row[7])
        nationName = row[0].split()
        newRow =[nationName,nationEcon,nationMil]
        newData.append(newRow)

with open('eco&milPower.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(newData)             

