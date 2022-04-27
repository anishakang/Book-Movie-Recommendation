import os
import re

import tqdm
import pandas as pd
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from elasticsearch.helpers import bulk


document_schema = {
    "mappings": {
            "properties": {
                "genre_enc": {
                    "type": "dense_vector",
                    "dims": 768
                },
                "synopsis_enc": {
                    "type": "dense_vector",
                    "dims": 768
                },
                "genre": {
                    "type": "keyword"
                },
                "name": {
                    "type": "text"
                },
                "object_type": {
                    "type": "keyword"
                },
                "synopsis": {
                    "type": "text"
                }
            }
        }
     }
INDEX_NAME = "recommenders"
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
client = Elasticsearch("http://localhost:9200")
try:
    client.indices.create(index=INDEX_NAME, body=document_schema)
except Exception as why:
    print(why)

def index_all_books(limit=None):
    # https://www.kaggle.com/datasets/joshuaokechukwu/public-books-dataset?resource=download
    compiled_regex = re.compile(r"\(Books\)")
    df = pd.read_csv("Books_Dataset.csv")
    df["Reviews"] = df["Reviews"].str.split(" ", expand=True)[0].astype(float)
    df["Genre"] = df["Genre"].str.replace(pat=compiled_regex, repl="").str.strip()

    data = []
    for row_number, book in df.iterrows():
        tqdm.tqdm.write(f"Processing {row_number} of {len(df)}... ")
        genre_enc = model.encode([book["Genre"]]).flatten().tolist()
        synopsis_enc = model.encode([book["Synopsis"]]).flatten().tolist()
        document = {"name": book["Title"], "synopsis": book["Synopsis"],
                    "genre": book["Genre"], "genre_enc": genre_enc,
                    "object_type": "book", "synopsis_enc": synopsis_enc,
                    "_index": INDEX_NAME}
        if limit is not None and row_number == limit:
            break
        data.append(document)

    bulk(client, data)

def index_all_movies(limit=None):
    # https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots
    compiled_regex = re.compile(r"unkown")
    df = pd.read_csv("wiki_movie_plots_deduped.csv")
    df["Genre"] = df["Genre"].str.replace(pat=compiled_regex, repl="NA").str.strip()
    df["Genre"] = df["Genre"].str.replace("/", " or ")

    data = []
    for row_number, movie in df.iterrows():
        tqdm.tqdm.write(f"Processing {row_number} of {len(df)}... ")
        genre_enc = model.encode([movie["Genre"]]).flatten().tolist()
        synopsis_enc = model.encode([movie["Plot"]]).flatten().tolist()
        document = {"name": movie["Title"], "synopsis": movie["Plot"],
                    "genre": movie["Genre"], "genre_enc": genre_enc,
                    "object_type": "movie", "synopsis_enc": synopsis_enc,
                    "_index": INDEX_NAME}
        if limit is not None and row_number == limit:
            break
        data.append(document)

    bulk(client, data)
index_all_movies(limit=40)
index_all_books(limit=40)
