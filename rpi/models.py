#TODO: Convert these JSON objects into Python Classes and objects
import json
from datetime import datetime
from crud import *
import os

class Home:
    def __init__(self, name):
        self.name = name
        self.home_id = None

        self.get_home_id() #Either gets the home_id or creates it

        print("Initialized home, with id", self.home_id)

    def get_home_id(self):
        if os.path.isfile('./data/home_id.json'):
            self.load_home_id_from_json()
        else:
            self.initialize_new_home_on_server()

    def load_home_id_from_json(self):
        with open('./data/home_id.json', 'r') as f: #Store the id on 'hard storage' as a JSOn
            self.home_id = json.load(f)

    def initialize_new_home_on_server(self):
        response = post_home_data({'name': self.name})
        self.home_id = response.json()["response"]["_id"]
        self.store_home_id()


    def store_home_id(self):
        if not os.path.isdir('./data'):
            os.mkdir('./data')
        with open('./data/home_id.json', 'w+') as f: #Store the id on 'hard storage' as a JSOn
            json.dump(self.home_id, f)


class Module: #Parent of IntruderModule and SensorModule
    def __init__(self, home_id):
        self._id = None
        self.name = None
        self.home_id = home_id
        self.sensors = [] # A dictionary where the key is the sensor_name, the value is just the object
        self.current_data = {}

    def add_sensors(self,*sensors):
        # Add one or multiple sensors
        for sensor in sensors:
            self.sensors.append(sensor)

    def update_current_data(self):
        for sensor in self.sensors:
            if sensor.get_most_recent_data(): #If the recent data is not none
                self.current_data[sensor.name] = sensor.get_most_recent_data()

    def export_daily_data(self): #The daily data is all of the data in a given day, the raspberry pi wipes the data every day
        for sensor in self.sensors:
            print(sensor)
    

    def check_data_and_notify(self):
        #TODO: Make sure the numbers are right
        for sensor in self.sensors:
            title = ""
            info = ""
            if sensor.name == 'temperature':
                if sensor.get_most_recent_data() > 25:
                    title = "Your house is overheating!"
                    info = "Your house is reaching a temperature of {}! This is quite high.".format(sensor.get_most_recent_data())
            
            elif sensor.name == 'humidity':
                if sensor.get_most_recent_data() > 70:
                    title = "High humidity detected!"
                    info = "Humidity of {}".format(sensor.get_most_recent_data())

        
            elif sensor.name == 'light_level':
                if sensor.get_most_recent_data() > 20:
                    title = "High light level detected!"
                    info = "Light level of {}".format(sensor.get_most_recent_data())


            elif sensor.name == 'moisture':
                if sensor.get_most_recent_data() > 30:
                    title = "High moisture detected!"
                    info = "You have a moisture of level {}".format(sensor.get_most_recent_data())

            if title != "" and info != "": #If there is a notification to be sent
                put_notification_data({'id': self.home_id, 'notification': {'title': title, 'module_id': self._id, 'info': info}})

class IntruderModule(Module):
    # Noise Sensor, Motion, door is open,
    def __init__(self, home_id):
        super().__init__(home_id) #Initialize parent class
        self.name = "Gongster's Intruder Module"

    def upload_data(self):
        final_object = self.current_data
        final_object['id'] = self._id

        response = put_intruders_data(final_object)
        return response

    def get_intruder_module_id(self):
        if os.path.isfile('./data/intruder_module_id.json'):
            self.load_intruder_module_id_from_json()
        else:
            self.initialize_new_intruder_module_on_server()

    def initialize_new_intruder_module_on_server(self):
        response = post_intruders_data({'name': self.name,'home_id': self.home_id, 'current_data': self.current_data})
        self._id = response.json()["response"]["intruderResult"]["_id"]
        self.store_intruder_module_id()

    def store_intruder_module_id(self):
        with open('./data/intruder_module_id.json', 'w+') as f: #Store the id on 'hard storage' as a JSOn
            json.dump(self._id, f)

    def load_intruder_module_id_from_json(self):
        with open('./data/intruder_module_id.json', 'r') as f: #Store the id on 'hard storage' as a JSOn
            self._id = json.load(f)




class Intruder:
    def __init__(self, name):
        self.name = name
    
    #We eventually want to detect when theres intrudders

class SensorModule(Module): 
    # Includes Light Level, Humidity, Temperature, and Moisture Sensor
    def __init__(self, home_id):
        super().__init__(home_id) #Initialize parent class
        self.name = "Gongster's Sensor Module"
        self.current_data = {}

        self.get_sensor_module_id()

        print("Initialized sensor module, with id", self._id)

    def get_sensor_module_id(self):
        if os.path.isfile('./data/sensor_module_id.json'):
            self.load_sensor_module_id_from_json()
        else:
            self.initialize_new_sensor_module_on_server()

    def initialize_new_sensor_module_on_server(self):
        response = post_sensors_data({'name': self.name,'home_id': self.home_id, 'current_data': self.current_data})
        self._id = response.json()["response"]["sensorResult"]["_id"]
        self.store_sensor_module_id()

    def store_sensor_module_id(self):
        with open('./data/sensor_module_id.json', 'w+') as f: #Store the id on 'hard storage' as a JSOn
            json.dump(self._id, f)

    def load_sensor_module_id_from_json(self):
        with open('./data/sensor_module_id.json', 'r') as f: #Store the id on 'hard storage' as a JSOn
            self._id = json.load(f)

    def upload_data(self):
        final_object = self.current_data
        final_object['id'] = self._id

        response = put_sensors_data(final_object)

class Sensor:
    def __init__(self, name):
        self.name = name
        self.data = None

        self.load_data()
        
    def reset_json(self):
        #Since all of the data is already stored on the MongoDB server, we don't need to save more. Only enough locally
        #so we know we are not sending duplicates
        os.remove('./data/sensors/' + self.name + '.json')

    def load_data(self):
        # If data exists, load it 
        if os.path.isfile('./data/sensors/' + self.name + '.json'):
            with open('./data/sensors/' + self.name + '.json', 'r') as f:
                self.data = json.load(f)
        
        else: #Create the file
            if not os.path.isdir('./data/sensors'):
                os.mkdir('./data/sensors/')
            self.data = []
            self.update_json()
            
    def append_data(self,data):
        current_unix_time = int(datetime.strftime(datetime.utcnow(), "%s"))
        if self.data is None:
            self.data = []
        self.data.append({'timestamp': current_unix_time, 'data': data})
        
    def update_json(self):
        with open('./data/sensors/' + self.name + '.json', 'w+') as f:
            json.dump(self.data, f)


    def get_most_recent_data(self):
        try:
            return self.data[-1]['data']
        except:
            return None