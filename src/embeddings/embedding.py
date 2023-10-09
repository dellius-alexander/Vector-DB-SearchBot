# $$ [markdown]
# # 1. Embeddings
#
# ## 1.1. Introduction
#
# Embeddings are a way to represent words as vectors. These vectors can be used as features in machine learning
# models. Embeddings are useful because they capture the semantic meaning of words. For example, the words "cat" and
# "dog" are semantically similar, so their embeddings will be similar as well. This allows us to use embeddings as
# features in machine learning models that require semantic information about words.
#
# In this notebook, we will explore different types of embeddings and how they can be used in machine learning
# models. We will also show how to train your own embeddings using the `Word2Vec` algorithm.
#
# ## 1.2. Table of Contents
#
# - [1. Embeddings](#1-embeddings)
#   - [1.1. Introduction](#11-introduction)
#   - [1.2. Table of Contents](#12-table-of-contents)
#   - [1.3. Imports](#13-imports)
#   - [1.4. Data](#14-data)
#     - [1.4.1. Load Data](#141-load-data)
#     - [1.4.2. Data Preprocessing](#142-data-preprocessing)
#     - [1.4.3. Train-Test Split](#143-train-test-split)
#   - [1.5. Word2Vec Embeddings](#15-word2vec-embeddings)
#     - [1.5.1. Train Word2Vec Embeddings](#151-train-word2vec-embeddings)
#     - [1.5.2. Visualize Word2Vec Embeddings](#152-visualize-word2vec-embeddings)
#     - [1.5.3. Save Word2Vec Embeddings](#153-save-word2vec-embeddings)
#   - [1.6. GloVe Embeddings](#16-glove-embeddings)
#     - [1.6.1. Load GloVe Embeddings](#161-load-glove-embeddings)
#     - [1.6.2. Visualize GloVe Embeddings](#162-visualize-glove-embeddings)
#     - [1.6.3. Save GloVe Embeddings](#163-save-glove-embeddings)
#   - [1.7. FastText Embeddings](#17-fasttext-embeddings)
#     - [1.7.1. Train FastText Embeddings](#171-train-fasttext-embeddings)
#     - [1.7.2. Visualize FastText Embeddings](#172-visualize-fasttext-embeddings)
#     - [1.7.3. Save FastText Embeddings](#173-save-fasttext-embeddings)
#   - [1.8. Summary](#18-summary)
#   - [1.9. References](#19-references)
#
# ## 1.3. Imports
#
# We will use the following libraries in this notebook:
#
# - `pandas` to load and manipulate data
# - `matplotlib` to visualize data
# - `gensim` to train and use word embeddings
# - `sklearn` to split data into train and test sets
# - `umap` to visualize embeddings in 2D
#
# We will also use the `utils` module from the `src` directory to load and preprocess the data.

# $$

import pandas as pd
KEY_SELECTION = "question"
samples = pd.read_csv(filepath_or_buffer="../Resources/datasets/questions_answers.csv",
                      nrows=10)
categories = sorted(samples[KEY_SELECTION].unique())
print(f"Categories of QA samples: \n{samples[KEY_SELECTION]}")
samples.head()

# $$ [markdown]
# ## 2.2. Data Preprocessing
#
# ### 2.2.1. Text Cleaning
#
# We will use the `clean_text` function from the `utils` module to clean the text data. This function performs the
# following operations:
#
# - Remove HTML tags
# - Remove accented characters
# - Expand contractions
# - Remove special characters
# - Lowercase all text
# - Remove stopwords
# - Lemmatize text
#
# We will also use the `clean_text` function to clean the text data in the `samples` DataFrame.

# $$
# from utils.encoders import clean_text

# # samples["clean_text"] = samples["text"].apply(clean_text)
# samples.head()

# $$ [markdown]
# ### 2.2.2. Train-Test Split
#
# We will use the `train_test_split` function from the `sklearn.model_selection` module to split the data into
# training and test sets. We will use 80% of the data for training and 20% for testing.

# $$
from sklearn.model_selection import train_test_split

