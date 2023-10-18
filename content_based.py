import pickle

def recommend_content_based(movie):
    # load files
    # Load the array from the pickle file
    with open('./PKL_Files/stemmed_df_content_based', 'rb') as file:
        new_df = pickle.load(file)

        # Load the array from the pickle file
    with open('./PKL_Files/similarity_content_based', 'rb') as file:
        similarity = pickle.load(file)

    mov_list = []

    movie_index = new_df[new_df['title'] == movie].index[0]
    print(movie_index)
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    for i in movie_list:
        d = dict()
        d['title'] = new_df.iloc[i[0]].title
        d['url'] = new_df.iloc[i[0]].Poster_URL
        mov_list.append(d)
    
    return mov_list