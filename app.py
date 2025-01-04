import streamlit as st
import pickle
import requests
import gzip




# Function to fetch movie posters
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url)
        data = data.json()
        poster_path = data.get('poster_path', None)
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"

    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Error"


# Load pickle files
df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = df['title'].values


# Recommendation function
def recommend(movie):
    if movie not in df['title'].values:
        return [], []

    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies:
        movie_id = df.iloc[i[0]].id  # Assuming 'id' column exists in your dataset
        recommended_movies.append(df.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


# Streamlit app
st.title('Movie Recommender')

# Dropdown for selecting a movie
selected_movie_name = st.selectbox(
    "Select a movie:",
    movies_list
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    if names and posters:
        # Display recommendations in columns
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.subheader(names[0])
            st.image(posters[0],width=100)

        with col2:
            st.subheader(names[1])
            st.image(posters[1],width=100)

        with col3:
            st.subheader(names[2])
            st.image(posters[2],width=100)

        with col4:
            st.subheader(names[3])
            st.image(posters[3],width=100)

        with col5:
            st.subheader(names[4])
            st.image(posters[4],width=100)
    else:
        st.error("No recommendations found or an error occurred.")
