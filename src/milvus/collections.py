from pymilvus import FieldSchema, CollectionSchema, DataType, Collection, list_resource_groups


# -------------------------------------------------------------------------------------------------
def get_simplified_nq_collection(collection_name: str,
                                 dimension: int = 768,
                                 segment_row_limit: int = 100) -> Collection:
    schema = get_collection_schema(
        collection_name=collection_name,
        fields=[
            FieldSchema(name='example_id', dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name='document_text', dtype=DataType.STRING),
            FieldSchema(name='long_answer_candidates', dtype=DataType.STRING, max_length=1000),
            FieldSchema(name='question_text', dtype=DataType.STRING),
            # annotations is a list of dictionaries
            FieldSchema(name='annotations', dtype=DataType.VARCHAR, max_length=1000),
            FieldSchema(name='document_url', dtype=DataType.VARCHAR, max_length=1000),

            FieldSchema(name='document_text_embedding', dtype=DataType.FLOAT_VECTOR, dim=dimension)
        ],
        segment_row_limit=segment_row_limit
    )
    return Collection(name=collection_name, schema=schema)


# -------------------------------------------------------------------------------------------------
def get_simplified_schema_collection(collection_name: str,
                                     dimension: int = 768,
                                     segment_row_limit: int = 100) -> Collection:
    schema = get_collection_schema(
        collection_name=collection_name,
        fields=[
            FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=200),
            # VARCHARS need a maximum length, so for this example they are set to 200 characters
            FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=dimension)
        ],
        segment_row_limit=segment_row_limit
    )
    return Collection(name=collection_name, schema=schema)


# -------------------------------------------------------------------------------------------------
def get_collection_from_schema(collection_name: str,
                               schema: CollectionSchema,
                               using: str = 'default', **kwargs) -> Collection:
    return Collection(name=collection_name, schema=schema, using=using, **kwargs)


# -------------------------------------------------------------------------------------------------
def get_collection_schema(collection_name: str, fields: list, segment_row_limit: int = 100) -> CollectionSchema:
    return CollectionSchema(
        collection_name=collection_name,
        fields=fields,
        segment_row_limit=segment_row_limit,
    )


# -------------------------------------------------------------------------------------------------
