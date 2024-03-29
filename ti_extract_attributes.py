import json
from datetime import datetime
import requests


# Open the JSON file
# with open('/Users/nmehrok/Desktop/python/t_res.json') as file:
#     data = json.load(file)

url = 'https://www.tesla.com/inventory/api/v4/inventory-results?query={"query":{"model":"my","condition":"used","options":{"TRIM":["LRAWD"],"WHEELS":["NINETEEN"],"VehicleHistory":["CLEAN"],"Year":["2023"]},"arrangeby":"Price","order":"asc","market":"US","language":"en","super_region":"north america","lng":-96.0996978,"lat":41.28991329999999,"zip":"68164","range":0,"region":"NE"},"offset":50,"count":50,"outsideOffset":0,"outsideSearch":true,"isFalconDeliverySelectionEnabled":false,"version":null}'
headers = {
    'authority': 'www.tesla.com',
    'accept': '*/*',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,tr-TR;q=0.6,tr;q=0.5',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

resp = requests.get(url, headers=headers, timeout=5)
data = resp.json()

data['results'] = [result for result in data['results'] if datetime.strptime(
    result['ActualGAInDate'], '%Y-%m-%dT%H:%M:%S.%f') > datetime.strptime('2023-06-15T12:07:23.000000', '%Y-%m-%dT%H:%M:%S.%f')]
# data['results'].sort(key=lambda x: datetime.strptime(
#     x['ActualGAInDate'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)

# Calculate the CostToOwn for each result
for result in data['results']:
    est_total_cost = result['CashDetails']['cash']['estTotalCost']
    transportation_fee = result['TransportationFee']
    result['CostToOwn'] = est_total_cost + transportation_fee

data['results'].sort(key=lambda x: x['CostToOwn'])


def convert_date(date):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')


output_file = 't_out.txt'

with open(output_file, 'r') as file:
    existing_content = file.read()
# Get today's date
today = datetime.now().strftime('%Y-%m-%d')
# Append today's date to t_out.txt
with open(output_file, 'w') as t_out_file:
    t_out_file.write(today + '\t' + str(len(data['results'])) + '\n')

    # Loop over the objects in the results list
    for result in data['results']:
        # Extract the required attributes
        vin = result['VIN']

        # actual_ga_in_date = result['ActualGAInDate']
        warranty_vehicle = f"{convert_date(result['WarrantyData']['WarrantyVehicleExpDate'])} -> {convert_date(result['WarrantyData']['WarrantyBatteryExpDate'])}"
        est_total_cost = result['CashDetails']['cash']['estTotalCost']
        transportation_fee = result['TransportationFee']
        odometer = result['Odometer']
        link = f"https://www.tesla.com/my/order/{vin}#overview"

        output_string = f"{vin}\t{warranty_vehicle}\t{est_total_cost}\t{transportation_fee}\t{transportation_fee + est_total_cost}\t{odometer}\t{link}"
        t_out_file.write(output_string + '\n')

        # Print the extracted attributes
        print(output_string)
with open(output_file, 'a') as file:
    file.write(existing_content + '\n')
