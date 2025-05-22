class BaseClass:
    data: dict = {}
    readings: list = []
    processed_data: list = []

    def __init__(self, data: dict):
        self.data = data
        self.readings = self.data.get("data", [])
