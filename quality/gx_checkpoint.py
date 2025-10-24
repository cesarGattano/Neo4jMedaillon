import great_expectations as gx
import pandas as pd
from fastparquet import ParquetFile, write

# Data context
context = gx.get_context()

# Data source
data_source_name = "neo4jmedaillon"
data_source = context.data_sources.add_pandas(data_source_name)

# Data asset
data_asset_name = "bronze"
data_asset = data_source.add_dataframe_asset(name=data_asset_name)

# Batch definition: quality assessment of nodes.parq
batch_def_name = "quality assessment of nodes"
batch_def = data_asset.add_batch_definition_whole_dataframe(batch_def_name)

# Expectation
pf = ParquetFile("data/bronze/nodes.parq")
df = pf.to_pandas()
batch = batch_def.get_batch(batch_parameters={"dataframe": df})
expectation = gx.expectations.ExpectColumnValuesToBeUnique(
    column="id", severity="critical"
)

# Test expectation
validation_result = batch.validate(expectation)

# Nettoyage
if not validation_result["success"]:
    df.drop_duplicates(subset="id", keep="first", inplace=True)

# Stockage
write("data/silver/nodes.parq", df)

# Batch definition: quality assessment of edges.parq
batch_def_name = "quality assessment of edges"
batch_def = data_asset.add_batch_definition_whole_dataframe(batch_def_name)

# Expectation
pf = ParquetFile("data/bronze/edges.parq")
df = pf.to_pandas()
batch = batch_def.get_batch(batch_parameters={"dataframe": df})
expectation = gx.expectations.ExpectColumnValuesToNotBeNull(
    column="src", severity="critical"
)

# Test expectation
validation_result1 = batch.validate(expectation)
print(validation_result1)

# Expectation
expectation = gx.expectations.ExpectColumnValuesToNotBeNull(
    column="dst", severity="critical"
)

# Test expectation
validation_result2 = batch.validate(expectation)
print(validation_result2)

# Nettoyage
if not validation_result1["success"] or not validation_result2["success"]:
    df.dropna(axis="index", how="any", subset=["src", "dst"], inplace=True)

# Stockage
write("data/silver/edges.parq", df)
