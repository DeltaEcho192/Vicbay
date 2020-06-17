#TODO Config file for specific wave
#TODO Connection Check
#TODO Independent Docker runnable
#BUG Future_wave wrong units

from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import mysql.connector
import datetime
import time
i = 0

try:
    driver = webdriver.Chrome()
    url = 'https://www.surfline.com/surf-report/victoria-bay/584204204e65fad6a77094ae'
    driver.get(url)
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()


    stats_switch = False
    dateTime = datetime.datetime.now()
    future_wave = []
    future_wind = []


    #print(response.text[:500])



    wave_height_container = html_soup.find('div', class_ = "quiver-spot-forecast-summary__stat-container quiver-spot-forecast-summary__stat-container--surf-height")

    wave_height = wave_height_container.span.text
    wave_heightArr = re.findall('\d+', wave_height)
    wave_height = float((int(wave_heightArr[0]) + int(wave_heightArr[1])) / 2)
    print(wave_height)

    tide_container = html_soup.find_all('div', class_ = "quiver-conditions-stats__stat-reading")

    for container in tide_container:
        if stats_switch == False:
            tide = container.span.text
            stats_switch = True
        else:
            wind = container.span.text

    wind_dir_container = html_soup.find('div', class_ = 'quiver-spot-forecast-summary__stat-container quiver-spot-forecast-summary__stat-container--wind')
    wind_dir = wind_dir_container.find('span', class_ = 'quiver-reading-description').text

    tideArr = re.findall('\d+',tide)
    if len(tideArr) == 1:
        tide = float(tideArr[0])
    elif len(tideArr) == 2:
        tide = float(tideArr[0] + "." + tideArr[1])
    elif len(tideArr) == 3:
        tide = float(tideArr[0] +tideArr[1]+ "." + tideArr[2])

    windArr = re.findall('\d+',wind)
    wind = float(windArr[0])
    wind_dirArr = re.findall('\d+',wind_dir)
    wind_dir = float(wind_dirArr[0])

    print(tide, "\n", wind , '\n', wind_dir)

    future_wave_container = html_soup.find_all('div', class_ = "quiver-surf-graph__height")

    #print(future_container)

    i = 0
    for container in future_wave_container:
        future_wave_descendents = container.descendants
        for f in future_wave_container:
            if i < 5:
                #print(f.text,"\n")
                future_wave.append(float(f.text))
                i = i + 1
            else:
                break

    future_wind_container = html_soup.find_all('div', class_ = 'quiver-wind-graph__label')
    i = 0
    for container in future_wind_container:
        future_wind_descendents = container.descendants
        for f in future_wind_container:
            if i < 5:
                #print(f.text,"\n")
                future_wind.append(float(f.text))
                i = i + 1
            else:
                break

    #Required Fields
    #Wave height
    #Tide
    #Wind Speed
    #Future Wave Heights
    #Future Winds
    #future_wave[0],future_wave[1],future_wave[2],future_wave[3],future_wave[4],future_wind[0],future_wind[1],future_wind[2],future_wind[3],future_wind[4]

    #
    #
    #
    creds = []

    f = open("creds.txt", "r")

    for x in f:
        creds.append(x)

    f.close()
    #
    #
    #


    sql = 'insert into surf_data_testing (dateid, curHeight,curTide,curWind,curWindDir,furWave1,furWave2,furWave3,furWave4,furWave5,furWind1,furWind2,furWind3,furWind4,furWind5) VALUES ("%s",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'% (dateTime, wave_height,tide,wind,wind_dir,future_wave[0],future_wave[1],future_wave[2],future_wave[3],future_wave[4],future_wind[0],future_wind[1],future_wind[2],future_wind[3],future_wind[4])

    db_connection = mysql.connector.connect(
        host=creds[0],
        user=creds[1],
        passwd=creds[2],
        database=creds[3]
    )

    # prepare a cursor object using cursor() method
    db_cursor = db_connection.cursor()
    print(db_connection)

    db_cursor.execute(sql)
    db_connection.commit()
    print('Data has been Entered into the DataBase')

    db_cursor.close()
except Exception as e:
    print(e)

#print(tide_container.span.text)
