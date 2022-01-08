from machine import ADC
from machine import Pin
from time import sleep


class DataLogger:
    """
    creats the log file and logs data to raspberry pico's flash
    """
    open("log.txt", "w").close()
    
    def __init__(self):
        self._temperature_val = None
        
    def get_data(self, val):
        self._temperature_val = val
        
    def log_it(self):
        with open("log.txt", "a") as ld:
            ld.write(f'Temperature registered - {self._temperature_val}\n')
            

class LM35Pico:
    """
    loads the LM35 and LED pins
    """
    _offset_voltage = 0.0330
    
    def __init__(self, pin_ADC: int, pin_LED: int):
        self._pin_ADC = pin_ADC
        self._pin_LED = Pin(pin_LED, Pin.OUT)
        self.__sleep_interval = 1
        self.log_data = False
        self.logger = DataLogger()
        
    def activate_data_logging(self):
        self.log_data = True
        
    def set_sleep_interval(self, sleep_val=1):
        self.__sleep_interval = sleep_val
        
    def __read_analog_input(self):
        """
        reads raw data from LM35 diode
        """
        return ADC.read_u16(ADC(self._pin_ADC))
    
    def compute_temperature(self):
        """
        converts the raw input to readeable data
        substract the diode offset voltage - preset to 0.0330
        returns Celcius temperature data by default
        """
        input_val = self.__read_analog_input()
        input_voltage = (input_val/65536) * 3.3
        input_voltage = (input_voltage  - LM35Pico._offset_voltage)*1000
        return input_voltage /10
    
    def get_temp_celcius(self):
        return round(self.compute_temperature(), 2)

    def start(self):     
        while 1:
            self._pin_LED.on()
            sleep(self.__sleep_interval)
            
            temp = self.get_temp_celcius()
            print(f'Temperature - {temp}')
            
            if self.log_data:
                self.logger.get_data(temp)
                self.logger.log_it()
            
            self._pin_LED.off()
            sleep(self.__sleep_interval)
            
    def __repr__(self):
        return f'ADC Pin used: {self._pin_ADC}\nLED Pin used: {self._pin_LED}\nLogger: {self.log_data}'
            
            

if __name__ == "__main__":
    new_lm = LM35Pico(28, 0)
    new_lm.set_sleep_interval(1)
    new_lm.activate_data_logging()
    print(new_lm)
    new_lm.start()
    
