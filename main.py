import requests
import json
from datetime import datetime
IPMA_URL = "http://api.ipma.pt/open-data/{}"

class IPMA:
    def __init__(self):
        self.ipma_url = IPMA_URL
        self.session = requests.Session()

    def getDistrits(self):
        r = self.session.get(self.ipma_url.format("distrits-islands.json"))
        return {i["local"]:i['globalIdLocal'] for i in r.json()["data"]}
    def getDistritID(self, distrit_name):
        r = self.session.get(self.ipma_url.format("distrits-islands.json"))
        return [i["globalIdLocal"] for i in r.json()["data"] if i["local"] == distrit_name][0]

    def getDistritName(self, distrit_id):
        r = self.session.get(self.ipma_url.format("distrits-islands.json"))
        return [i["local"] for i in r.json()["data"] if i["globalIdLocal"] == distrit_id][0]
    def getWindSpeed(self, class_wind_speed):
        r = self.session.get(self.ipma_url.format("wind-speed-daily-classe.json"))
        return [{"PT":i["descClassWindSpeedDailyPT"] ,"EN": i["descClassWindSpeedDailyEN"]} for i in r.json()["data"] if i["classWindSpeed"] == str(class_wind_speed)][0]

    def getWeather(self, weather_id):
        r = self.session.get(self.ipma_url.format("weather-type-classe.json"))
        return [{"PT":i["descWeatherTypePT"] ,"EN": i["descWeatherTypeEN"]} for i in r.json()["data"] if i["idWeatherType"] == weather_id][0]

    def getPrecipitation(self, precipitation_id):
        r = self.session.get(self.ipma_url.format("precipitation-classe.json"))
        return [{"PT":i["descClassPrecIntPT"] ,"EN": i["descClassPrecIntEN"]} for i in r.json()["data"] if i["classPrecInt"] == str(precipitation_id)][0]

    def getDaily(self, distrit_name):
        r = self.session.get(self.ipma_url.format("forecast/meteorology/cities/daily/{}.json".format(self.getDistritID(distrit_name))))
        weather_data = {distrit_name:{}}
        for i in r.json()["data"]:
            weather_data[distrit_name][i["forecastDate"]] = {
                "precipitaProb": i["precipitaProb"],
                "tAverage": (float(i["tMin"]) + float(i["tMax"]))/2,
                "tMin" : i["tMin"],
                "tMax" : i["tMax"],
                "precipitation": self.getPrecipitation(i["classPrecInt"]) if "classPrecInt" in i else None,
                "windSpeed": self.getWindSpeed(i["classWindSpeed"]),
                "weatherType": self.getWeather(i["idWeatherType"]),
            }

        return weather_data
    def getToday(self, distrit_name):
        today_date = datetime.today().strftime("%Y-%m-%d")
        weather_data = self.getDaily(distrit_name)
        return weather_data[distrit_name][today_date] if today_date in weather_data[distrit_name] else {"error": "No date for today"}

