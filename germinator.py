from datetime import datetime, timedelta

class Germinator:
    data: dict = {}
    readings: list = []
    processed_data: list = []

    def __init__(self, data: dict = {}):
        self.data = data
        self.readings = self.data.get("data", [])
        self.__process_data()

    def __process_data(self):
        for reading in self.readings:
            created = reading.get("created_date")
            offset = timedelta(hours=-4)
            timestamp = datetime.fromisoformat(created.replace('Z', '+00:00')) + offset
        
            entry = {
                "timestamp": timestamp,
                "lights_on": reading["data"]["lights"],
                "soil_temp": reading["data"]["soil"]["soil_temp"],
                "soil_moisture": reading["data"]["soil"]["moisture"],
                "humidity_actual": reading["data"]["air"]["humidity"]["actual"],
                "humidity_target_low": reading["data"]["air"]["humidity"]["target"][0],
                "humidity_target_high": reading["data"]["air"]["humidity"]["target"][1],
                "temp_actual": reading["data"]["air"]["temperature"]["actual"],
                "temp_target_low": reading["data"]["air"]["temperature"]["target"][0],
                "temp_target_high": reading["data"]["air"]["temperature"]["target"][1]
            }
            self.processed_data.append(entry)
