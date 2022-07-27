import json
from glob import glob
import pandas as pd
import numpy as np

df_historical = pd.read_csv("./data/historical.csv", parse_dates=["Date"]).loc[:,["Date",'Count']].dropna()

rows_updated = []
files = glob('./data/202*.json')
from datetime import datetime

def parse_date(date):
    try:
        d = datetime.strptime(date, '%B %d %Y')
    except:
        d = datetime.strptime(date, '%b %d %Y')
    return d

for file in files:
    with open (file) as f:
        rows_updated += json.load(f)

df_updated = pd.DataFrame(rows_updated).rename({"count" : "Count"}, axis = 1)
df_updated['date'] = (df_updated.apply(lambda x: f"{x['date']} {x.scrape_time_UTC[:4]}",axis=1))
df_updated['Count'] = df_updated['Count'].str.replace(",","").astype(float)
df_updated['date'] = df_updated['date'].apply(parse_date)
df_updated = df_updated.sort_values("scrape_time_UTC", ascending=True).groupby("date").last()
df_full = pd.DataFrame(data = {"Count" : np.nan} ,index = pd.date_range(start = df_historical.Date.min(), end=df_updated.index.max()))
df_full.fillna(df_historical.set_index("Date")).fillna(df_updated).to_csv("data/full_dataset.csv")
