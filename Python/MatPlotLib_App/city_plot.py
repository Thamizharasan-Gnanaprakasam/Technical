import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

cols=["Country","City","AQI Value","AQI Category"]
data = pd.read_csv("gap.csv",usecols=cols)

data.sort_values(by="AQI Value",inplace=True)

print(data)

countries = data.groupby(by="Country")

india = countries.get_group("Peru")

def colors(value: int) -> str:
    if value<50:
        return "forestgreen"
    elif value<100:
        return "orange"
    else:
        return "crimson"

city_colors = india["AQI Value"].apply(colors)

print(city_colors)

india.plot(kind="barh",
           y="AQI Value",
           x="City",
           color=city_colors.values)

plt.show()
