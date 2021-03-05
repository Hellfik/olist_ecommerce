import pandas as pd

geolocation_dataset = pd.read_csv("datasets/olist_geolocation_dataset.csv")

geolocation_dataframe = pd.DataFrame(geolocation_dataset)

print(geolocation_dataframe)


