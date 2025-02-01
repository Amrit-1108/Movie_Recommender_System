# Movie Recommendation System

This project is a **Movie Recommendation System** built using **Streamlit**. It recommends movies based on user input using similarity scores derived from TMDB movie datasets.

## Features
- Movie recommendations based on similarity scores.
- Uses **cosine similarity** for finding similar movies.
- **Streamlit** web application for an interactive user experience.
- Pretrained similarity model for fast recommendations.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Amrit-1108/Movie_Recommender_System.git
   cd Movie_Recommender_System
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Enter a movie name to get recommendations.

## Dataset
- Uses **TMDB 5000 Movies and Credits** dataset.
- Preprocessed and stored as `movie_list.pkl` and `similarity.pkl`.

## Files
- **`app.py`** - Main Streamlit application.
- **`movies.ipynb`** - Jupyter notebook for data exploration.
- **`movie-recommendor.ipynb`** - Model development notebook.
- **`tmdb_5000_movies.csv` & `tmdb_5000_credits.csv`** - Datasets.
- **`movie_list.pkl` & `similarity.pkl`** - Preprocessed files for recommendations.
