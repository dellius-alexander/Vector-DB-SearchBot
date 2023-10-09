# hello_milvus.py demonstrates the basic operations of PyMilvus, a Python SDK of Milvus.
# 1. connect to Milvus
# 2. create collection
# 3. insert data
# 4. create index
# 5. search, query, and hybrid search on entities
# 6. delete entities by PK
# 7. drop collection
import json
import time

import numpy as np
from ..database.milvus import ConnectAPI, CollectionAPI
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from ..myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)

###################################################################################################
COLLECTION_NAME = "hello_milvus"

fmt = "\n========================================================================================\n{:30}" \
      "\n========================================================================================\n"
search_latency_fmt = "search latency = {:.4f}s"
num_entities, dim = 3000, 8

#################################################################################
# 1. connect to Milvus
# Add a new connection alias `default` for Milvus server in `localhost:19530`
# Actually the "default" alias is a buildin in PyMilvus.
# If the address of Milvus is the same as `localhost:19530`, you can omit all
# parameters and call the method as: `connections.connect()`.
#
# Note: the `using` parameter of the following methods is default to "default".
log.info(fmt.format("start connecting to Milvus"))
utility.connections.connect(alias='default',
                            host='127.0.0.1',
                            port='19530',
                            user='alpha',
                            password='developer')

has = utility.has_collection(COLLECTION_NAME)

# Remove collection if it already exists
if has:
    utility.drop_collection(COLLECTION_NAME)
    log.info(f"Collection \"{COLLECTION_NAME}\" exists. Removing collection \"{COLLECTION_NAME}\".")

else:
    log.info(f"Collection \"{COLLECTION_NAME}\" does not exist. Creating collection \"{COLLECTION_NAME}\".")

#################################################################################
# 2. create collection
# We're going to create a collection with 3 fields.
# +-+------------+------------+------------------+------------------------------+
# | | field name | field type | other attributes |       field description      |
# +-+------------+------------+------------------+------------------------------+
# |1|    "pk"    |   VarChar  |  is_primary=True |      "primary field"         |
# | |            |            |   auto_id=False  |                              |
# +-+------------+------------+------------------+------------------------------+
# |2|  "random"  |    Double  |                  |      "a double field"        |
# +-+------------+------------+------------------+------------------------------+
# |3|"embeddings"| FloatVector|     dim=8        |  "float vector with dim 8"   |
# +-+------------+------------+------------------+------------------------------+
fields = [
    FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100,
                description="primary key"),
    FieldSchema(name="random", dtype=DataType.DOUBLE),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim)
]

schema = CollectionSchema(fields=fields,
                          description=f"\"{COLLECTION_NAME}\" is the simplest demo to introduce the APIs")

log.info(fmt.format(f"Create collection \"{COLLECTION_NAME}\""))
hello_milvus = Collection(name=COLLECTION_NAME,
                          schema=schema,
                          using="default")

################################################################################
# 3. insert data
# We are going to insert 3000 rows of data into `hello_milvus`
# Data to be inserted must be organized in fields.
#
# The insert() method returns:
# - either automatically generated primary keys by Milvus if auto_id=True in the schema;
# - or the existing primary key field from the entities if auto_id=False in the schema.

log.info(fmt.format("Start inserting entities"))
rng = np.random.default_rng(seed=19530)
entities = [
    # provide the pk field because `auto_id` is set to False
    [str(i) for i in range(num_entities)],
    # size: (x) -> x: number of entities
    # field random, only supports list
    rng.random(size=num_entities).tolist(),
    # size: (x, y, z) -> x: number of entities, y: dimension of each entity, z: depth of each entity
    # field embeddings, supports numpy.ndarray and list
    rng.random(size=(num_entities, dim), dtype=float).tolist(),
]

log.info(f"Number of entities to be inserted: {len(entities[0])}")
log.info("\nEntities sample: \n")
for i in range(3):
    log.info(entities[i])
