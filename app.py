import streamlit as st
import pandas as pd
import pickle
import requests
from pathlib import Path

# background image

import base64

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()



img = get_base64("background/movie.jpg")

st.markdown(f"""
<style>

.stApp{{
    background:
        linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)),
        url("data:image/jpeg;base64,{img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

</style>
""", unsafe_allow_html=True)

# Adding style and configration

import time

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# fetching poster from TMDb API

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

# improving header 

st.markdown("""
<div style="
background:linear-gradient(90deg,#0f766e,#2e8b57);
padding:30px;
border-radius:18px;
text-align:center;
color:white;
margin-bottom:25px;
box-shadow:0px 5px 15px rgba(0,0,0,0.2);
">

<h1 style="color:white;">🎬 Movie Recommender System</h1>

<p style="font-size:18px;">
Machine Learning based Movie Recommendation using cosine similarity and content-based filtering. This system recommends movies based on the movie you select from the dropdown list. It fetches movie posters using The Movie Database (TMDb) API.
</p>

</div>
""", unsafe_allow_html=True)


# recommendation function

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



BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR /

with open(MODEL_DIR / "movie_dict.pkl", "rb") as f:
    movies_dict = pickle.load(f)

with open(MODEL_DIR / "similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

movies = pd.DataFrame(movies_dict)

#---------------- Streamlit UI ----------------
col1, col2 = st.columns([3, 1])

with col1:
    selected_movie = st.selectbox(
        "🎬 Select a Movie",
        movies['title'].values
    )

with col2:
    st.markdown("### 🎥 About")
    st.success("Content-Based Recommender")
    st.write("✅ Cosine Similarity")
    st.write("✅ TMDb Posters")
    st.write("🎬 Top 5 Similar Movies")

#----------------- Streamlit UI ----------------

if st.button("🎬 Get Recommendations", use_container_width=True):
    with st.spinner("Finding similar movies..."):
        names, posters = recommend(selected_movie)
   

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0], use_container_width=True)
        st.markdown(f"<center><b>{names[0]}</b></center>", unsafe_allow_html=True)

    with col2:
        st.image(posters[1], use_container_width=True)
        st.markdown(f"<center><b>{names[1]}</b></center>", unsafe_allow_html=True)

    with col3:
        st.image(posters[2], use_container_width=True)
        st.markdown(f"<center><b>{names[2]}</b></center>", unsafe_allow_html=True)

    with col4:
        st.image(posters[3], use_container_width=True)
        st.markdown(f"<center><b>{names[3]}</b></center>", unsafe_allow_html=True)

    with col5:
        st.image(posters[4], use_container_width=True)
        st.markdown(f"<center><b>{names[4]}</b></center>", unsafe_allow_html=True)


st.markdown("---")



st.markdown(
"""
<div style='text-align:center; color:lightgray;'>

### 🎬 Movie Recommendation System

Developed by **Harshit Mehta**

B.Tech CSE (AI & ML)

</div>
""",
unsafe_allow_html=True)

