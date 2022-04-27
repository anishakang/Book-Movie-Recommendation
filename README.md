# Book-Movie-Recommendation
To run the application on your system: 

You will need to install elasticsearch version 7.17.3. Run the command `pip install elasticsearch sentence-transformers`.
After doing the same, run the py file `db_indexer.py`. This will do our initial setup and Database indexing. Note that db_indexer.py may take some time to run. 


Now install djangorestframework on your system if not already done, since the project is implemented in that. On the terminal, run `py manage.py runserver` to start the server.

Go to <ins>localhost:8000/genre</ins>. This is the starting point of the application. 

## Features of the application: 
1. Listing of Books or Movies based on similar genres. 
2. Listing of Books or Movies based on similar synopsis.
3. Use of pretrained NLP model to generate ndarray vectors for genres and synopsis. 
4. Vectors are saved in elasticsearch. Elasticsearch is the database being used. 
5. Querying for similar objects (books, movies) using cosinesimilarity in Elasticsearch. 
6. Fetching of distinct genres if none requested by user. 
