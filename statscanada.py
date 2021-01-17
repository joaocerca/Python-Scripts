import urllib3, shutil
from urllib3 import request
import datetime as dt
from string import Template


print("Starting download")

url = Template('https://www150.statcan.gc.ca/n1/delta/$date.zip')

today_day = dt.date.today()

def switch(today_day):

    if today_day.weekday() == 6:
        d = today_day.day - 2
        today_day = today_day.replace(day=d)
        return today_day

    elif today_day.weekday() == 5:
        d = today_day.day - 1
        today_day = today_day.replace(day=d)
        return today_day

    else:
        return today_day


new_day = switch(today_day)

new_day = new_day.__str__().replace("-","", -1)

url = url.substitute(date=new_day)

connection = urllib3.PoolManager()

filename = new_day.__add__(".zip")

with connection.request('GET', url, preload_content=False) as res, open(filename, 'wb') as out_file:
    shutil.copyfileobj(res, out_file)

print("Download completed!")

