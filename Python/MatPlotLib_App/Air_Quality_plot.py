import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

cols=["Country","City","AQI Value","AQI Category"]
data = pd.read_csv("gap.csv",usecols=cols)

data.sort_values(by="AQI Value",inplace=True)

print(data)

countries = data.groupby(by="Country")

average = countries.mean(numeric_only=True).round(2)

print(average)

def colors(value: int) -> str:
    if value<50:
        return "forestgreen"
    elif value<100:
        return "orange"
    else:
        return "crimson"

country_colors = average["AQI Value"].apply(colors)

print(country_colors.values)

average.plot(kind="barh",
             color=country_colors.values,
             y="AQI Value",
             ylabel="Country",
             xlabel="AQI Value")

good = Patch(color="forestgreen", label="Good")
ok = Patch(color="orange", label="Okay")
bad = Patch(color="crimson", label="Bad")

plt.legend(handles=[good,ok,bad])

plt.show()

