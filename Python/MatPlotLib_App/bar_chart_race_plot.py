import pandas as pd
import bar_chart_race as bcr
import matplotlib.pyplot as plt

#Documentation to install ffmpeg: https://phoenixnap.com/kb/ffmpeg-mac

languages = pd.read_csv("languages.csv",parse_dates=["Date"],index_col="Date")

languages.index = languages.index.to_period("M")

print(languages)

bcr.bar_chart_race(languages, # DataFrame
                   n_bars=10, # No. of Bars Should Be Shown
                   steps_per_period=130, #Animation Speed
                   period_length=125,
                   title="Most Popular Language",
                   figsize=(6,4),
                   filter_column_colors=True,
                   cmap=["forestgreen","skyblue"], # color
                   dpi= 400,
                   bar_label_size=5,#Values in Chart
                   tick_label_size=10, #Y Axis Label
                   filename="Sample.mp4"
                   )

