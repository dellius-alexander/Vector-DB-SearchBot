import json
import math
from typing import List

import nltk
import numpy as np
from gensim.models import Word2Vec
from nltk import word_tokenize
from nltk.internals import Counter
from pymilvus import Collection, FieldSchema, DataType, CollectionSchema
from sklearn.preprocessing import OneHotEncoder

from src.database.milvus import ConnectAPI, MilvusAPI, CollectionAPI, IndexAPI
from src.utils.embedding import  clean_text, chunk_the_text
from src.utils.decoders import WordDecoder
from src.utils.encoders import WordEncoder


def init_collection(collection_name: str, fields: List[FieldSchema]) -> Collection:
    schema = CollectionSchema(fields=fields, description="test collection")
    return Collection(name=collection_name, schema=schema)


def test_milvus_api():
    collection_name = "test_milvus_api"
    client: MilvusAPI = MilvusAPI(alias="default", host='127.0.0.1', port='19530', user='milvus', password='developer')
    print("\nCollection name: ")
    print(collection_name)
    print("\nStored Collections: ")
    print(json.dumps(client.list_collections(), indent=2))
    if client.has_collection(collection_name=collection_name):
        client.drop_collection(collection_name=collection_name)

    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False,
                    description="primary key", max_length=100),
        FieldSchema(name="random", dtype=DataType.INT64),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=(768))
    ]

    collection: Collection = init_collection(collection_name, fields=fields)
    print("\nSchema: ")
    print(collection.schema)
    print(collection)
    print("\nCollections: ")
    print(json.dumps(client.list_collections(), indent=2))
    if client.has_collection(collection_name=collection_name):
        assert collection_name in client.list_collections()
        client.drop_collection(collection_name=collection_name)
    print("\nCollections: ")
    print(json.dumps(client.list_collections(), indent=2))


def test_connect_api():
    collection_name = 'test_collection'
    client = ConnectAPI(alias="default", host='127.0.0.1', port='19530', user='milvus', password='developer') \
        .get_client()
    print("\nClient: ")
    print(json.dumps(dir(client), indent=2))
    if client.has_collection(collection_name=collection_name):
        client.drop_collection(collection_name=collection_name)
    # initialize a collection
    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False,
                    description="primary key", max_length=100),
        FieldSchema(name="random", dtype=DataType.INT64),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=(768))
    ]
    collection: Collection = init_collection(collection_name, fields=fields)
    # client.create_collection(collection=collection)
    print("\nSchema: ")
    print(collection.schema)
    print("\nCollections: ")
    print(json.dumps(client.list_collections(), indent=2))
    if client.has_collection(collection_name=collection_name):
        print("\nCollections: ")
        print(json.dumps(client.list_collections(), indent=2))
        assert collection_name in client.list_collections()
        client.drop_collection(collection_name=collection_name)
    else:
        print("\nCollections: ")
        print(json.dumps(client.list_collections(), indent=2))
        assert collection_name not in client.list_collections()
    print("\nVerfy collection dropped: ")
    assert collection_name not in client.list_collections()
    print(json.dumps(client.list_collections(), indent=2))


# Test the CollectionAPI
def test_collection_api():
    collection_name = "test_collection_api"
    client: CollectionAPI = CollectionAPI(alias="default", host='127.0.0.1', port='19530', user='milvus', password='')
    print("\nCollection name: ")
    print(collection_name)
    print("\nStored Collections: ")
    print(json.dumps(client.list_collections(), indent=2))
    if client.has_collection(collection_name=collection_name):
        client.drop_collection(collection_name=collection_name)

    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False,
                    description="primary key", max_length=100),
        FieldSchema(name="random", dtype=DataType.INT64),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=(768))
    ]

    collection: Collection = init_collection(collection_name, fields=fields)
    # collection.create_index(field_name="embeddings", index_params={"metric_type": "L2"})
    # client.create_collection(collection=collection)
    print("\nCollection: ")
    print(collection)
    print("\nCollections: ")
    print(json.dumps(client.list_collections(), indent=2))
    if client.has_collection(collection_name=collection_name):
        assert collection_name in client.list_collections()
        client.drop_collection(collection_name=collection_name)
    print("\nCollections: ")
    print(json.dumps(client.list_collections(), indent=2))


