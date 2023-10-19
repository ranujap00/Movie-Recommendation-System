import streamlit as st
import random
import pandas as pd
from content_based import recommend_content_based
from collaborative import collaborative_recommend
import pickle

# Function to display movies in a card format
def recommend(movie_name, n_outputs, mode):
    if mode == 'Content based':
        result = recommend_content_based(movie_name.lower(), n_outputs)
    elif mode == 'Collaborative':
        result = collaborative_recommend(movie_name.lower(), n_outputs)

    col1, col2, col3 = st.columns(3)
    title_height = "70px"  # Adjust the height as needed

    for i, val in enumerate(result):
        title_div = f"<div style='height: {title_height}; display: flex; align-items: center;'>{val['title']}</div>"
        if i % 3 == 0:
            with col1:
                st.write(title_div, unsafe_allow_html=True)
                st.image(val['url'], width=200)
        elif i % 3 == 1:
            with col2:
                st.write(title_div, unsafe_allow_html=True)
                st.image(val['url'], width=200)
        else:
            with col3:
                st.write(title_div, unsafe_allow_html=True)
                st.image(val['url'], width=200)

def get_movie_list():
    movies = pd.read_csv('movie_data_with_urls.csv')
    movList = list(movies['title'])
    return movList


def getTopRatedMovies(n_outputs):
    with open('./PKL_Files/popular_movies_df', 'rb') as file:
        new_df = pickle.load(file)
    
    top_movies = new_df.head(n_outputs)

    col1, col2, col3 = st.columns(3)
    title_height = "70px"  # Adjust the height as needed

    for i, movie in top_movies.iterrows():
        title_div = f"<div style='height: {title_height}; display: flex; align-items: center;'>{movie['title']}</div>"
        if i % 3 == 0:
            with col1:
                st.write(title_div, unsafe_allow_html=True)
                st.image(movie['Poster_URL'], width=200)
        elif i % 3 == 1:
            with col2:
                st.write(title_div, unsafe_allow_html=True)
                st.image(movie['Poster_URL'], width=200)
        else:
            with col3:
                st.write(title_div, unsafe_allow_html=True)
                st.image(movie['Poster_URL'], width=200)

# Streamlit UI
st.title("Movie Recommendation System")


# Create a radio button for page selection
selected_page = st.sidebar.radio("", ["Recommendation", "Popular"])

# Depending on the selected page, show the appropriate content
if selected_page == "Recommendation":
    st.sidebar.title("User Preferences")
    st.sidebar.markdown("Select your movie preferences:")
    movie = st.sidebar.selectbox("Movie", get_movie_list())
    # genre = st.sidebar.selectbox("Genre", ["Action", "Drama", "Comedy", "Sci-Fi", "Adventure"], disabled=True)
    mode = st.sidebar.selectbox("Recommendation Mode", ["Content based", "Collaborative"])
    num_recommendations = st.sidebar.number_input("Number of Recommendations", min_value=1, max_value=10, value=5)
    
    st.subheader("Click below to get a movie recommendation:")
    if st.button("Recommend a Movie"):
        recommend(movie, num_recommendations, mode)

elif selected_page == "Popular":

    # Disable inputs in the sidebar when "Popular" is selected
    st.sidebar.markdown("### Popular Page")
    st.sidebar.selectbox("Movie", options=get_movie_list(), key="popular_movie", disabled=True)
    st.sidebar.selectbox("Recommendation Mode", options=["Content based", "Collaborative"], key="popular_mode", disabled=True)
    # genre = st.sidebar.selectbox("Genre", ["Action", "Drama", "Comedy", "Sci-Fi", "Adventure"], disabled=False)
    n_movies = st.sidebar.slider("Number of Movies", min_value=1, max_value=50, value=5, key="popular_recommendations", disabled=False)

    getTopRatedMovies(n_movies)
        
