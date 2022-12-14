from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
#from airflow.operators.bash import BashOperator

import psycopg2
from random import randint
from datetime import *

import requests
import json


def _read_weather():
    params = {
    'dbname': 'website_database',
    'user': 'postgres',
    'password': 'Magnus7257251!',
    'host': '90.231.140.42',
    'port': 5432
    }
    
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()





    href = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station-set/all/period/latest-hour/data.json"
    data_text = requests.get(href).text
    hour_data_json = json.loads(data_text)
    cursor.execute("""
        select max(timestamp) from temperature;
        """)
    # Check if there's a new timestamp in the first entry., imf there's no new timestamp we assume there's no new data.
    times = latest_timestamp = int(cursor.fetchone()[0])
    if times is not None:
        latest_timestamp = int(times)
        if latest_timestamp == hour_data_json["station"][0]["value"][0]["date"]:
            print("Timestamp not new, quitting program")
            cursor.close()
            connection.close()
            return None
       
    for i in range(len(hour_data_json["station"])):
        if hour_data_json["station"][i]["value"] is not None:
            station_id = int(hour_data_json["station"][i]["key"])
            station_name = hour_data_json["station"][i]["name"]
            station_owner = hour_data_json["station"][i]["owner"]
            station_longitude = hour_data_json["station"][i]["longitude"]
            station_latitude = hour_data_json["station"][i]["latitude"]
            station_temperature = hour_data_json["station"][i]["value"][0]["value"]
            station_value_quality = hour_data_json["station"][i]["value"][0]["quality"]
            station_value_date = hour_data_json["station"][i]["value"][0]["date"]
            station_height = hour_data_json["station"][i]["height"]

            # I also added variables for the less used variables below:
            # station_to = hour_data_json["station"][i]["to"]
            # station_from = hour_data_json["station"][i]["from"]
            # measuring_Stations = hour_data_json["station"][i]["measuringStations"]
            # station_owner_category = hour_data_json["station"][i]["ownerCategory"]
            cursor.execute("""SELECT station_id from station;""")
            idlist = list()
            for tupel in cursor.fetchall():
                tupel = tupel[0]
                idlist.append(tupel)

            if station_id not in idlist:
                cursor.execute(f"""
                INSERT INTO station (station_id, station_name, station_owner, longitude, latitude, height ) VALUES
                ({station_id}, $${station_name}$$, $${station_owner}$$, {station_longitude}, {station_latitude}, {station_height});
            """)
                connection.commit()

            if hour_data_json["station"][i]["value"] is not None:
                cursor.execute(f"""
                INSERT INTO temperature (station_id, value, timestamp, quality) VALUES
                ({station_id}, {station_temperature}, {station_value_date}, '{station_value_quality}');
                """)
                connection.commit()

    cursor.close()
    connection.close()
    return None


            # Timestamp is in Unix Epoch Time
            # We may want to check before posting to database if timestamp is represented in database. Most likely we can just check the first value and do a query as:
            # select timestamp from temperature
            # order by timestamp DESC
            # limit 1
            # And compare to the timestamp of first entry.

with DAG("weather_dag", start_date=datetime(2021, 1, 1),
    schedule_interval='0 */2 * * *', catchup=False) as dag:

        read_weather = PythonOperator(
            task_id="read_weather",
            python_callable=_read_weather
        )

        [read_weather]

