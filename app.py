import streamlit as st
import pandas as pd
import pickle
import requests



import time

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a94a99c3f78167cf0e53da6a518c8271&language=en-US"

    try:
        response = requests.get(
            url,
            timeout=10  
        )

        response.raise_for_status()

        data = response.json()

        if "poster_path" in data and data["poster_path"]:
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

        # return "https://via.placeholder.com/500x750?text=No+Poster"

    except Exception as e:
        print(f"Failed to fetch poster for movie_id={movie_id}")
        print(e)
        return "https://via.placeholder.com/500x750?text=Error"
    


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    # Already contains the top 20 recommended movie indices
    movie_list = similarity[movie_index][:5]

    recommended_movies = []
    recommended_posters = []

    for idx in movie_list:
        movie_id = movies.iloc[idx].id

        recommended_movies.append(movies.iloc[idx].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ---------------- Streamlit UI ----------------

st.title("🎬 Movie Recommender System")

movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movies = pd.DataFrame(movies_dict)

selected_movie_name = st.selectbox(
    "Which movie would you like to search for?",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
