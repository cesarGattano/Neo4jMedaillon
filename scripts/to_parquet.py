from fastparquet import write
from pandas import read_csv

df = read_csv("data/raw/nodes.csv")
write("data/bronze/nodes.parq", df)

df = read_csv("data/raw/edges.csv")
write("data/bronze/edges.parq", df)
