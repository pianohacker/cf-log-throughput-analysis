import matplotlib.pyplot as plt
import matplotlib.ticker
import mplcursors
import numpy as np
import pandas as pd
import re
import seaborn
import sys

filename = sys.argv[1]

data = pd.read_json(filename, lines = True)

df = data.groupby('source').mean()
df = df[df > 0].dropna()
df["source_type"] = df.index.map(lambda source: 'app' if re.match(r'^........-....-....-....-............$', source) else 'platform')
print(df)

def add_quantiles(rates, color = ''):
    quantiles = [0.01, 0.1, 0.5, 0.9, 0.99]
    quantile_positions = rates.quantile(quantiles)

    ax = plt.gca()
    y_min, y_max = ax.get_ylim()
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:.1f}'))
    ax.get_xaxis().set_major_locator(matplotlib.ticker.FixedLocator(quantile_positions))
    ax.get_yaxis().set_visible(False)

    for q, x in zip(quantiles, quantile_positions):
        plt.axvline(x, color="black")
        plt.annotate(xy = (x, 1), xycoords = ax.get_xaxis_transform(), text = "{:.0f}%".format(q *
            100), xytext = (0, 10), textcoords='offset pixels',
            horizontalalignment = 'center')

    ax.set_title(ax.get_title(), pad = 20)

g = seaborn.displot(df, row = "source_type", kind = 'kde', x = 'rate', log_scale =
        True, common_norm = False, bw_adjust = .5, facet_kws = dict(sharex = False)).map(add_quantiles, 'rate')
g.fig.subplots_adjust(top = 0.9, wspace = 0, hspace = 0.2)

mplcursors.cursor(hover=True)
plt.show()
