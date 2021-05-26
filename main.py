import requests
import json
import pandas as pd
import numpy as np
from pandas import json_normalize


def find_series_name(url):

    key = 'Dataflow'
    series_list = requests.get(f'{url}{key}').json()['Structure']['Dataflows']['Dataflow']
    data = {}

    series_df = pd.DataFrame(data=data)

    for n, dimension in enumerate(series_list):

        data = {
            'seriesCode': [dimension['KeyFamilyRef']['KeyFamilyID']],
            'seriesDesc': [dimension['Name']['#text']],
        }
        temp_df = pd.DataFrame(data=data)
        series_df = series_df.append(temp_df, ignore_index=True)

        series_df.to_csv('main_series.csv')

    return series_df




def find_series_dimensions(url, series_df):

    dims_df = pd.DataFrame()

    for n in range(0, series_df.shape[0]):
        code = series_df.loc[n][0]
        # print(code)

        key = 'DataStructure/' + code
        data = {}

        try:

            dimension_list = requests.get(f'{url}{key}').json()['Structure']['KeyFamilies']['KeyFamily']['Components']['Dimension']

            for n, dimension in enumerate(dimension_list):

                data = {
                    'seriesCode': code,
                    'dimension': [dimension["@codelist"]]
                }
                # print(dimension["@codelist"])

                temp_df = pd.DataFrame(data=data)
                dims_df = dims_df.append(temp_df, ignore_index=True)

        except json.decoder.JSONDecodeError:
            print("Series " + code + " do not exist")


        dims_df.to_csv('dimensions.csv')

    return dims_df


def find_codes_desc(url, dims_df):

    codes_desc_df = pd.DataFrame()

    dims_df_temp = pd.DataFrame(dims_df, columns=['seriesCode', 'dimension'])

    dims_to_extract = dims_df_temp['dimension'].unique()

    for code in enumerate(dims_to_extract):

        key = 'CodeList/' + str(code[1])

        print(key)

        try:

            dimension_list = requests.get(f'{url}{key}').json()['Structure']['CodeLists']['CodeList']['Code']

            for n, dimension in enumerate(dimension_list):
                data = {
                    'seriesCode': str(code),
                    'dimension': [dimension["@value"]]
                }
                print(dimension["@value"])

                temp_df = pd.DataFrame(data=data)
                codes_desc_df = codes_desc_df.append(temp_df, ignore_index=True)

        except json.decoder.JSONDecodeError:
            print("There are no codes")

        codes_desc_df.to_csv('codes_desc.csv')


def mainRequest():

    url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'


def main():



    url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
    series_df = find_series_name(url)
    dims_df = find_series_dimensions(url, series_df)
    find_codes_desc(url, dims_df)
    #
    # test_code(url)

    # find_series_dimensions(url)



def test_code(url):

    key = 'CodeList/CL_FREQ'

    dimension_list = requests.get(f'{url}{key}').json()['Structure']['CodeLists']['CodeList']['Code']


    for n, dimension in enumerate(dimension_list):
        data = {
            'seriesCode': 'CL_FREQ',
            'dimension': [dimension["@value"]]
        }
        print(dimension["@value"])

        # temp_df = pd.DataFrame(data=data)
        # codes_desc_df = codes_desc_df.append(temp_df, ignore_index=True)




if __name__ == '__main__':

    main()