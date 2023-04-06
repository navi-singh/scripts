import requests
from random import seed
from random import randint
import datetime
import json
import time

urls = ['https://www.tesla.com/inventory/api/v1/inventory-results?query={"query":{"model":"my","condition":"new","options":{"TRIM":["LRAWD"]},"arrangeby":"Relevance","order":"desc","market":"US","language":"en","super_region":"north america","lng":-104.8279512,"lat":39.6631609,"zip":"80014","range":200,"region":"CO"},"offset":0,"count":50,"outsideOffset":0,"outsideSearch":false}',
'https://www.tesla.com/inventory/api/v1/inventory-results?query={"query":{"model":"my","condition":"new","options":{"TRIM":["LRAWD"]},"arrangeby":"Relevance","order":"desc","market":"US","language":"en","super_region":"north america","lng":-96.1420947,"lat":41.1675179,"zip":"68138","range":200,"region":"NE"},"offset":0,"count":50,"outsideOffset":0,"outsideSearch":false}',
'https://www.tesla.com/inventory/api/v1/inventory-results?query={"query":{"model":"my","condition":"new","options":{"TRIM":["LRAWD"]},"arrangeby":"Relevance","order":"desc","market":"US","language":"en","super_region":"north america","lng":-90.19282160000002,"lat":38.6305392,"zip":"63101","range":100,"region":"MO"},"offset":0,"count":50,"outsideOffset":0,"outsideSearch":false}']

# open the file tdata.txt in append mode
file = open("tdata.txt", "r")
prevData = {}
# read the line by line and load into dictionary
for line in file:
    data = line.split("|")
    print("test")
    prevData[data[0]] = line

file.close()
file = open("tdata.txt", "a+")
while True:
    print("*******************************************")
    print(datetime.datetime.now().strftime("%H:%M"))
    for url in urls:
        response = requests.get(url)
        # response = requests.get(url, headers=headers, cookies=cookies)
        # check response is not null
        if response.content is not None:
            json_response = json.loads(response.content)
            results = json_response['results']

            for result in results:
                if 'EtaToCurrent' in result:
                # if result contains ['ActualGAInDate'] == None:
                    print('{\n\t'+ str(result['TotalPrice']) + "\t"+ result['City'] + "\t"+ result['VehicleRegion'] + '\t' + result['EtaToCurrent'])
                    for option in result['OptionCodeSpecs']['C_OPTS']['options']:
                        if option['name'] != 'Autopilot':
                            print('\t' + option['name'] )
                    print('}')
                    if result['VIN'] not in prevData:
                        newLine = result['VIN'] + "|" + str(result['TotalPrice']) + "|" + result['City'] + "|" + result['VehicleRegion'] + "|" + result['EtaToCurrent']
                        for option in result['OptionCodeSpecs']['C_OPTS']['options']:
                            if option['name'] != 'Autopilot':
                                newLine += '|' + option['name']
                        now = datetime.datetime.now()
                        newLine += now.strftime("|%H:%M:%S")
                        prevData[result['VIN']] = newLine
                        print(result['VIN'])
                        print(prevData.keys())
                        newLine += '\n'
                        file.write(newLine)
                        file.flush()
    print("*******************************************")
    time.sleep(300)
