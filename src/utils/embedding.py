from typing import List, Dict, Any, Union
import jsonlines
import pandas as pd
import re

from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer


# ---------------------------------------------------------------------------------------
def merge_df(df1: DataFrame, df2: DataFrame):
    # Concatenate the two dataframes using concat()
    concat_df = pd.concat([df1, df2])
    print("\nMerged Dataframe:")
    print(concat_df)
    return concat_df


# ---------------------------------------------------------------------------------------
def print_df_info(df: DataFrame, num_lines: int = 10) -> None:
    # displaying the schema of the first 100 objects
    print("\nDataframe schema:")
    print(df.head(num_lines).dtypes)
    # analyzing the objects using pandas
    print("\nDataframe info:")
    print(df.head(num_lines).info())
    # displaying the shape of the first 100 objects
    print("\nDataframe shape:")
    print(f"Shape: {df.head(num_lines).shape}")
    # displaying the first 100 objects
    print("\nDataframe head:")
    print(df.head(num_lines))

# ---------------------------------------------------------------------------------------
def get_df_from_file(filepath: str, num_records: int = 10) -> Dict[
        str, Union[list[Union[dict[str, Any], list[Any], bool, float, int, str]], DataFrame]]:
    """
    Read a jsonl file and print the first 25 lines by default.

    :param filepath: The path to the *.jsonl file to read data from
    :param num_records: The number of records to load
    :return: None
    """
    # open jsonlines file
    with jsonlines.open(file=filepath, mode="r") as reader:
        # read the first 100 objects
        data = [next(reader.iter()) for x in range(num_records)]
    # convert to pandas dataframe
    return {"df": pd.DataFrame(data), "data": data}


# ---------------------------------------------------------------------------------------
def write_df_to_file(df: pd.DataFrame, filepath: str) -> bool:
    """
    Write a pandas dataframe to a jsonl file

    :param df: The pandas dataframe to write to file
    :param filepath: The path to the *.jsonl file to write data to
    :param mode: The mode to open the file in
    :return: True if successful, False otherwise
    """
    try:
        # open jsonlines file
        with jsonlines.open(file=filepath, mode='w') as writer:
            # write the dataframe to file
            writer.write_all(df.to_dict(orient='dict').items())
            print(f"Successfully wrote dataframe to file: {filepath}")
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return False


# ---------------------------------------------------------------------------------------
def chunk_the_text(text: str, chunk_size: int = 256):
    chunk_list = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if len(chunk) != chunk_size:
            diff = chunk_size - len(chunk)
            chunk += ' ' * diff
        chunk_list.append(chunk)
    return chunk_list


# ---------------------------------------------------------------------------------------
def clean_text(
        string: str,
        punctuations: str = r'''!()-[]{};:'"\,<>./?@#$%^&*_~''',
        stop_words: List[str] = ['the', 'a', 'and', 'is', 'be', 'will']) -> str:
    """
    A method to clean text
    """
    # Cleaning the urls
    string = re.sub(r'https?://\S+|www\.\S+', '', str(string))
    # Cleaning the html elements
    string = re.sub(r'<.*?>', '', string)
    # Removing the punctuations
    for x in string.lower():
        if x in punctuations:
            string = string.replace(x, "")

    # Converting the text to lower
    string = string.lower()
    # Removing stop words
    string = ' '.join([word for word in string.split() if word not in stop_words])
    # Cleaning the whitespaces
    string = re.sub(r'\s+', ' ', string).strip()
    # Removing the 's from the text
    string = re.sub(r"'s\b", "", string)

    return string


# ---------------------------------------------------------------------------------------
class TextEmbedding3DVector:
    tfidf_fit_vector = None
    selftfidf_vector = None
    hashing_fit_vector = None
    hashing_vector = None
    count_fit_vector = None
    count_vector = None

    def __init__(self, input_text: str = None):
        self.tfidf_vectorizer = TfidfVectorizer()
        self.hashing_vectorizer = HashingVectorizer()
        self.count_vectorizer = CountVectorizer()
        if input_text is not None:
            self.fit_transforms = self.fit_transform(input_text)
            self.tfidf_fit_vector, self.hashing_fit_vector, self.count_fit_vector = self.fit_transforms
            self.transforms = self.transform(input_text)
            self.tfidf_vector, self.hashing_vector, self.count_vector = self.transforms

    def fit_transform(self, text: str):
        """
        Fit and transform the text

        :param text: The text to fit and transform
        :return: The transformed text (tfidf[Tf-idf-weighted document-term matrix],
        hashing[Document-term matrix],
        count[Document-term matrix])
        """
        tfidf_vector = self.get_tfidf_fit_vector(text)
        hashing_vector = self.get_hashing_fit_vector(text)
        count_vector = self.get_count_fit_vector(text)
        return tfidf_vector, hashing_vector, count_vector

    def transform(self, text: str):
        """
        Fit and transform the text

        :param text: The text to fit and transform
        :return: The transformed text (tfidf[Tf-idf-weighted document-term matrix],
        hashing[Document-term matrix],
        count[Document-term matrix])
        """
        tfidf_vector = self.get_tfidf_vector(text)
        hashing_vector = self.get_hashing_vector(text)
        count_vector = self.get_count_vector(text)
        return tfidf_vector, hashing_vector, count_vector

    def get_hashing_vector(self, text: str):
        return self.hashing_vectorizer.transform(chunk_the_text(clean_text(text)))

    def get_tfidf_vector(self, text: str):
        return self.tfidf_vectorizer.transform(chunk_the_text(clean_text(text)))

    def get_count_vector(self, text: str):
        return self.count_vectorizer.transform(chunk_the_text(clean_text(text)))

    def get_tfidf_fit_vector(self, text: str):
        return self.tfidf_vectorizer.fit_transform(chunk_the_text(clean_text(text)))

    def get_count_fit_vector(self, text: str):
        return self.count_vectorizer.fit_transform(chunk_the_text(clean_text(text)))

    def get_hashing_fit_vector(self, text: str):
        return self.hashing_vectorizer.fit_transform(chunk_the_text(clean_text(text)))

    def language_translation(self, text, target_language):
        # TODO: Add language translation logic
        pass
