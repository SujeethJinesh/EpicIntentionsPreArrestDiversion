import pandas as pd
import requests
from api_keys import GOOGLE_MAPS_API_KEY
from pandas import ExcelWriter
from math import isnan
import plotly.graph_objs as go
import plotly
import time


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
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + GOOGLE_MAPS_API_KEY + '&address='
    addresses = excel['Arrest.Location'].tolist()
    t0 = time.time()
    for index, address in enumerate(addresses):
        address += ", Atlanta, GA"
        req = requests.get(GOOGLE_MAPS_API_URL + address.replace(" ", "+"))
        resp = req.json()
        try:
            lat_lng = resp['results'][0]['geometry']['location']
            print(address)
            lat = lat_lng['lat']
            lng = lat_lng['lng']
            print(lat_lng)

            # X is longitude and Y is latitude
            if excel['lng'][index] == '--' or excel['lng'][index] is None or excel['lng'][index] == '' or isnan(
                    excel['lng'][index]):
                excel['lng'][index] = lng
                excel['lng'][index] = lat
        except IndexError:
            import ipdb;
            ipdb.set_trace()
            pass
    t1 = time.time()
    print("time taken: ", t0-t1)
    writer = ExcelWriter("CleanedData.xlsx")
    excel.to_excel(writer, 'Sheet1')
    writer.save()


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
