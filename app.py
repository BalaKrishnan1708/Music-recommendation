from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

# Global variables to store data and models
df = None
tfidf_matrix = None
vectorizer = None

def load_and_preprocess_data():
    """Load and preprocess the music dataset"""
    global df, tfidf_matrix, vectorizer
    
    print("Loading dataset...")
    # Load dataset in chunks to reduce memory usage
    df = pd.read_csv('spotify_millsongdata.csv')
    
    # Clean the data - remove any rows with missing values
    df = df.dropna()
    
    # OPTIMIZATION: Sample dataset for free tier (reduce to 20,000 songs to fit in 512MB)
    # Remove this line if you upgrade to a paid plan
    if len(df) > 20000:
        print(f"Sampling dataset from {len(df)} to 20000 songs for memory optimization...")
        df = df.sample(n=20000, random_state=42).reset_index(drop=True)
    
    # Combine relevant features: artist, song name, and lyrics
    df['combined_features'] = df['artist'].astype(str) + ' ' + df['song'].astype(str) + ' ' + df['text'].astype(str)
    
    # Convert to lowercase for better matching
    df['combined_features'] = df['combined_features'].str.lower()
    
    print(f"Dataset loaded: {len(df)} songs")
    print("Applying TF-IDF vectorization...")
    
    # Initialize TF-IDF Vectorizer with reduced parameters for memory efficiency
    # max_features limits the vocabulary size for efficiency
    # ngram_range=(1,1) uses only single words (reduces memory)
    vectorizer = TfidfVectorizer(
        max_features=3000,  # Reduced from 5000
        stop_words='english',
        ngram_range=(1, 1),  # Changed from (1,2) to (1,1) to reduce memory
        min_df=3,  # Increased from 2 to reduce vocabulary
        max_df=0.95
    )
    
    # Fit and transform the combined features
    tfidf_matrix = vectorizer.fit_transform(df['combined_features'])
    
    print("TF-IDF vectorization completed!")
    print(f"Feature matrix shape: {tfidf_matrix.shape}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    load_and_preprocess_data()
    yield
    # Shutdown (if needed, cleanup code would go here)

app = FastAPI(title="Song Recommendation System", lifespan=lifespan)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the frontend HTML file"""
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Song Recommendation System API</h1><p>Status: Running</p>"

@app.get("/api/songs")
async def get_all_songs(limit: int = 100):
    """Get a list of all songs (limited for performance)"""
    if df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")
    
    # Return song list with artist and song name
    songs = df[['artist', 'song']].head(limit).to_dict('records')
    return {"songs": songs, "total": len(df)}

@app.get("/api/search")
async def search_songs(query: str, limit: int = 20):
    """Search for songs by name or artist"""
    if df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")
    
    query_lower = query.lower()
    # Filter songs that match the query in song name or artist
    mask = df['song'].str.lower().str.contains(query_lower, na=False) | \
           df['artist'].str.lower().str.contains(query_lower, na=False)
    
    results = df[mask][['artist', 'song']].head(limit).to_dict('records')
    return {"results": results, "count": len(results)}

@app.post("/api/recommend")
async def recommend_songs(song_name: str, artist_name: str = None, num_recommendations: int = 10):
    """
    Get song recommendations based on a selected song
    
    Parameters:
    - song_name: Name of the song
    - artist_name: Optional artist name for better matching
    - num_recommendations: Number of recommendations to return (default: 10)
    """
    if df is None or tfidf_matrix is None:
        raise HTTPException(status_code=500, detail="Dataset or model not loaded")
    
    # Find the song in the dataset
    song_name_lower = song_name.lower()
    
    if artist_name:
        artist_name_lower = artist_name.lower()
        mask = (df['song'].str.lower() == song_name_lower) & \
               (df['artist'].str.lower() == artist_name_lower)
    else:
        mask = df['song'].str.lower() == song_name_lower
    
    matching_songs = df[mask]
    
    if len(matching_songs) == 0:
        raise HTTPException(
            status_code=404, 
            detail=f"Song '{song_name}' not found in the dataset. Please try another song."
        )
    
    # Get the first matching song's index
    song_index = matching_songs.index[0]
    
    # Calculate cosine similarity for this song with all other songs
    song_vector = tfidf_matrix[song_index]
    similarity_scores = cosine_similarity(song_vector, tfidf_matrix).flatten()
    
    # Get indices of most similar songs (excluding the song itself)
    similar_indices = np.argsort(similarity_scores)[::-1][1:num_recommendations + 1]
    
    # Prepare recommendations
    recommendations = []
    for idx in similar_indices:
        recommendations.append({
            "artist": df.iloc[idx]['artist'],
            "song": df.iloc[idx]['song'],
            "similarity_score": float(similarity_scores[idx]),
            "link": df.iloc[idx]['link']
        })
    
    return {
        "selected_song": {
            "artist": df.iloc[song_index]['artist'],
            "song": df.iloc[song_index]['song']
        },
        "recommendations": recommendations,
        "total_recommendations": len(recommendations)
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "dataset_loaded": df is not None,
        "model_loaded": tfidf_matrix is not None,
        "total_songs": len(df) if df is not None else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