train_samples, test_samples = train_test_split(samples, test_size=0.2, random_state=42)
print("Number of training samples:", len(train_samples))
print("Number of test samples:", len(test_samples))

# $$ [markdown]
# ### 2.2.3. Label Encoding
#
# We will use the `LabelEncoder` class from the `sklearn.preprocessing` module to encode the labels in the training
# and test sets. The `LabelEncoder` class converts the categorical labels into integers. We will use the
# `inverse_transform` method to convert the predicted labels back into the original categorical labels.

# $$
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()

train_samples["label"] = label_encoder.fit_transform(train_samples[KEY_SELECTION])
test_samples["label"] = label_encoder.transform(test_samples[KEY_SELECTION])
train_samples.head()
print(f"Test: \n{test_samples[KEY_SELECTION]}")
print(f"Train: \n{train_samples[KEY_SELECTION]}")
exit(0)
# $$ [markdown]
# ## 2.3. Feature Extraction
#
# We will use the `TfidfVectorizer` class from the `sklearn.feature_extraction.text` module to convert the text data
# into a matrix of TF-IDF features. We will use the `fit_transform` method to fit the `TfidfVectorizer` on the
# training data and convert the training data into a matrix of TF-IDF features. We will use the `transform` method to
# convert the test data into a matrix of TF-IDF features.

# $$
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
train_features = vectorizer.fit_transform(train_samples[KEY_SELECTION])
test_features = vectorizer.transform(test_samples[KEY_SELECTION])
print("Number of features:", len(vectorizer.get_feature_names()))

# $$ [markdown]
# ## 2.4. Model Training
#
# We will use the `LogisticRegression` class from the `sklearn.linear_model` module to train a logistic regression
# model. We will use the `fit` method to train the logistic regression model on the training data and labels. We will
# use the `predict` method to predict the labels for the test data.

# $$
from sklearn.linear_model import LogisticRegression

logistic_regression = LogisticRegression()
logistic_regression.fit(train_features, train_samples["label"])
test_samples["predicted_label"] = logistic_regression.predict(test_features)
test_samples.head()

# $$ [markdown]
# ## 2.5. Model Evaluation
#
# We will use the `accuracy_score` function from the `sklearn.metrics` module to calculate the accuracy of the
# logistic regression model on the test data.

# $$
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(test_samples["label"], test_samples["predicted_label"])
print("Accuracy:", accuracy)

# $$ [markdown]
# ## 2.6. Model Inference
#
# We will use the `predict` method of the logistic regression model to predict the label for a new sample.

# $$
new_sample = "The moon is the only natural satellite of Earth"
new_sample_features = vectorizer.transform([new_sample])
new_sample_predicted_label = logistic_regression.predict(new_sample_features)
print("Predicted label:", label_encoder.inverse_transform(new_sample_predicted_label)[0])

# $$ [markdown]
# ## 2.7. Saving the Model
#
# We will use the `dump` function from the `joblib` module to save the logistic regression model and the label
# encoder to disk.

# $$
from joblib import dump

dump(logistic_regression, "models/logistic_regression.joblib")
dump(label_encoder, "models/label_encoder.joblib")

# $$ [markdown]
# ## 2.8. Loading the Model
#
# We will use the `load` function from the `joblib` module to load the logistic regression model and the label
# encoder from disk.

# $$
from joblib import load

logistic_regression = load("../Resources/models/logistic_regression.joblib")
label_encoder = load("../Resources/models/label_encoder.joblib")

# $$ [markdown]
# ## 2.9. Model Inference
#
# We will use the `predict` method of the logistic regression model to predict the label for a new sample.

# $$
new_sample = "The moon is the only natural satellite of Earth"
new_sample_features = vectorizer.transform([new_sample])
new_sample_predicted_label = logistic_regression.predict(new_sample_features)
print("Predicted label:", label_encoder.inverse_transform(new_sample_predicted_label)[0])

# $$ [markdown]
# ## 2.10. Model Evaluation
#
# We will use the `accuracy_score` function from the `sklearn.metrics` module to calculate the accuracy of the
# logistic regression model on the test data.

# $$
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(test_samples["label"], test_samples["predicted_label"])
print("Accuracy:", accuracy)