log.info(f"Number of entities in Milvus: {hello_milvus.num_entities}")

insert_result = hello_milvus.insert(entities)

log.info(f"Number of entities inserted: {len(insert_result.primary_keys)}")
log.info("Insert result sample: \n")
log.info(insert_result)

hello_milvus.flush()

log.info(f"Number of entities in Milvus: {hello_milvus.num_entities}")  # check the num_entites

################################################################################
# 4. create index
# We are going to create an IVF_FLAT index for hello_milvus collection.
# create_index() can only be applied to `FloatVector` and `BinaryVector` fields.
log.info(fmt.format("Start Creating index IVF_FLAT"))
index = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128},
}

hello_milvus.create_index("embeddings", index)

################################################################################
# 5. search, query, and hybrid search
# After data were inserted into Milvus and indexed, you can perform:
# - search based on vector similarity
# - query based on scalar filtering(boolean, int, etc.)
# - hybrid search based on vector similarity and scalar filtering.
#

# Before conducting a search or a query, you need to load the data in `hello_milvus` into memory.
log.info(fmt.format("Start loading"))
hello_milvus.load()

# -----------------------------------------------------------------------------
# search based on vector similarity
log.info(fmt.format("Start searching based on vector similarity"))
vectors_to_search = entities[-1][-2:]
search_params = {
    "metric_type": "L2",
    "params": {"nprobe": 10},
}

start_time = time.time()
result = hello_milvus.search(vectors_to_search, "embeddings", search_params, limit=3, output_fields=["random"])
end_time = time.time()

for hits in result:
    for hit in hits:
        log.info(f"hit: {hit}, random field: {hit.entity.get('random')}")
log.info(search_latency_fmt.format(end_time - start_time))

# -----------------------------------------------------------------------------
# query based on scalar filtering(boolean, int, etc.)
log.info(fmt.format("Start querying with `random > 0.5`"))

start_time = time.time()
result = hello_milvus.query(expr="random > 0.5", output_fields=["random", "embeddings"])
end_time = time.time()

log.info(f"query result:\n-{result[0]}")
log.info(search_latency_fmt.format(end_time - start_time))

# -----------------------------------------------------------------------------
# pagination
r1 = hello_milvus.query(expr="random > 0.5", limit=4, output_fields=["random"])
r2 = hello_milvus.query(expr="random > 0.5", offset=1, limit=3, output_fields=["random"])
log.info(f"query pagination(limit=4):\n\t{r1}")
log.info(f"query pagination(offset=1, limit=3):\n\t{r2}")

# -----------------------------------------------------------------------------
# hybrid search
log.info(fmt.format("Start hybrid searching with `random > 0.5`"))

start_time = time.time()
result = hello_milvus.search(vectors_to_search, "embeddings", search_params, limit=3, expr="random > 0.5",
                             output_fields=["random"])
end_time = time.time()

for hits in result:
    for hit in hits:
        log.info(f"hit: {hit}, random field: {hit.entity.get('random')}")
log.info(search_latency_fmt.format(end_time - start_time))

###############################################################################
# 6. delete entities by PK
# You can delete entities by their PK values using boolean expressions.

ids = insert_result.primary_keys

expr = f'pk in ["{ids[0]}" , "{ids[1]}"]'
log.info(fmt.format(f"Start deleting with expr `{expr}`"))

result = hello_milvus.query(expr=expr, output_fields=["random", "embeddings"])
log.info(fmt.format(f"query before delete by expr=`{expr}` -> result: \n-{result[0]}\n-{result[1]}\n"))

hello_milvus.delete(expr)

result = hello_milvus.query(expr=expr, output_fields=["random", "embeddings"])
log.info(fmt.format(f"query after delete by expr=`{expr}` -> result: {result}\n"))

###############################################################################
# 7. drop collection
# Finally, drop the hello_milvus collection
log.info(fmt.format(f"Drop collection `{COLLECTION_NAME}`"))
# utility.drop_collection(COLLECTION_NAME)
