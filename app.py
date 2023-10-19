import streamlit as st
import pandas as pd
import requests


# Function to display movies in a card format
def recommend(movie_name, n_outputs, mode):
    if mode == 'Content based':
        response = requests.get(f'https://irwa-mrs.azurewebsites.net/api/content_based_function?code=RVFv-4r1jBXguVgnPXynSjocCfCtIo4TG5lX12U_7nG6AzFuWFIBjQ==&movie={movie_name}&n_outputs={n_outputs}')
    elif mode == 'Collaborative':
        response = requests.get(f'https://irwa-mrs.azurewebsites.net/api/collab_based_function?code=IdyiqdvfYl65fznPgT_9msXIoZxsJ3cLk-8cPwTRVEuFAzFuerIW9Q==&movie={movie_name}&n_outputs={n_outputs}')

    if response.status_code == 200:
        result = response.json()

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
    movies = pd.read_csv('./Implementation/movie_data_with_urls.csv')
    movList = list(movies['title'])
    return movList


def getTopRatedMovies(n_outputs):
    response = requests.get(f'https://irwa-mrs.azurewebsites.net/api/get_top_movies?code=oGzTT7kXPhOrS1rV-auobqVm-u3C0WcOKJ-vJf7nKHHzAzFuM04VPQ==&n_outputs={n_outputs}')
    
    if response.status_code == 200:
        top_movies = response.json()

    col1, col2, col3 = st.columns(3)
    title_height = "70px"  # Adjust the height as needed

    for i, movie in enumerate(top_movies):
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


# Custom CSS to style the selection box
st.markdown(
    """
    <style>
    .selectbox-container {
        display: flex;
        align-items: center;
        background-color: #f0f0f0;
        border-radius: 5px;
    }
    .stSelectbox {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

selected_page = st.selectbox("", ["Recommendation", "Popular"], key="my_selectbox")

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
        
