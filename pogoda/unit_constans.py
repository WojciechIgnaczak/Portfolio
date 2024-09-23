class Unit_and_Constans:
    def __init__(self):
        pass

    def FtoC(self, tempF): # konwercja stopni Fahrenhait'a na Celsjusza
        try:
            return round((tempF - 32) / 1.8)
        except TypeError as e: print(f"Unit conversion in Fahrenhait to Celsjusz error: {e}") 

    def Mph_to_kmh(self, mph): # konwersja mil na godzine na kilometry na godzine
        try:
            return round(mph / 1.609344)
        except TypeError as e: print(f"Unit conversion in Mph to Kmh error: {e}") 

    def Cal_to_mm(self,opad): # konwersja cali na milimetry
        try:
            return round(opad/0.039370,1)
        except TypeError as e: print(f"Unit conversion error in cal to mm: {e}") 

    def wind_degrees(self, wind): # kąty wiatru a kierunek wiania
        wind=round(wind)
        directions = {
            (0, 33): "N", (34, 78): "NE", (79, 123): "E",
            (124, 168): "SE", (169, 213): "S", (214, 258): "SW",
            (259, 303): "W", (304, 348): "NW", (349, 360): "N"
        }
        for (low, high), direction in directions.items():
            if low <= wind <= high:
                return direction
        return "Unknown"