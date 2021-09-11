from geopy import distance
import pandas as pd
import numpy as np

df = pd.read_csv('RA.csv')
n = len(df)
distances = np.zeros((n, n))

lat = df['lat'].to_numpy()
lon = df['lon'].to_numpy()

for i in range(n):
    for j in range(n):
        coords_1 = (lat[i], lon[i])
        coords_2 = (lat[j], lon[j])
        distances[i][j] = distance.distance(coords_1, coords_2).km

np.savetxt("distances.csv", distances, delimiter=",")