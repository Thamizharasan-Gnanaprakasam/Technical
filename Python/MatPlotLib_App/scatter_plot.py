import pandas as pd
import matplotlib.pyplot  as plt

cols = ["date","open","close","high","low"]
data = pd.read_csv("AAPL.csv",usecols=cols,index_col="date",parse_dates=["date"])

data1 = data.resample("a").mean()

data1.index = data1.index.year

data1.plot(kind="scatter",
           x="high",
           y="open")

plt.show()