# Converts the "json" file from ttn-receiver into a csv file.
# Example usage:
#   python3 ./out-to-csv.py ./ttn-receiver-data/data.json > data.csv

import json
import sys
import dateutil.parser

print("time,pm1_pm10,pm1_pm25,pm2_pm10,pm2_pm25,temperature,humidity")
with open(sys.argv[1], "r") as f:
    for line in f.readlines():
        data = json.loads(line)
        p = data["payload_fields"]
        time = dateutil.parser.isoparse(data["metadata"]["time"])
        # month/day/year as google sheets prefers that :(
        datetime = time.strftime("%m/%d/%Y %H:%M:%S")
        temp = int(p["temperature"]) / 10
        humidity = int(p["humidity"]) / 10
        if temp == 0 and humidity == 0:
            # If these are both zero this is probably a broken reading.
            continue
        print(
            f'{datetime},{p["PM1_PM10"]},{p["PM1_PM25"]},{p["PM2_PM10"]},{p["PM2_PM25"]},{temp},{humidity}'
        )
