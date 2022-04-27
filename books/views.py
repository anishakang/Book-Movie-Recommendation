import random

import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from rest_framework.renderers import TemplateHTMLRenderer

from recommendo.settings import ES_BASE_URL, ES_INDEX, SEARCH_PAYLOAD, \
                                DISTINCT_GENRES
from books import model

url = ES_BASE_URL + "/_search?pretty=true"


class Genre(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'skeleton.html'

    def get(self, request, genre=None):
        if genre is None:
            genre = random.choice(Genre.get_unique_genres())
        
        query_vector = model.encode([genre]).flatten().tolist()

        SEARCH_PAYLOAD["query"]["script_score"]["script"]["source"] = SEARCH_PAYLOAD["query"]["script_score"]["script"]["source"].format("genre_enc")
        SEARCH_PAYLOAD["query"]["script_score"]["script"]["params"]["query_vector"] = query_vector

        response = requests.get(url, json=SEARCH_PAYLOAD).json()
        records = []

        data = response.get("hits", {}).get("hits", [])
        genres = []
        if data:
            for record in data:
                name = record["_source"]["name"]
                genre = record["_source"]["genre"]
                synopsis = record["_source"]["synopsis"]
                object_type = record["_source"]["object_type"]
                records.append({"name": name, "genre": genre, "synopsis": synopsis,
                                "object_type": object_type})
        else:
            genres = Genre.get_unique_genres()

        return Response({'objects': records, "genres": genres})

    @staticmethod
    def get_unique_genres():
        genres = []
        response = requests.get(url, json=DISTINCT_GENRES).json()
        for object in response.get("aggregations", {}).get("keys", {}).get("buckets", []):
            genres.append(object["key"])

        return genres

class Synopsis(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'skeleton.html'

    def get(self, request, synopsis):
        query_vector = model.encode([synopsis]).flatten().tolist()

        SEARCH_PAYLOAD["query"]["script_score"]["script"]["source"] = SEARCH_PAYLOAD["query"]["script_score"]["script"]["source"].format("synopsis_enc")
        SEARCH_PAYLOAD["query"]["script_score"]["script"]["params"]["query_vector"] = query_vector

        url = ES_BASE_URL + "/_search?pretty=true"
        response = requests.get(url, json=SEARCH_PAYLOAD).json()
        data = response.get("hits", {}).get("hits", [])
        records = []
        for record in data:
            name = record["_source"]["name"]
            genre = record["_source"]["genre"]
            synopsis = record["_source"]["synopsis"]
            object_type = record["_source"]["object_type"]
            records.append({"name": name, "genre": genre, "synopsis": synopsis,
                            "object_type": object_type})

        return Response({'objects': records})
