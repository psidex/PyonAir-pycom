"""
Tasks to be called by event scheduler
"""

import os
import time
import ujson

import strings as s
from Configuration import config
from helper import (blink_led, current_lock, get_format, get_sensors,
                    mean_across_arrays, minutes_of_the_month)


def get_sensor_averages(logger, sensor_loggers, lora):
    """
    Takes the averages of sensor readings from the sensor loggers and constructs a line to log to the terminal and lora buffer.
    :param logger: status logger
    :type logger: LoggerFactory object
    :param lora: LoRaWAN object, False if lora is not enabled
    :type lora: LoRaWAN object
    """

    logger.debug("Getting sensor averages")

    # Get a dictionary of sensors and their status
    sensors = get_sensors()
    fmt = get_format(sensors)
    version = str(config.get_config("fmt_version"))
    timestamp = s.csv_timestamp_template.format(*time.gmtime())  # get current time in desired format
    minutes = str(minutes_of_the_month())  # get minutes past last midnight

    try:
        sensor_averages = {}
        for sensor_logger in sensor_loggers:
            sensor_averages.update(sensor_logger.get_averages())

        # Append averages to the line to be sent over LoRa according to which sensors are defined.
        line_to_log = '{}' + fmt + ',' + version + ',' + minutes
        for sensor_name in [s.TEMP, s.PM1, s.PM2]:
            if sensors[sensor_name]:
                line_to_log += ',' + str(config.get_config(sensor_name + "_id")) + ',' + ','.join(sensor_averages[sensor_name + "_avg"]) + ',' + str(sensor_averages[sensor_name + "_count"])
        line_to_log += '\n'

        # Logs line_to_log to archive and places copies into relevant to_send folders
        log_averages(line_to_log.format(timestamp + ','))
        if lora is not False:
            year_month = timestamp[2:4] + "," + timestamp[5:7] + ','
            lora.lora_buffer.write(line_to_log.format(year_month))

    except Exception:
        logger.exception("Failed to flash averages")
        blink_led((0x550000, 0.4, True))


def log_averages(line_to_log):
    """
    Logs averages to the 'Averages' folder in 'Archive' separated by each month
    :param line_to_log: line of averages to log
    :type line_to_log: str
    """
    # Save averages to a new file each month
    archive_filename = "{:04d}_{:02d}".format(*time.gmtime()[:2]) + "_Sensor_Averages"  # yyyy_mm_Sensor_Averages
    archive_filepath = s.archive_averages_path + archive_filename + ".csv"  # /sd/archive/Averages/archive_filename
    with open(archive_filepath, 'a') as f:
        f.write(line_to_log)
