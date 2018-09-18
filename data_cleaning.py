import pandas as pd
import requests
from api_keys import GOOGLE_MAPS_API_KEY
from pandas import ExcelWriter

# location of data
file_name = "data/09.13.18 PAD Diversions To Date.xlsx"
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + GOOGLE_MAPS_API_KEY + '&address='

excel = pd.read_excel(io=file_name)
addresses = excel['LOCATION/STREET'].tolist()

for index, address in enumerate(addresses):
    address += ", Atlanta, GA"
    req = requests.get(GOOGLE_MAPS_API_URL + address.replace(" ", "+"))
    resp = req.json()
    lat_lng = resp['results'][0]['geometry']['location']
    print(address)
    lat = lat_lng['lat']
    lng = lat_lng['lng']
    print(lat_lng)

    # import ipdb; ipdb.set_trace()

    # X is longitude and Y is latitude
    if excel['X'][index] == '--' or excel is None or excel == '':
        excel['X'][index] = lng
        excel['Y'][index] = lat

writer = ExcelWriter("CleanedData.xlsx")
excel.to_excel(writer, 'Sheet1')
writer.save()