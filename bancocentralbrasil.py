import pandas as pd
import requests
import scrapy
import re
import urllib.request
import openpyxl
from string import Template
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

url = "https://www.bcb.gov.br/content/estatisticas/docs_estatisticasfiscais/Notimp3.xlsx"

r = requests.get(url)
filename = url.split('/')[-1]

filedownload = open('sourcefiles/' + filename, 'wb')
filedownload.write(r.content)
filedownload.close()

print(pd.read_excel(filename, sheet_name=[2]))


