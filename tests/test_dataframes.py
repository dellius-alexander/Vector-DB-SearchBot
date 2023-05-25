from pandas import DataFrame

from milvus.question_answering import remove_batch, batch_eliminator
from src.utils.embedding import merge_df


# Testing merge dataframes
def test_merge_dataframes():
    # Create two sample dataframes
    df1 = DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3'],
                     'C': ['C0', 'C1', 'C2', 'C3'],
                     'D': ['D0', 'D1', 'D2', 'D3']},
                    index=[0, 1, 2, 3])

    df2 = DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                     'B': ['B4', 'B5', 'B6', 'B7'],
                     'C': ['C4', 'C5', 'C6', 'C7'],
                     'D': ['D4', 'D5', 'D6', 'D7']},
                    index=[4, 5, 6, 7])

    # Concatenate the two dataframes using concat()
    df0 = merge_df(df1, df2)
    assert df0.shape == (8, 4)


# Testing adding columns to dataframes
def test_add_columns_to_dataframes_using_merge():
    # Create two sample dataframes
    df1 = DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3'],
                     'C': ['C0', 'C1', 'C2', 'C3'],
                     'D': ['D0', 'D1', 'D2', 'D3']},
                    index=[0, 1, 2, 3])

    df2 = DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                     'B': ['B4', 'B5', 'B6', 'B7'],
                     'E': ['E4', 'E5', 'E6', 'E7'],
                     'F': ['F4', 'F5', 'F6', 'F7']},
                    index=[4, 5, 6, 7])

    print(df1)
    print(df2)
    df0 = merge_df(df1, df2)
    print(f"Shape: {df0.shape}")
    assert df0.shape == (8, 6)


def test_batchs_func():
    array = [x for x in range(10000)]
    batch_size = 1000

    for batch in batch_eliminator(array, batch_size):
        print("\n")
        print(batch)

