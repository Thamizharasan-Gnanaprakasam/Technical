import pandas as pd
import matplotlib.pyplot  as plt

cols = ["date","open","close","high","low"]
data = pd.read_csv("AAPL.csv",usecols=cols,index_col="date",parse_dates=["date"])

data.loc["2016-05"].plot(kind="line",
          xlabel="Year",
          ylabel="Stock Price $",
          y=["close","open"],
          color=["forestgreen","skyblue","crimson"],
          linewidth=2,
          marker='o',
          markersize=5,
          linestyle="solid")
"""
for style in plt.style.available:
    plt.style.use(style)
    print(style)
"""
plt.style.use("tableau-colorblind10")

plt.show()