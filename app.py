import pickle
import streamlit as st
import requests

# App configuration
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Constants
API_KEY = "your_api_key_here"
BASE_URL = "https://api.themoviedb.org/3/movie/"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500/"
YOUTUBE_BASE_URL = "https://www.youtube.com/watch?v="

# Function to fetch movie details and trailer
def fetch_movie_details(movie_id):
    try:
        url = f"{BASE_URL}{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract details
        poster_path = data.get('poster_path')
        rating = data.get('vote_average', 'N/A')
        genres = ', '.join([genre['name'] for genre in data.get('genres', [])])
        popularity = data.get('popularity', 'N/A')
        release_date = data.get('release_date', 'N/A')
        overview = data.get('overview', 'No overview available.')
        full_poster_path = POSTER_BASE_URL + poster_path if poster_path else "https://via.placeholder.com/500x750?text=No+Image+Available"

        # Fetch trailer link
        trailer_url = fetch_trailer(movie_id)

        return full_poster_path, rating, genres, popularity, release_date, overview, trailer_url
    except requests.exceptions.RequestException:
        return (
            "https://via.placeholder.com/500x750?text=Error+Fetching+Poster",
            "N/A",
            "N/A",
            "N/A",
            "N/A",
            "No overview available.",
            None,
        )

# Function to fetch the trailer link
def fetch_trailer(movie_id):
    try:
        url = f"{BASE_URL}{movie_id}/videos?api_key={API_KEY}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Find the first YouTube trailer
        for video in data.get('results', []):
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                return YOUTUBE_BASE_URL + video['key']
        return None
    except requests.exceptions.RequestException:
        return None

# Function to recommend movies
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        recommended_movie_ratings = []
        recommended_movie_genres = []
        recommended_movie_popularities = []
        recommended_movie_release_dates = []
        recommended_movie_trailers = []

        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            poster, rating, genres, popularity, release_date, _, trailer_url = fetch_movie_details(movie_id)
            recommended_movie_posters.append(poster)
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_ratings.append(rating)
            recommended_movie_genres.append(genres)
            recommended_movie_popularities.append(popularity)
            recommended_movie_release_dates.append(release_date)
            recommended_movie_trailers.append(trailer_url)

        return (
            recommended_movie_names,
            recommended_movie_posters,
            recommended_movie_ratings,
            recommended_movie_genres,
            recommended_movie_popularities,
            recommended_movie_release_dates,
            recommended_movie_trailers,
        )
    except IndexError:
        st.error("Movie not found. Please select a valid movie from the list.")
        return [], [], [], [], [], [], []

# Function to get trending movies
def fetch_trending_movies():
    try:
        url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        trending_movies = []
        for movie in data['results']:
            trending_movies.append({
                "title": movie['title'],
                "poster": POSTER_BASE_URL + movie['poster_path'] if movie.get('poster_path') else "https://via.placeholder.com/500x750?text=No+Image+Available",
                "movie_id": movie['id']
            })
        return trending_movies
    except requests.exceptions.RequestException:
        return []

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = movies['title'].values

# Header
st.title("🎬 Movie Recommender System")

# Trending Movies Section
st.subheader("🌟 Trending Movies")
trending_movies = fetch_trending_movies()

if trending_movies:
    trending_cols = st.columns(5)
    for col, movie in zip(trending_cols, trending_movies):
        with col:
            st.markdown(f"""
                <style>
                    .trending-movie-{movie['title']} img {{
                        transition: transform 0.3s ease-in-out;
                    }}
                    .trending-movie-{movie['title']}:hover img {{
                        transform: scale(1.1);
                    }}
                </style>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="trending-movie-{movie["title"]}"><img src="{movie["poster"]}" alt="{movie["title"]}" width="100%" /></div>', unsafe_allow_html=True)
            st.caption(movie["title"])

# Search bar
search_query = st.text_input("Search for a movie:")
filtered_movies = movies[movies['title'].str.contains(search_query, case=False, na=False)]['title'].values if search_query else movie_list

# Movie selection
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown:",
    filtered_movies
)

if selected_movie:
    # Fetch details for the selected movie
    movie_id = movies[movies['title'] == selected_movie].iloc[0].movie_id
    poster, rating, genres, popularity, release_date, overview, trailer_url = fetch_movie_details(movie_id)

    # Display selected movie details with CSS animation
    st.subheader("Selected Movie Details")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
            <style>
                .movie-poster img {{
                    transition: transform 0.3s ease-in-out;
                }}
                .movie-poster:hover img {{
                    transform: scale(1.1);
                }}
            </style>
        """, unsafe_allow_html=True)
        # Display poster using HTML for animation effect
        st.markdown(f'<div class="movie-poster"><img src="{poster}" alt="Movie Poster" width="100%" /></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"### {selected_movie}")
        st.markdown(f"⭐ **Rating:** {rating}")
        st.markdown(f"🎭 **Genres:** {genres}")
        st.markdown(f"📅 **Release Date:** {release_date}")
        st.markdown(f"🔥 **Popularity:** {popularity:.0f}")
        st.markdown(f"**Overview:** {overview}")
        if trailer_url:
            st.markdown(f"🎥 [Watch Trailer]({trailer_url})")

if st.button('Show Recommendation'):
    (
        recommended_movie_names,
        recommended_movie_posters,
        recommended_movie_ratings,
        recommended_movie_genres,
        recommended_movie_popularities,
        recommended_movie_release_dates,
        recommended_movie_trailers,
    ) = recommend(selected_movie)

    # Display recommendations with hover effect animation
    if recommended_movie_names:
        st.subheader("Recommended Movies:")
        cols = st.columns(len(recommended_movie_names))
        for col, name, poster, rating, genres, popularity, release_date, trailer_url in zip(
            cols,
            recommended_movie_names,
            recommended_movie_posters,
            recommended_movie_ratings,
            recommended_movie_genres,
            recommended_movie_popularities,
            recommended_movie_release_dates,
            recommended_movie_trailers,
        ):
            with col:
                # Add hover effect animation to the recommendation posters
                st.markdown(f"""
                    <style>
                        .rec-movie-{name} img {{
                            transition: transform 0.3s ease-in-out;
                        }}
                        .rec-movie-{name}:hover img {{
                            transform: scale(1.1);
                        }}
                    </style>
                """, unsafe_allow_html=True)
                # Display recommendation poster using HTML for animation effect
                st.markdown(f'<div class="rec-movie-{name}"><img src="{poster}" alt="{name}" width="100%" /></div>', unsafe_allow_html=True)
                st.caption(
                    f"**{name}**\n"
                    f"⭐ **Rating:** {rating}\n"
                    f"🎭 **Genres:** {genres}\n"
                    f"📅 **Release Date:** {release_date}\n"
                    f"🔥 **Popularity:** {popularity:.0f}"
                )  # Display movie details
                if trailer_url:
                    st.markdown(f"🎥 [Watch Trailer]({trailer_url})")
