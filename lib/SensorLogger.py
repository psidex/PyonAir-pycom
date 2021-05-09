"""
Simple logger for logging sensor readings.
Replaces the functionality of the sensor logger that was previously produced by the LoggerFactory
"""
import sys
from helper import current_lock
import strings as s
from welford import WelfordAverage
import ujson

class SensorLogger:
    def __init__(self, sensor_name, sensor_type, terminal_out=True, terminator='\n'):
        """
        :param sensor_name: sensor name
        :type sensor_name: str
        :param terminal_out: print output to terminal
        :type terminal_out: bool
        :param terminator: end of line character
        :type terminator: object
        """
        self.filename = s.current_path + sensor_name + '.json'
        self.terminal_out = terminal_out
        self.terminator = terminator
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type
        self.init_averages()
    
    def init_averages(self):
        """
        Create an instance of the welford average class for each value we're reading.
        """
        # TODO: We want to call this ideally after every lora message sent.
        header_count = len(s.lora_sensor_headers[self.sensor_type])
        self.average_list = [WelfordAverage() for _ in range(header_count)]

    def log_row(self, row):
        """
        Logs sensor readings and updates the stored averages.
        """
        row_to_log = row + self.terminator
        if self.terminal_out:
            sys.stdout.write(self.sensor_name + " - " + row_to_log)
        
        # Parse row to get the values we want.
        headers = s.headers_dict_v4[self.sensor_type]
        stripped_line_lst = str(row).split(',')
        named_line = dict(zip(headers, stripped_line_lst))

        # Update the rolling averages in self.average_list.
        for i, header in enumerate(s.lora_sensor_headers[self.sensor_type]):
            self.average_list[i].update(int(named_line[header]))

        # Get the current averages and save to file so other threads can read.
        # x.averages() returns a list, see welford.py
        try:
            averages = [str(int(x.averages()[1])) for x in self.average_list]
        except ValueError:
            # The first one or two calls to averages() will return float("nan") due to
            # how the algorithm works. If this happens we don't want to write these
            # incorrect values to the disk.
            return

        # Pull the count from the first reading.
        average_counter = self.average_list[0].averages()[0]

        # This is the information that get_average in averages.py wants to return.
        calculated = {
            self.sensor_name + "_avg": averages,
            self.sensor_name + "_count": average_counter
        }

        # Spend as little time in the lock as possible.
        dump = ujson.dumps(calculated)
        with current_lock:
            with open(self.filename, 'w') as f:
                f.write(dump)
