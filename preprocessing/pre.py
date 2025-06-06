import pandas as pd
import numpy as np

TrafficCounts = pd.read_csv("./csv/TrafficCounts.csv", skipinitialspace=True)
TrafficCounts = TrafficCounts.dropna(subset=['AADT_ALLVE'])

Scats = pd.read_csv("./csv/Scats.csv", skipinitialspace=True)

vNums = [f"V{str(i).zfill(2)}" for i in range(96)]

ScatsReformed = Scats.melt(
    id_vars=['SCATS Number', 'Location', 'Date', 'NB_LATITUDE' , 'NB_LONGITUDE'],
    value_vars=vNums,
    var_name='Interval',
    value_name='Volume'
)

ScatsReformed['Date'] = pd.to_datetime(ScatsReformed['Date'], dayfirst=True)
ScatsReformed['Interval'] = pd.Categorical(ScatsReformed['Interval'], categories=vNums, ordered=True)
ScatsReformed = ScatsReformed.sort_values(['Location', 'Date', 'Interval']).reset_index(drop=True)

ScatsReformed.to_csv("./csv/ScatsReformed.csv", index=False)