# Test the IndexAPI
def test_index_api():
    collection_name = "test_index_api"
    index_params = {
        'metric_type': 'L2',
        'index_type': "IVF_FLAT",
        'params': {"nlist": 2048}
    }

    client: IndexAPI = IndexAPI(alias="default", host='127.0.0.1', port='19530', user='milvus', password='',
                                index_params=index_params)

    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False,
                    description="primary key", max_length=100),
        FieldSchema(name="random", dtype=DataType.INT64),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=(768))
    ]
    schema = CollectionSchema(fields=fields, description=collection_name)
    collection = Collection(name=collection_name, schema=schema)
    print("\nCollection: ")
    print(collection)
    results = client.create_index(field_name="embeddings", collection_name=collection_name, schema=schema,
                                  index_params=index_params)
    print("\nResults: ")
    print(results)


def test_create_embeddings():
    text = """Webpack v5 comes with the latest terser-webpack-plugin out of the box. If you are using Webpack v5 or  \
           "above and wish to customize the options, you will still need to install terser-webpack-plugin. Using  \
           "Webpack v4, you have to install terser-webpack-plugin v4."""
    cleaned_text = clean_text(text)
    print("\nCleaned text: ")
    print(cleaned_text.split())
    model = Word2Vec([cleaned_text.split()], min_count=1, vector_size=768, window=5, workers=3)
    text_vector = model.wv.get_vector("webpack")
    print("\nText vector: ")
    print(text_vector)
    print("\nText vector shape: ")
    print(text_vector.shape)
    # normalize the vector
    temp_text_vector = np.zeros(text_vector.shape)
    # vector_sum = sum([abs(a) for a in text_vector.sum(axis=0)])
    vector_sum = deep_sum(text_vector)
    print("\nVector sum: ")
    print(vector_sum)
    print(sum(abs(text_vector)))
    if vector_sum < 1:
        vector_sum = 1
    for i, vec in enumerate(text_vector):
        temp_vec = vec / vector_sum
        print("\nVec: ")
        print(temp_vec)
        temp_text_vector[i] = temp_vec
    text_vector = temp_text_vector
    print("\nNormalize Text vector: ")
    print(text_vector)
    print("\nText vector shape: ")
    print(text_vector.shape)


# recursively sum all numbers in a vector
def deep_sum(vector):
    vec_sum = 0
    vector = abs(vector)
    if isinstance(vector, (list, tuple, np.ndarray)):
        for i, vec in enumerate(vector):
            if isinstance(vec, (list, tuple, np.ndarray)):
                return deep_sum(vec)
            else:
                vec_sum += abs(vec)
    else:
        vec_sum += abs(vector)
    return vec_sum


def test_encode_word(word="webpack"):
    # Create a list of characters to store the characters of the given word
    characters = []
    # Iterate through each character in the given word
    for char in word:
        # Append the ASCII value of each character to the list
        _ord = ord(char)
        print("\nOrd: ")
        print(_ord)
        characters.append(_ord)
    # Create a list of floats to store the floating point numbers
    floats = []
    # Iterate through each character in the list of characters
    for char in characters:
        # Calculate the floating point number from the ASCII value
        float_val = float(char) / 256
        # Append the floating point number to the list
        floats.append(float_val)
    # Return the list of floats
    print("\nFloats: ")
    print(floats)


