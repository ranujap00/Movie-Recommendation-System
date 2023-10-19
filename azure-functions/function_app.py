import azure.functions as func
import logging
import pickle
import pandas as pd
import json
import numpy as np

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="content_based_function")
def content_based_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    movie = req.params.get('movie').lower()
    n_outputs = int(req.params.get('n_outputs'))

    with open('./PKL_Files/stemmed_df_content_based', 'rb') as file:
        new_df = pickle.load(file)

        # Load the array from the pickle file
    with open('./PKL_Files/similarity_content_based', 'rb') as file:
        similarity = pickle.load(file)

    mov_list = []

    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:n_outputs+1]

    for i in movie_list:
        d = dict()
        d['title'] = new_df.iloc[i[0]].title
        d['url'] = new_df.iloc[i[0]].Poster_URL
        mov_list.append(d)


    if len(mov_list)> 0:
        response_data = json.dumps(mov_list)
        return func.HttpResponse(response_data, mimetype="application/json")
    else:
        return func.HttpResponse(
             "No Movies to recommend",
             status_code=200
        )


@app.route(route="get_top_movies", auth_level=func.AuthLevel.FUNCTION)
def get_top_movies(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    n_outputs = int(req.params.get('n_outputs'))

    with open('PKL_Files/popular_movies_df', 'rb') as file:
        new_df = pickle.load(file)

    if not new_df.empty:
        # Convert the DataFrame to a list of dictionaries
        data_list = new_df.head(n_outputs).to_dict(orient='records')

        # Convert the list to a JSON string
        response_data = json.dumps(data_list)

        return func.HttpResponse(response_data, mimetype="application/json")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="collab_based_function", auth_level=func.AuthLevel.FUNCTION)
def collab_based_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    movie = req.params.get('movie').lower()
    n_outputs = int(req.params.get('n_outputs'))

    with open('./PKL_Files/movie_rating_collaborative', 'rb') as file:
        mov_ratings = pickle.load(file)

    with open('./PKL_Files/similarity_scores_collaborative', 'rb') as file:
        similarity_scores = pickle.load(file)

    with open('./PKL_Files/pivot_table_collaborative', 'rb') as file:
        pt = pickle.load(file)

    # index fetch
    index = np.where(pt.index==movie)[0][0]

    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:n_outputs+1]
    # simillar items from 1 to 4
    
    data = []
    for i in similar_items:
        item = []
        d = dict()
        temp_df = mov_ratings[mov_ratings['title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))

        # urls = temp_df['Poster_URL'].str.replace(r'\d+', '', regex=True) # to remove the index value before the RL

        d['title'] = item[0]
        d['url'] = temp_df['Poster_URL'].values.tolist()[0]
        data.append(d)

    if len(data)> 0:
        response_data = json.dumps(data)
        return func.HttpResponse(response_data, mimetype="application/json")
    else:
        return func.HttpResponse(
             "No Movies to recommend",
             status_code=200
        )