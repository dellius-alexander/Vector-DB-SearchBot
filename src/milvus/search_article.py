# Searh article in Medium
# 0. Overview
#
# We'll search for text in the Medium dataset, and it will find the most similar results to the search text across
# all titles. Searching for articles is different from traditional keyword searches, which search for semantically
# relevant content. If you search for "funny python demo" it will return "Python Coding for Kids - Setting Up For the
# Adventure", not "No key words about funny python demo".
#
# We will use Milvus and Towhee to help searches. Towhee is used to extract the semantics of the text and return the
# text embedding. The Milvus vector database can store and search vectors, and return related articles. So we first
# need to install Milvus and Towhee:
#
# Please start Milvus server first
import traceback
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

import os
import timeit
import pandas as pd
import numpy as np
from utils.request_types import request_get
from myLogger.Logger import getLogger as GetLogger

log = GetLogger(__file__)


# -----------------------------------------------------------------------------
def create_milvus_collection(collection_name, dim):
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="title_vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="link", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="reading_time", dtype=DataType.INT64),
        FieldSchema(name="publication", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="claps", dtype=DataType.INT64),
        FieldSchema(name="responses", dtype=DataType.VARCHAR, max_length=500)
    ]
    schema = CollectionSchema(fields=fields, description='search text')
    _collection = Collection(name=collection_name, schema=schema)

    index_params = {
        'metric_type': "L2",
        'index_type': "IVF_FLAT",
        'params': {"nlist": 2048}
    }
    _collection.create_index(field_name='title_vector', index_params=index_params)
    return _collection


# -----------------------------------------------------------------------------


