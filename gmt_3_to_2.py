import pandas as pd
from datetime import timedelta

data = pd.read_csv("join_csv.csv")

# Convert timestamp column to datetime format
data["timestamp"] = pd.to_datetime(data["timestamp"])

# Shift time forward by one hour
# ...and if you wish, you can move in the other direction :)
data["timestamp"] = data["timestamp"] + timedelta(hours=1)

data.to_csv("join_csv_gmt2.csv", index=False)
