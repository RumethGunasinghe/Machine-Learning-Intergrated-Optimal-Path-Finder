import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from Classes.Node import Node
from Classes.Location import Location 
from Classes.Graph import Graph
import pandas as pd
import numpy as np
import math

from models.GRU import GRU_Model
from models.LSTM import LSTM_Model
from models.RandomForest import RF_Model

from haversine import haversine, Unit


def findTime(location_name, input_model , currentNode , neighbourNode, TOD):
    X, y, scaler, TOD = preprocessing("./csv/ScatsReformed.csv", location_name, 10, TOD)

    if input_model == 1:
        prediction = LSTM_Model(X, y, scaler)
    elif input_model == 2:
        prediction = GRU_Model(X, y, scaler)
    elif input_model == 3:
        prediction = RF_Model(X, y, scaler)

    predicted_speed = flow_to_speed(prediction)

    current_coords = (currentNode.latitude, currentNode.longitude)
    neighbour_coords = (neighbourNode.latitude, neighbourNode.longitude)

    predicted_time, distance = speed_to_time(predicted_speed, current_coords, neighbour_coords)
    return(predicted_time)



def preprocessing(csv, location, lookback=10, TOD=""):
        df = pd.read_csv(csv)
    
        if TOD == "Morning":
            cols = [f"V{str(i).zfill(2)}" for i in range(0, 32)]
        elif TOD == "Afternoon":
            cols = [f"V{str(i).zfill(2)}" for i in range(32, 64)]
        elif TOD == "Night":
            cols = [f"V{str(i).zfill(2)}" for i in range(64, 95)]
        else:
            cols = [f"V{str(i).zfill(2)}" for i in range(0, 95)]


        # print("Available locations:", df["Location"].unique())
        # print("Checking for location:", location)
        # print("Available intervals:", df["Interval"].unique())
        # print("Filtering for intervals:", cols)


        filtered_df = df[(df["Location"] == location) & (df["Interval"].isin(cols))].sort_values(by=["Date", "Interval"])
        
        if filtered_df.empty:
            raise ValueError("file path is empty, no rows in csv")
        
        print(TOD)   
        scaler = MinMaxScaler()

        filtered_df["ScaledVolume"] = scaler.fit_transform(filtered_df[['Volume']])

        data = filtered_df["ScaledVolume"].values
        X = []
        y = []

        for i in range(len(data) - lookback):
            X.append(data[i:i + lookback])
            y.append(data[i + lookback])

        X = np.array(X).reshape(-1, lookback, 1)
        y = np.array(y)

        return X, y, scaler, TOD


def flow_to_speed(flow_15min):
    flow_hr = flow_15min * 4  # Convert to vehicles/hour

    # Use the same traffic model
    a = -1.4648375
    b = 93.75
    c = -flow_hr

    if flow_hr > 1500:
        return 32 * 0.25  # return min speed in km/15min

    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None

    sqrt_disc = math.sqrt(discriminant)
    speed_kmh = (-b - sqrt_disc) / (2*a)

    if 0 < speed_kmh <= 60:
        return speed_kmh * 0.25  # Convert to km/15min
    else:
        return 60 * 0.25  # Cap to 15 km/15min


    
def speed_to_time(speed, loc1, loc2): # pass in current coords and neighbour coords

    distance = haversine(loc1, loc2, unit=Unit.KILOMETERS)
    if speed == 0 or speed is None:
        return float("inf"), float("inf")  # Avoid division by zero or no solution
    else:
        time = distance / speed * 15  # in minutes (15 min blocks)
        return time, distance

