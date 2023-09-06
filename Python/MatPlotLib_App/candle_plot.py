import pandas as pd
import mplfinance as mpf

cols = ["date","open","close","high","low"]
data = pd.read_csv("AAPL.csv",usecols=cols,index_col="date",parse_dates=["date"])

year_2016 = data.loc["2016"]

print(year_2016)

mpf.plot(year_2016,
         type="candle",
         style="yahoo",
         title="Apple Stock",
         ylabel="Price $",
         #volume=True,
         figratio=(3,3))

mpf.show()