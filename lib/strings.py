csv_timestamp_template = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}.csv"  # yyyy-mm-dd hh-mm-ss

headers_dict_v4 = {
    "PMS5003": ["timestamp", "pm10_cf1", "PM1", "pm25_cf1", "PM25", "pm100_cf1", "PM10", "gr03um", "gr05um", "gr10um", "gr25um", "gr50um", "gr100um", ""],
    "PMS7003": ["timestamp", "pm10_cf1", "PM1", "pm25_cf1", "PM25", "pm100_cf1", "PM10", "gr03um", "gr05um", "gr10um", "gr25um", "gr50um", "gr100um", ""],
    "PMSA003": ["timestamp", "pm10_cf1", "PM1", "pm25_cf1", "PM25", "pm100_cf1", "PM10", "gr03um", "gr05um", "gr10um", "gr25um", "gr50um", "gr100um",""],
    "OPCN2": ["timestamp", "PM1", "PM25", "PM10", "Bin0", "Bin1", "Bin1MToF", "Bin2", "Bin3", "Bin3MToF", "Bin4", "Bin5", "Bin5MToF", "Bin6", "Bin7", "Bin7MToF", "Bin8", "Bin9", "Bin10", "Bin11", "Bin12", "Bin13", "Bin14", "Bin15", "SFR", "Checksum", "SamplingPeriod"],
    "HPMA115S0": ["timestamp", "PM10", "PM25"],
    "OPCR1": ["timestamp", "PM1", "PM25", "PM10", "Bin0", "Bin1", "Bin1MToF", "Bin2", "Bin3", "Bin3MToF", "Bin4", "Bin5", "Bin5MToF", "Bin6", "Bin7", "Bin7MToF", "Bin8", "Bin9", "Bin10", "Bin11", "Bin12", "Bin13", "Bin14", "Bin15", "SFR", "Checksum", "SamplingPeriod", "Temperature", "Humidity"],
    "SPS030": ["timestamp", "PM1", "PM25", "PM4", "PM10", "n05", "n1", "n25", "n4", "n10", "tps"],
    "SDS018": ["timestamp", "PM10", "PM25"],
    "AM2302": ["timestamp", "humidity", "temperature"],
    "BME280": ["timestamp", "humidity", "temperature", "pressure"],
    "SHT35": ["timestamp", "temperature", "humidity"]
}

# headers from headers_dict_v4 to calculate averages in task.py and send over LoRaWAN
lora_sensor_headers = {
    "SHT35": ["temperature", "humidity"],
    "PMS5003": ["PM10", "PM25"],
    "SPS030": ["PM10", "PM25"]
}

status_header = ['type', 'timestamp', 'message']

config_filename = 'config.txt'

# Sensor names
PM1 = 'PM1'
PM2 = 'PM2'
TEMP = 'TEMP'

# Extensions
current_ext = '.current'
processing_ext = '.processing'
dump_ext = ''

# Directories
current = 'current'
processing = 'processing'
lora = 'lora_tosend'
wifi = 'wifi_tosend'
archive = 'archive'

# Paths
root_path = '/sd/'
current_path = root_path + current + '/'
processing_path = root_path + processing + '/'
archive_path = root_path + archive + '/'
lora_path = root_path + lora + '/'
filesystem_dirs = [current, processing, lora, wifi, archive]

# Templates
file_name_temp = root_path + '{}' + '.csv' + '{}'  # call this like: file_name_temp.format(sensor_name, extension)

# Temporary constant files before message queueing implemented
lora_file = 'lora.csv'
