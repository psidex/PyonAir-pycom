import time
import pycom

from Configuration import config
from helper import get_sensors
from plantowerpycom import Plantower
from sensirionpycom import Sensirion
from TempSHT35 import TempSHT35

class HardwareTester:
    """
    A very verbose script that runs tests on all enabled hardware.
    If a developer or user suspects something isn't quite right with their hardware
    they can run this and it should help them diagnose the problem.
    """

    def __init__(self, logger):
        self.logger = logger
    
    def run_test(self):
        pycom.rgbled(0x66039a)
        self.logger.info("Running hardware test")

        active_sensors = get_sensors()
        active_sensor_names = list(active_sensors.keys())

        self.logger.info("Found {} sensors: {}".format(
            len(active_sensor_names),
            active_sensor_names
        ))

        for sensor_name in active_sensor_names:
            if active_sensors[sensor_name] == False:
                self.logger.info("Skipping test of disabled sensor {}".format(sensor_name))
                continue

            self.logger.info("Testing sensor {}".format(sensor_name))

            sensor_type = config.get_config(sensor_name)
            
            self.logger.info("Sensor {} found to be of type {}".format(
                sensor_name,
                sensor_type
            ))

            self.logger.info("Attempting to initialize sensor")
            # TODO: Double check I got the pins a id's the right way round!
            try:
                if sensor_type == "PMS5003":
                    sensor = Plantower(pins=("P3", "P17"), id=1,)
                elif sensor_type == "SPS030":
                    sensor = Sensirion(retries=1, pins=("P11", "P18"), id=2)
                elif sensor_type == "SHT35":
                    sensor = TempSHT35(None, None)
                else:
                    raise ValueError("Unknown sensor type")
            except Exception as e:
                self.logger.exception("Failed to initialize sensor: {}".format(e))
                continue

            time.sleep(1)
            init_count = 0

            try:
                init_limit = int(config.get_config(sensor_name + "_init"))
            except TypeError:
                # Sensor doesn't have a set init time.
                init_limit = 5

            self.logger.info("Warming up sensor for {} seconds".format(init_limit))
            while init_count < init_limit:
                try:
                    time.sleep(1)
                    sensor.read()
                    init_count += 1
                except Exception as e:
                    self.logger.exception("Failed to read from sensor: {}".format(e))
                    continue
            
            time.sleep(3)  # We can't read the sensor too fast after warmup
            self.logger.info("Attempting read of data from sensor")
            try:
                recv = sensor.read()
                if recv:
                    recv_str = str(recv)
                    self.logger.info("Read data: {}".format(recv_str))
                else:
                    self.logger.info("sensor.read returned no data")
            except Exception as e:
                self.logger.exception("Failed to read from sensor {}".format(sensor_type))
                continue

            self.logger.info("Finished testing sensor {}".format(sensor_name))

        self.logger.info("Hardware test finished")
        pycom.rgbled(0x000000)
