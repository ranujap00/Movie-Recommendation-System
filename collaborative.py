import pickle
import numpy as np


def collaborative_recommend(movie_name, n_outputs):
    # Load files
    with open('./PKL_Files/movie_rating_collaborative', 'rb') as file:
        mov_ratings = pickle.load(file)

    with open('./PKL_Files/similarity_scores_collaborative', 'rb') as file:
        similarity_scores = pickle.load(file)

    with open('./PKL_Files/pivot_table_collaborative', 'rb') as file:
        pt = pickle.load(file)

    # index fetch
    index = np.where(pt.index==movie_name)[0][0]

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
    
    return data