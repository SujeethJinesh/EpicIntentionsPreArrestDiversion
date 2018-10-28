import pandas as pd
import csv


def init_data(filename):
    df = pd.read_csv(filename, low_memory=False)
    df = df.replace('NA', df.replace(['NA'], [None]))  # replace "NA" values, all locations are valid
    return df


def get_unique_charges(df):
    unique = set()
    keyword = "20-Quality of Life"

    type_of_arrest_list = df['Arrest.Charge']

    for index, type_of_arrest in enumerate(type_of_arrest_list):
        if df['Cobra.Section'][index] == keyword:
            unique.add(type_of_arrest)

    unique_list = list(unique)

    with open('unique_charges.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter='\n')
        wr.writerow(unique_list)

    import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    file_name = "data/Cleaned Arrest data CSV.csv"
    dataframe = init_data(file_name)
    get_unique_charges(dataframe)
