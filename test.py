from datetime import datetime
from main import IPMA

#Get the weather from the IPMA API for today in Leiria
weather_test = IPMA()
weather_data = weather_test.getDaily("Leiria")
print(weather_data["Leiria"][datetime.today().strftime("%Y-%m-%d")]["weatherType"]["PT"])
