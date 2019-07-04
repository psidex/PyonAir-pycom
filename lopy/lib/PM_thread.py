from plantowerpycom import Plantower, PlantowerException
from strings import timestamp_template
from helper import mean_across_arrays
import time


def pm_thread(sd, id, logger):

    print("Thread: {} started".format(id))

    # variables for sensor reading and computing averages
    plantower = Plantower()
    last_timestamp = None
    sensor_readings_lst = []

    # read and log pm sensor data
    while True:

        try:
            recv = plantower.read()
            if recv:
                recv_lst = str(recv).split(',')
                curr_timestamp = recv_lst[0]
                sensor_reading = [int(i) for i in recv_lst[1:]]
                if curr_timestamp != last_timestamp:
                    # If there are any readings with the previous timestamps, process them
                    if len(sensor_readings_lst) > 0:
                        lst_to_log = [last_timestamp] + [str(i) for i in mean_across_arrays(sensor_readings_lst)]
                        line_to_log = ','.join(lst_to_log)
                        logger.info(line_to_log)
                    # Set/reset global variables
                    last_timestamp = curr_timestamp
                    sensor_readings_lst = []
                # Add the current reading to the list, which will be processed when the timestamp changes
                sensor_readings_lst.append(sensor_reading)

        except PlantowerException as e:
            status_line = ', '.join([timestamp_template.format(*time.gmtime()), str(e.__class__)])
            print(status_line)
            # TODO: log exception

    # TODO: take mean of the messages if two or more readings per second
