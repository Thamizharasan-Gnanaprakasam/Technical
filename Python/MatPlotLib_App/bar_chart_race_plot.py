import pandas as pd
import bar_chart_race as bcr
import matplotlib.pyplot as plt

#Documentation to install ffmpeg: https://trac.ffmpeg.org/wiki/CompilationGuide/macOS#ffmpegthroughHomebrew

languages = pd.read_csv("languages.csv",parse_dates=["Date"],index_col="Date")

print(languages)

bcr.bar_chart_race(languages.iloc[:10],
                   n_bars=10,
                   steps_per_period=130,
                   period_length=125,
                   title="Most Popular Language",
                   figsize=(6,4),
                   filter_column_colors=True,
                   )

plt.show()