def test_decode_word(floats=None):
    # Create a list of characters to store the decoded characters
    if floats is None:
        # floats = "webpack"
        floats = [0.46484375, 0.39453125, 0.3828125, 0.4375, 0.37890625, 0.38671875, 0.41796875]
    characters = []
    # Iterate through each float in the list of floats
    for float_val in floats:
        # Calculate the ASCII value from the float
        char_val = int(float_val * 256)
        # Append the decoded character to the list
        characters.append(chr(char_val))
    # Join the characters to form the decoded word
    decoded_word = ''.join(characters)
    # Return the decoded word
    print("\nDecoded word: ")
    print(decoded_word)


def test_word_encoder(word="melody is my love!"):
    # Test
    print("\nWord: ")
    print(word)
    encode_word = WordEncoder(word)
    print("\nEncode word: ")
    # assert encode_word.encode() == encode_word.encode()
    print(encode_word.encode())  # [0.46484375, 0.39453125, 0.3828125, 0.4375, 0.37890625, 0.38671875, 0.41796875]
    # Return the resized and reshaped list of floats
    cols = 7
    rows = len(encode_word.encoded_word) // cols
    print("\nResized and reshaped floats: ")
    # assert encode_word.resize_and_reshape(2) == encode_word.resize_and_reshape(2)
    print(encode_word.resize_and_reshape((4, cols)))  # [[0.46484375, 0.39453125]]
    # print("\nResized and reshaped floats: ")
    # print(encode_word.resize_and_reshape((2, 5)))  # [[0.46484375, 0.39453125], [0.3828125, 0.4375], [0.37890625]]
    print("\nNormalized floats: ")
    print(encode_word.normalize())  # [0.16234652114597545, 0.1377899045020464, 0.13369713506139155,
    # 0.15279672578444747, 0.13233287858117326, 0.13506139154160982, 0.14597544338335608]
    print("\nUn-normalized floats: ")
    print(encode_word.un_normalize())  # [0.46484375, 0.39453125000000006, 0.38281250000000006, 0.4375, 0.37890625,
    # 0.38671875, 0.41796875]
    print("\nEncrypted floats: ")
    print(encode_word.encrypt())  # [0.39870500981447843, 0.3383966890022044, 0.3283453022001587, 0.3752517739430385,
    # 0.32499483993281014, 0.33169576446750726, 0.3584994626062957]
    print("\nDecrypted floats: ")
    print(encode_word.decrypt())  # [0.46484375000000006, 0.39453125, 0.3828125, 0.4375, 0.37890625, 0.38671875,
    # 0.41796875]
    decode_word = WordDecoder(encode_word.encode())
    print("\nDecoded floats to word: ")
    print(decode_word.decode())  # webpack
    decode_word = WordDecoder(encode_word.un_normalize())
    print("\nNormalized decoded floats to word: ")
    print(decode_word.decode())  # webpack
    print("\nEncoded object: ")
    print(json.dumps(encode_word.__dict__(), indent=2))
    print("\nEncoded object state: ")
    print(json.dumps(encode_word.__getstate__().__str__(), indent=2))
    print("\nDecoded object: ")
    print(json.dumps(decode_word.__dict__(), indent=2))


def calculate_IDF(tokens, unique_tokens):
    idf_values = {}
    for token in unique_tokens:
        contains_token = sum([1 for text in tokens if token in text])
        idf_values[token] = 1 + math.log((len(tokens) + 1) / (contains_token + 1))
    return idf_values


