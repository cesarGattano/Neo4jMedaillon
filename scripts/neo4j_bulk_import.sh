#!/bin/bash

neo4j-admin database import full --nodes data/gold/nodeS.csv --relationships data/gold/shard_\d+\/edges.csv neo4j

exit 0