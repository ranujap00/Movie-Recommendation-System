import streamlit as st
import random
from content_based import recommend_content_based

# In a typical Streamlit app, the Python script is executed from top to bottom every time you interact with the user interface. When you change a setting or input (e.g., adjust the rating slider), Streamlit automatically re-executes the Python script. This is known as "reactivity" in Streamlit, and it's a fundamental feature that allows your app to dynamically respond to user input.

# Sample list of movies (you can replace this with a real dataset)
movies = [
    "The Shawshank Redemption",
    "The Godfather",
    "The Dark Knight",
    "Pulp Fiction",
    "Forrest Gump",
    "Inception",
    "The Matrix",
    "The Lord of the Rings",
    "Fight Club",
    "Goodfellas",
]

# Function to recommend a random movie
def recommend_movie():
    return random.choice(movies)

# Streamlit UI
st.title("Movie Recommendation System")

st.write("Welcome to the Movie Recommendation System!")

st.subheader("Click below to get a movie recommendation:")
if st.button("Recommend a Movie"):
    # recommended_movie = recommend_movie()
    result = recommend_content_based('cocoon (1985)')
    st.write(f"Recommended Movie: {result}")

st.sidebar.title("User Preferences")

# You can add more user preferences here (e.g., genre, rating, etc.)
# For a more advanced system, you would collect and use user data.

st.sidebar.markdown("Select your movie preferences:")
genre = st.sidebar.selectbox("Genre", ["Action", "Drama", "Comedy", "Sci-Fi", "Adventure"])
mode = st.sidebar.selectbox("Recommendation Mode", ["Content based", "Collaborative"])
rating = st.sidebar.slider("Minimum Rating", 1, 10, 5)

st.sidebar.markdown("Choose the number of recommendations:")
num_recommendations = st.sidebar.number_input("Number of Recommendations", min_value=1, max_value=10, value=5)

# In a real system, you would use user preferences to generate recommendations.

st.subheader("Your Recommendations:")
for _ in range(num_recommendations):
    recommended_movie = recommend_movie()
    st.write(f"- {recommended_movie}")

st.write("Enjoy your movie!")

# Run the app with: streamlit run your_script.py
