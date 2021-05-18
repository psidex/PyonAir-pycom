"""
Simple logger for logging/storing sensor readings.
Replaces the functionality of the sensor logger that was previously produced by the LoggerFactory
"""
import _thread
import sys

import strings as s
from Configuration import config
from welford import WelfordAverage

class SensorLogger:
    """Stores sensor reading averages and also logs data to the terminal"""

    def __init__(self, sensor_name, terminal_out=True, terminator='\n'):
        """
        :param sensor_name: sensor name
        :type sensor_name: str
        :param terminal_out: print output to terminal
        :type terminal_out: bool
        :param terminator: end of line character
        :type terminator: object
        """
        self.terminal_out = terminal_out
        self.terminator = terminator
        self.sensor_name = sensor_name
        self.sensor_type = config.get_config(sensor_name)
        
        # Average data that we return if there isn't enough readings to create one
        self.zeroed_data = list('0' * len(s.lora_sensor_headers[self.sensor_type]))

        # We use a lock since log_row and get_averages will be called from diff threads
        self.average_list_lock = _thread.allocate_lock()

        self.average_list = []
        self.init_averages()
    
    def init_averages(self):
        """
        Create an instance of the welford average class for each value we're reading.
        Resets any previously used average instances.
        """
        header_count = len(s.lora_sensor_headers[self.sensor_type])
        self.average_list = [WelfordAverage() for _ in range(header_count)]
    
    def get_averages(self):
        """
        Calculates, returns, and then resets the running averages for this sensor.
        """
        with self.average_list_lock:
            try:
                # x.averages() returns a list, see welford.py
                averages = [str(int(x.averages()[1])) for x in self.average_list]
                # Pull the count from the first reading.
                average_counter = self.average_list[0].averages()[0]

            except ValueError:
                # The first one or two calls to averages() will return float("nan") due to
                # how the algorithm works. If this happens we don't want to write these
                # incorrect values to the disk.
                averages = self.zeroed_data
                average_counter = 0

            # This method should only be called when the averages are being "used", so now
            # they are used we should reset.
            self.init_averages()

        # This is the information that get_average in averages.py wants to return.
        return {
            self.sensor_name + "_avg": averages,
            self.sensor_name + "_count": average_counter
        }

    def log_row(self, row):
        """
        Logs sensor readings and updates the stored averages.
        :param row: The data row constructed from a process_readings method
        :type row: str
        """
        if self.terminal_out:
            sys.stdout.write(self.sensor_name + " - " + row + self.terminator)

        # Parse row to get the values we want.
        headers = s.headers_dict_v4[self.sensor_type]
        row_values = str(row).split(',')
        headers_with_values = dict(zip(headers, row_values))

        # Update the rolling averages in self.average_list.
        with self.average_list_lock:
            # For each header we want to keep track of
            for i, header in enumerate(s.lora_sensor_headers[self.sensor_type]):
                self.average_list[i].update(int(headers_with_values[header]))
