import streamlit as st
import random
import pandas as pd
from content_based import recommend_content_based
from collaborative import collaborative_recommend

# In a typical Streamlit app, the Python script is executed from top to bottom every time you interact with the user interface. When you change a setting or input (e.g., adjust the rating slider), Streamlit automatically re-executes the Python script. This is known as "reactivity" in Streamlit, and it's a fundamental feature that allows your app to dynamically respond to user input.


# Function to display movies in a card format
def recomnend(movie_name, n_outputs):
    if mode == 'Content based':
        result = recommend_content_based(movie_name.lower(), n_outputs)

    elif mode == 'Collaborative':
        result = collaborative_recommend(movie_name.lower(), n_outputs)

    col1, col2, col3 = st.columns(3)
    for i, val in enumerate(result):
        if i % 3 == 0:
            with col1:
                st.write(f"{val['title']}")
                st.image(val['url'], use_column_width=True)
        elif i % 3 == 1:
            with col2:
                st.write(f"{val['title']}")
                st.image(val['url'], use_column_width=True)
        else:
            with col3:
                st.write(f"{val['title']}")
                st.image(val['url'], use_column_width=True)


def get_movie_list():
    movies = pd.read_csv('movie_data_with_urls.csv')
    movList = list(movies['title'])

    return movList


# Streamlit UI
st.title("Movie Recommendation System")

st.sidebar.title("User Preferences")

# You can add more user preferences here (e.g., genre, rating, etc.)
# For a more advanced system, you would collect and use user data.

st.sidebar.markdown("Select your movie preferences:")

movie = st.sidebar.selectbox("Movie", get_movie_list())
genre = st.sidebar.selectbox("Genre", ["Action", "Drama", "Comedy", "Sci-Fi", "Adventure"])
mode = st.sidebar.selectbox("Recommendation Mode", ["Content based", "Collaborative"])
rating = st.sidebar.slider("Rating", 1, 10, 5)

st.sidebar.markdown("Choose the number of recommendations:")
num_recommendations = st.sidebar.number_input("Number of Recommendations", min_value=1, max_value=10, value=5)

st.subheader("Click below to get a movie recommendation:")
if st.button("Recommend a Movie"):
    recomnend(movie, num_recommendations)

# In a real system, you would use user preferences to generate recommendations.

st.write("Enjoy your movie!")

# Run the app with: streamlit run your_script.py
