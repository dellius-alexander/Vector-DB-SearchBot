import torch
from torch.ao import nn
import numpy as np
from src.myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)


def test_torch_embedding_1():
    m = nn.quantized.Embedding(num_embeddings=10, embedding_dim=12)
    indices = torch.tensor([9, 6, 5, 7, 8, 8, 9, 2, 8])
    log.info(f"\n{indices}")
    output = m(indices)
    log.info(f"\n{output.size()}")
    x = torch.rand(5, 3)
    log.info(f"\n{x}")


def test_torch_embedding_2():
    m = nn.Embedding(10, 3)
    indices = torch.tensor([[1, 2, 4, 5], [4, 3, 2, 9]])
    log.info(f"\n{indices}")
    output = m(indices)
    log.info(f"\n{output.size()}")


def test_numpy_embedding_1():
    text = "Webpack v5 comes with the latest terser-webpack-plugin out of the box. If you are using Webpack \
    v5 or above and wish to customize the options, you will still need to install terser-webpack-plugin. Using \
    Webpack v4, you have to install terser-webpack-plugin v4."
    text_vector = np.array([float(w) for w in [word for word in text.split()]])
    log.info(f"\n{text_vector}")