try:
    print('Start search article')
    # 1. Connect to Milvus
    connections.connect(alias='default',
                        user='alpha',
                        password='developer',
                        host='127.0.0.1',
                        port='19530')

    fmt = "\n{:30}\n"
    # get the project root directory
    ROOT_DIR = '..'
    url = 'https://github.com/dellius-alexander/Project-Datasets-Repo/raw/main/datasets/CSV' \
          '/cleaned_medium_article_dataset.csv'
    file_path = f'{ROOT_DIR}/Resources/datasets/cleaned-medium-articles-dataset.csv'
    print(file_path)
    if not os.path.exists(file_path):
        request_get(url=url, ext_file_location=file_path)
        print('Downloading dataset file')
    else:
        print('Dataset file exists')

    # 1. Data preprocessing
    #
    # The data is from the Cleaned Medium Articles Dataset(you can download it from Kaggle), which cleared the empty
    # article titles in the data and conver the string title to the embeeding with Towhee text_embedding.dpr operator,
    # as you can see the title_vector is the embedding vectors of the title.

    df = pd.read_csv(file_path, converters={'title_vector': lambda x: eval(x)})
    head = df.head()
    print(df.head(10))
    print(df.info())
    print(df.describe())
    print(df.dtypes)
    print(f'Shape: {df.shape}')

    # 2. Load Data
    #
    # The next step is to get the text embedding, and then insert all the extracted embedding vectors into Milvus.
    # Create Milvus Collection
    #
    # We need to create a collection in Milvus first, which contains multiple fields of id, title, title_vector, link,
    # reading_time, publication, claps and responses.

    collection = create_milvus_collection('search_article_in_medium', 768)
    print(collection)
    # start = timeit.default_timer()
    # Convert data in title_vector column to two-dimensional list in float format
    # df['title_vector'] = df['title_vector'].apply(lambda x: list(map(float, x[1:-1].split(','))))
    # insert all the fields into Milvus
    # status, ids = collection.insert(collection_name='search_article_in_medium',
    #                                 data=df,
    #                                 ids=None)
    # print(status)
    # print(ids)
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)
    #
    # exit(0)
    # Data to Milvus
    #
    # Towhee supports reading df data through the from_df interface, and then we need to convert the title_vector column
    # in the data to a two-dimensional list in float format, and then insert all the fields into Milvus, each field
    # inserted into Milvus corresponds to one Collection fields created earlier.
    ###############################################################################################
    # from towhee import ops, pipe, DataCollection

    insert_pipe = (pipe.input('df')
                   .flat_map('df', 'data', lambda df: df.values.tolist())
                   .map('data', 'res',
                        ops.ann_insert.milvus_client(
                            host='127.0.0.1',
                            port='19530',
                            collection_name='search_article_in_medium'))
                   .output('res')
                   )

    start = timeit.default_timer()
    _ = insert_pipe(df)
    print(_)
    stop = timeit.default_timer()
    print('Time: ', stop - start)

    # We need to call collection.load() to load the data after inserting the data, then run collection.num_entities to
    # get the number of vectors in the collection. We will see the number of vectors is 5979, and we have successfully
    # load the data to Milvus.

    collection.load()
    print(collection.num_entities)

    # 3. Search embedding title
    # Search one text in Milvus
    #
    # The retrieval process also to generate the text embedding of the query text, then search for similar vectors in
    # Milvus, and finally return the result, which contains id(primary_key) and score. For example, we can search for
    # "funny python demo":

    search_pipe = (pipe.input('query')
                   .map('query', 'vec', ops.text_embedding.dpr(model_name="facebook/dpr-ctx_encoder-single-nq-base"))
                   .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
                   .flat_map('vec', ('id', 'score'), ops.ann_search.milvus_client(host='127.0.0.1',
                                                                                  port='19530',
                                                                                  collection_name='search_article_in_medium'))
                   .output('query', 'id', 'score')
                   )

    res = search_pipe('funny python demo')
    DataCollection(res).show()

    # Search multi text in Milvus
    #
    # We can also retrieve multiple pieces of data, for example we can specify the array(['funny python demo',
    # 'AI in data analysis']) to search in batch, which will be retrieved in Milvus:

    res = search_pipe.batch(['funny python demo', 'AI in data analysis'])
    for re in res:
        DataCollection(re).show()

    # Search text and return multi fields
    #
    # If we want to return more information when retrieving, we can set the output_fields parameter in
    # ann_search.milvus operator. For example, in addition to id and score, we can also return title, link, claps,
    # reading_time, and response:

    search_pipe1 = (pipe.input('query')
                    .map('query', 'vec', ops.text_embedding.dpr(model_name="facebook/dpr-ctx_encoder-single-nq-base"))
                    .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
                    .flat_map('vec', ('id', 'score', 'title'), ops.ann_search.milvus_client(host='127.0.0.1',
                                                                                            port='19530',
                                                                                            collection_name='search_article_in_medium',
                                                                                            output_fields=['title']))
                    .output('query', 'id', 'score', 'title')
                    )

    res = search_pipe1('funny python demo')
    DataCollection(res).show()

    # milvus search with multi outpt fields
    search_pipe2 = (pipe.input('query')
                    .map('query', 'vec', ops.text_embedding.dpr(model_name="facebook/dpr-ctx_encoder-single-nq-base"))
                    .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
                    .flat_map('vec',
                              ('id', 'score', 'title', 'link', 'reading_time', 'publication', 'claps', 'responses'),
                              ops.ann_search.milvus_client(host='127.0.0.1',
                                                           port='19530',
                                                           collection_name='search_article_in_medium',
                                                           output_fields=['title', 'link', 'reading_time',
                                                                          'publication', 'claps', 'responses'],
                                                           limit=5))
                    .output('query', 'id', 'score', 'title', 'link', 'reading_time', 'publication', 'claps',
                            'responses')
                    )

    res = search_pipe2('funny python demo')
    DataCollection(res).show()

    # Search text with some expr
    #
    # In addition, we can also set some expressions for retrieval. For example, we can specify that the beginning of the
    # article is an article in Python by setting expr='title like "Python%"':

    search_pipe3 = (pipe.input('query')
                    .map('query', 'vec', ops.text_embedding.dpr(model_name="facebook/dpr-ctx_encoder-single-nq-base"))
                    .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
                    .flat_map('vec',
                              ('id', 'score', 'title', 'link', 'reading_time', 'publication', 'claps', 'responses'),
                              ops.ann_search.milvus_client(host='127.0.0.1',
                                                           port='19530',
                                                           collection_name='search_article_in_medium',
                                                           expr='title like "Python%"',
                                                           output_fields=['title', 'link', 'reading_time',
                                                                          'publication', 'claps', 'responses'],
                                                           limit=5))
                    .output('query', 'id', 'score', 'title', 'link', 'reading_time', 'publication', 'claps',
                            'responses')
                    )

    res = search_pipe3('funny python demo')
    DataCollection(res).show()

    # 4. Query data in Milvus
    #
    # We have done the text retrieval process before, and we can get articles such as "Python coding for kids - getting
    # ready for an adventure" by retrieving "fun python demos".
    #
    # We can also do a simple query on the data, we need to set expr and output_fields with the collection.query
    # interface, for example, we can filter out articles with faults greater than 300 and reading time less than 15
    # minutes, and submitted to TDS :

    results = collection.query(
        expr='claps > 3000 && reading_time < 15 && publication like "Towards Data Science%"',
        output_fields=['id', 'title', 'link', 'reading_time', 'publication', 'claps', 'responses'],
        consistency_level='Strong'
    )

    print(results)
except Exception as e:
    print(f'Error: \n{e}')
    print(f'Error: \n{traceback.format_exc()}')
