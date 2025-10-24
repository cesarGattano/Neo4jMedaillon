import os
from dotenv import load_dotenv
from fastparquet import ParquetFile

load_dotenv()

# Prepare nodes.csv
pf = ParquetFile("data/silver/nodes.parq")
df = pf.to_pandas()
df.rename(columns={"id": "id:ID", "label": ":LABEL"}, inplace=True)
df.to_csv("data/gold/nodes.csv", index=False)

# Prepare shard_?/edges.csv
for i in range(int(os.environ["NB_SHARDS"])):
    pf = ParquetFile(f"data/silver/shard_{i}/edges.parq")
    df = pf.to_pandas()
    df.rename(
        columns={"src": ":START_ID", "dst": ":END_ID", "type": ":TYPE"}, inplace=True
    )
    os.mkdir(f"data/gold/shard_{i}")
    df.to_csv(f"data/gold/shard_{i}/edges.csv", index=False)
