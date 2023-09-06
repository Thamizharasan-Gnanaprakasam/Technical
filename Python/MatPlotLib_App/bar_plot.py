import pandas as pd
import matplotlib.pyplot  as plt

cols = ["date","open","close","high","low"]
data = pd.read_csv("AAPL.csv",usecols=cols,index_col="date",parse_dates=["date"])

data1 = data.resample("a").mean()

data1.index = data1.index.year

print(data1)

data1.plot(kind="bar",
           xlabel="Year",
           ylabel="Stock Price $",
           color=["forestgreen","skyblue","blue","crimson"])

plt.show()