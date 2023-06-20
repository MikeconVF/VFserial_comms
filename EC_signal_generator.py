# EC_signal_generator.py
import time

class sim_EC_signal:
    def __init__(self, start_value, end_value, step):
        self.start_value = start_value
        self.end_value = end_value
        self.step = step

    def generate_signal(self):
        current_value = self.start_value
        signal_values = []

        while current_value <= self.end_value:
            signal_values.append(current_value)
            time.sleep(1)  # Added for demonstration purposes, you can adjust the delay as needed
            current_value += self.step

        return signal_values
