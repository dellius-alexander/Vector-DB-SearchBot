import logging
import traceback
import unittest
from asyncio import Queue
import time
from collections.abc import Sequence
from typing import Union, List, Tuple
import multiprocessing as mp
from sympy import Array
from tqdm import tqdm

from myLogger.Logger import getLogger as GetLogger

log = GetLogger(name=__name__, level=logging.DEBUG)


def progress_bar(
        totals: Union[int, List[int]],
        queue: Queue,
) -> None:
    if isinstance(totals, list):
        splitted = True
        pbars = [
            tqdm(
                desc=f'Worker {pid + 1}',
                total=total,
                position=pid,
            )
            for pid, total in enumerate(totals)
        ]
    else:
        splitted = False
        pbars = [
            tqdm(total=totals)
        ]

    while True:
        try:
            message = queue.get()
            if message.startswith('update'):
                if splitted:
                    pid = int(message[6:])
                    pbars[pid].update(1)
                else:
                    pbars[0].update(1)
            elif message == 'done':
                break
        except:
            pass
    for pbar in pbars:
        pbar.close()


def batch_retrieval(data: Union[Array, Sequence, List, Tuple],
                    batch_size: int,
                    data_type: str = 'array') -> Union[Array, Sequence, List, Tuple]:
    """
    Retrieve batches of size `batch_size` from input of type `data_type x`

    :param data: data to be batched
    :param data_type: type of data to be batched
    :param batch_size: size of batch
    """

    # Get the original length of the data
    data_length = len(data)

    # Create a start index for the batch
    start_idx = 0
    indexes = []
    # Iterate through the data and get batch of size batch_size
    while start_idx < data_length:
        # If the batch size is greater than the remainder of the data
        if start_idx + batch_size > data_length:
            batch_size = data_length - start_idx

        # Get a list of indexes corresponding to the batch
        if data_type == 'array' or data_type == 'list':
            indexes = range(start_idx, start_idx + batch_size)
        elif data_type == 'tuple':
            indexes = [start_idx + i for i in range(batch_size)]

        # log.debug(f'\nIndexes: \n{indexes}')
        # Get the corresponding batch
        try:
            batch = [data[i] for i in indexes]
            yield batch
        except Exception as e:
            log.debug("An unexpected error occured: %s" % e)
            log.debug(traceback.format_exc())
            return

        # Increment the starting index
        start_idx += batch_size


class TestBatchArray(unittest.TestCase):

    def setUp(self):
        self.arr = [a for a in range(10)]
        # self.arr = tuple(a for a in range(100))
        self.batch_size = 2

    def test_batch_func(self):
        results = []
        try:
            for batch in batch_retrieval(self.arr, self.batch_size, 'list'):
                log.debug(f'\nBatch: \n{batch}')
                # self.assertEqual(self.batch_size, len(result))
        except StopIteration:
            log.debug(f'\nResults: \n{results}')


if __name__ == '__main__':
    unittest.main()
