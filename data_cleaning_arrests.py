import pandas as pd
import requests
from api_keys import GOOGLE_MAPS_API_KEY_SUJEETH, GOOGLE_MAPS_API_KEY_DIANA, GOOGLE_MAPS_API_KEY_FELIX
from pandas import ExcelWriter
from math import isnan
import plotly.graph_objs as go
import plotly
import time
import pickle


def graph(excel, column_name, title, x_label, y_label="# of Arrests"):
    print(excel[column_name].value_counts())  # print type of
    layout = go.Layout(title=title,
                       xaxis=dict(title=x_label),
                       yaxis=dict(title=y_label))
    data_types = excel[column_name].value_counts().to_dict()

    data = [go.Bar(
        x=list(data_types.keys()),
        y=list(data_types.values())
    )]
    fig = go.Figure(data=data, layout=layout)

    plotly.offline.plot(fig, filename=column_name, image_filename=column_name, image='png')


def clean_data(excel):
    # location of data
    addresses = excel['Arrest.Location'].tolist()
    errors = []
    lat_lngs = []

    t0 = time.time()
    for index, address in enumerate(addresses):
        if index > 26500:
            GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + GOOGLE_MAPS_API_KEY_DIANA + '&address='
        elif index < 5000:
            GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + GOOGLE_MAPS_API_KEY_SUJEETH + '&address='
        else:
            GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + GOOGLE_MAPS_API_KEY_FELIX + '&address='
        # time.sleep(1.2)  # prevent overruning server
        address += ", Atlanta, GA"
        req = requests.get(GOOGLE_MAPS_API_URL + address.replace(" ", "+"))
        resp = req.json()
        try:
            lat_lng = resp['results'][0]['geometry']['location']
            print(address)
            lat = lat_lng['lat']
            lng = lat_lng['lng']
            print(lat_lng)
            lat_lngs.append({'address': address, "lat_lng": lat_lng, "index": index})

            # X is longitude and Y is latitude
            if excel['lng'][index] == '--' or excel['lng'][index] is None or excel['lng'][index] == '' or isnan(
                    excel['lng'][index]):
                excel['lng'][index] = lng
                excel['lat'][index] = lat
        except IndexError:
            with open('lat_lngs.pkl', 'wb') as f:
                pickle.dump(lat_lngs, f)
            errors.append(index)
            pass
    with open('lat_lngs.pkl', 'wb') as f:
        pickle.dump(lat_lngs, f)
    t1 = time.time()
    print("time taken: ", t1-t0)
    print("errors", errors)
    # errors: 298, 494, 891, 901, 902, 1584, 1590, 1824, 2433, 2451, 3019, 3355, 3616, 4034, 4813, 4945, 4960, 5532, 5685, 5712, 5955, 6496, 6581, 8227, 8501, 9782, 10427, 18933, 35488, 42930
    writer = ExcelWriter("CleanedData.xlsx")
    excel.to_excel(writer, 'Sheet1')
    writer.save()
    import ipdb; ipdb.set_trace()


def init_data(filename):
    df = pd.read_csv(filename, low_memory=False)
    df.replace('NA', df.replace(['NA'], [None]))  # replace "NA" values, all locations are valid
    df['lng'] = None
    df['lat'] = None
    return df


if __name__ == '__main__':
    file_name = "data/Cleaned-Data-Arrests-Jan17-Aug18-withrationale.csv"
    dataframe = init_data(file_name)

    # arrest_type = 'Cobra.Section'
    # graph(dataframe, arrest_type, "Arrest Types", "Arrest Type")
    #
    # arrest_reasons = 'Arrest.Charge'
    # graph(dataframe, arrest_reasons, "Arrest Reasons", "Arrest Reason")
    #
    # race = 'Race'
    # graph(dataframe, race, "Races", "Race")
    #
    # sex = 'Sex'
    # graph(dataframe, sex, "Sex", "Sex")
    #
    # beat = 'Beat'
    # graph(dataframe, beat, "Beats", "Beat Number")
    #
    # age = 'Age.at.arrest'
    # graph(dataframe, age, "Ages", "Age")
    #
    # last_name = 'Last.Name'
    # graph(dataframe, last_name, "Last Names", "Last Name")
    #
    # officer_id = 'Officer.ID'
    # graph(dataframe, officer_id, "Officer Ids", "Officer Id")

    clean_data(dataframe)