def test_calculate_floating_vector(text="melody is my love!"):
    nltk.download('punkt')
    # Tokenization
    tokens = word_tokenize(text)
    print("\nTokens: ")
    print(tokens)

    # One-Hot Encoding
    enc = OneHotEncoder(handle_unknown="ignore")
    enc.fit(tokens)
    encoded_data = enc.transform(tokens).toarray()
    print("\nOne-Hot Encoding: ")
    print(encoded_data)

    # Calculate Term Frequency
    term_frequency = Counter(tokens)
    print("\nTerm Frequency: ")
    print(term_frequency)

    # Calculate Inverse Document Frequency
    unique_tokens = list(set(tokens))
    idf_values = calculate_IDF(tokens, unique_tokens)
    print("\nInverse Document Frequency: ")
    print(idf_values)

    # Calculate TF-IDF
    tf_idf = {}
    for token in tokens:
        tf_idf[token] = term_frequency[token] * idf_values[token]

    # Calculate the final floating vector
    floating_vector = sum(tf_idf.values())
    print("\nFloating Vector: ")
    print(floating_vector)

    # Normalizing the Floating Vector
    max_value = max(tf_idf.values())
    min_value = min(tf_idf.values())
    normalized_vector = (floating_vector - min_value) / (max_value - min_value)
    print("\nNormalized Floating Vector: ")
    print(normalized_vector)
    # return normalized_vector


def tokenize(text):
    tokens = [a for a in text.split()]
    return tokens


# One-Hot Encoding
def one_hot_encode(tokens):
    one_hot_encoded_tokens = []
    for token in tokens:
        one_hot_encoded_token = np.zeros(len(tokens))
        one_hot_encoded_token[tokens.index(token)] = 1.0
        one_hot_encoded_tokens.append(one_hot_encoded_token)
    return one_hot_encoded_tokens


# Calculating Term Frequency
def term_frequency(one_hot_encoded_tokens):
    term_frequencies = []
    for token in one_hot_encoded_tokens:
        term_frequency = np.sum(token)
        term_frequencies.append(term_frequency)
    return term_frequencies


# Calculating Inverse Document Frequency
def inverse_document_frequency(one_hot_encoded_tokens):
    inverse_document_frequencies = []
    n_documents = len(one_hot_encoded_tokens[0])
    for token in one_hot_encoded_tokens:
        n_document_with_token = np.sum(token)
        inverse_document_frequency = np.log(n_documents / n_document_with_token)
        inverse_document_frequencies.append(inverse_document_frequency)
    return inverse_document_frequencies


# Multiplying TF and IDF
def multiply_tf_idf(term_frequencies, inverse_document_frequencies):
    tf_idf_values = []
    for i in range(len(term_frequencies)):
        tf_idf_value = term_frequencies[i] * inverse_document_frequencies[i]
        tf_idf_values.append(tf_idf_value)
    return tf_idf_values


# Summing the Values
def sum_tf_idf(tf_idf_values):
    return np.sum(tf_idf_values)


# Normalizing the Vector
def normalize_vector(tf_idf):
    # Calculate the final floating vector
    floating_vector = sum(tf_idf)
    print("\nFloating Vector: ")
    print(floating_vector)

    # Normalizing the Floating Vector
    max_value = max(tf_idf)
    min_value = min(tf_idf)
    normalized_vector = []
    for value in tf_idf:
        print("\nValue: ")
        print(value)
        normalized_vector.append((value / floating_vector))
    # normalized_vector = (floating_vector - min_value) / (max_value - min_value)
    print("\nNormalized Floating Vector: ")
    print(normalized_vector)
    return normalized_vector


# Main Function
def test_convert_text_to_floating_vector(text="melody is my love!"):
    tokens = tokenize(text)
    print("\nTokens: ")
    print(tokens)
    one_hot_encoded_tokens = one_hot_encode(tokens)
    print("\nOne-Hot Encoding: ")
    print(one_hot_encoded_tokens)
    term_frequencies = term_frequency(one_hot_encoded_tokens)
    print("\nTerm Frequency: ")
    print(term_frequencies)
    inverse_document_frequencies = inverse_document_frequency(one_hot_encoded_tokens)
    print("\nInverse Document Frequency: ")
    print(inverse_document_frequencies)
    tf_idf_values = multiply_tf_idf(term_frequencies, inverse_document_frequencies)
    print("\nTF-IDF: ")
    print(tf_idf_values)
    normalized_vector = normalize_vector(tf_idf_values)
    print("\nNormalized Floating Vector: ")
    print(normalized_vector)
    return normalized_vector
