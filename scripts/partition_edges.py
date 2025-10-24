import os
from fastparquet import ParquetFile, write
import numpy as np

NB_SHARDS = 8

pf = ParquetFile("data/silver/edges.parq")
df = pf.to_pandas()

for idx, shard in enumerate(np.array_split(df, NB_SHARDS)):
    os.mkdir(f"data/silver/shard_{idx:1d}")
    write(f"data/silver/shard_{idx}/edges.parq", shard)
