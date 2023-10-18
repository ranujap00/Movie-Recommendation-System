import pickle

def getTopRatedMovies():
    with open('./PKL_Files/popular_movies_df', 'rb') as file:
        new_df = pickle.load(file)
    
    num_rating_df = new_df.groupby('title').count()['rating'].reset_index()
    avg_rating_df = new_df.groupby('title')['rating'].mean().reset_index()

    avg_rating_df.rename(columns={'rating':'avg_rating'},inplace=True)

    popular_df = num_rating_df.merge(avg_rating_df,on='title')

    # popular_df = popular_df[popular_df['rating'] >= 30].sort_values('avg_rating', ascending=False).head(50)

    print(popular_df)


getTopRatedMovies()