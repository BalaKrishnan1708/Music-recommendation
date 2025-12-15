# 🎵 Song Recommendation System

A content-based music recommendation system that uses TF-IDF vectorization and cosine similarity to suggest similar songs based on song metadata (artist, song name, and lyrics).

## 📋 Project Overview

This project implements a music recommendation system that analyzes song content to find similarities between songs. Unlike collaborative filtering approaches that rely on user ratings, this system uses content-based filtering to recommend songs based on their intrinsic features.

### Key Features

- **Content-Based Filtering**: Analyzes song content (artist, title, lyrics) to find similarities
- **TF-IDF Vectorization**: Converts text data into numerical features for analysis
- **Cosine Similarity**: Measures similarity between songs based on their feature vectors
- **RESTful API**: FastAPI backend with multiple endpoints
- **Interactive Frontend**: Beautiful, responsive web interface
- **Real-time Search**: Auto-suggestions while typing song names

## 🛠️ Technologies Used

- **Backend**: FastAPI, Python
- **Machine Learning**: scikit-learn (TF-IDF, Cosine Similarity)
- **Data Processing**: pandas, numpy
- **Frontend**: HTML, CSS, JavaScript
- **Server**: Uvicorn

## 📁 Project Structure

```
music project/
│
├── app.py                          # FastAPI backend application
├── index.html                      # Frontend web interface
├── requirements.txt                # Python dependencies
├── spotify_millsongdata.csv        # Music dataset
└── README.md                       # Project documentation
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

Start the FastAPI server:

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Step 3: Access the Frontend

Open your web browser and navigate to:
- **Frontend**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative API Docs**: `http://localhost:8000/redoc`

## 📊 How It Works

### 1. Data Preprocessing

- Loads the music dataset from CSV
- Combines relevant features: `artist + song name + lyrics`
- Cleans and normalizes text data (lowercase conversion)
- Removes missing values

### 2. TF-IDF Vectorization

**TF-IDF (Term Frequency-Inverse Document Frequency)** converts text into numerical vectors:
- **Term Frequency (TF)**: How often a word appears in a document
- **Inverse Document Frequency (IDF)**: How rare/common a word is across all documents
- Creates a feature matrix where each song is represented as a vector

**Configuration:**
- Max features: 5000 (vocabulary size)
- N-gram range: (1, 2) - considers single words and word pairs
- English stop words removed
- Minimum document frequency: 2

### 3. Cosine Similarity

**Cosine Similarity** measures the angle between two vectors:
- Range: 0 to 1 (1 = identical, 0 = completely different)
- Calculates similarity between the selected song and all other songs
- Returns songs with highest similarity scores

### 4. Recommendation Generation

When a user selects a song:
1. Find the song in the dataset
2. Get its TF-IDF vector
3. Calculate cosine similarity with all other songs
4. Sort by similarity score (descending)
5. Return top N recommendations (excluding the selected song)

## 🔌 API Endpoints

### 1. Get All Songs
```
GET /api/songs?limit=100
```
Returns a list of songs (limited for performance).

**Response:**
```json
{
  "songs": [
    {"artist": "Artist Name", "song": "Song Name"},
    ...
  ],
  "total": 10000
}
```

### 2. Search Songs
```
GET /api/search?query=shape&limit=20
```
Search for songs by name or artist.

**Response:**
```json
{
  "results": [
    {"artist": "Artist Name", "song": "Song Name"},
    ...
  ],
  "count": 5
}
```

### 3. Get Recommendations
```
POST /api/recommend
Body: {
  "song_name": "Shape of You",
  "artist_name": "Ed Sheeran",  // Optional
  "num_recommendations": 10      // Optional, default: 10
}
```

**Response:**
```json
{
  "selected_song": {
    "artist": "Ed Sheeran",
    "song": "Shape of You"
  },
  "recommendations": [
    {
      "artist": "Artist Name",
      "song": "Song Name",
      "similarity_score": 0.85,
      "link": "/path/to/song"
    },
    ...
  ],
  "total_recommendations": 10
}
```

### 4. Health Check
```
GET /api/health
```
Check API status and dataset loading status.

## 🧪 Testing the API

### Using cURL

```bash
# Get recommendations
curl -X POST "http://localhost:8000/api/recommend?song_name=Shape%20of%20You&num_recommendations=5"

# Search songs
curl "http://localhost:8000/api/search?query=shape&limit=10"

# Health check
curl "http://localhost:8000/api/health"
```

### Using Python

```python
import requests

# Get recommendations
response = requests.post(
    "http://localhost:8000/api/recommend",
    params={
        "song_name": "Shape of You",
        "num_recommendations": 10
    }
)
print(response.json())
```

### Using Swagger UI

Visit `http://localhost:8000/docs` for interactive API documentation where you can test all endpoints directly.

## 📸 Usage Example

1. **Start the server**: Run `python app.py`
2. **Open browser**: Navigate to `http://localhost:8000`
3. **Enter song name**: Type a song name (e.g., "Shape of You")
4. **Get recommendations**: Click "Get Recommendations" or press Enter
5. **View results**: See similar songs with similarity scores

## 🎯 Key Concepts Explained

### TF-IDF (Term Frequency-Inverse Document Frequency)

**Purpose**: Convert text into numerical features that capture word importance.

**Example**:
- If "love" appears frequently in a song's lyrics, it gets a high TF score
- If "love" appears in many songs, it gets a lower IDF score (less distinctive)
- TF-IDF balances both: frequent in document, rare across documents = high importance

### Cosine Similarity

**Purpose**: Measure how similar two songs are based on their feature vectors.

**Formula**: 
```
similarity = (A · B) / (||A|| × ||B||)
```

**Why Cosine?**: 
- Measures angle between vectors, not magnitude
- Range 0-1 makes it easy to interpret
- Works well with high-dimensional sparse data (like TF-IDF vectors)

## 📝 Project Workflow

```
Data Loading → Preprocessing → TF-IDF Vectorization → 
Cosine Similarity Calculation → Recommendation Generation
```

1. **Data Loading**: Read CSV file with song metadata
2. **Preprocessing**: Clean and combine features (artist + song + lyrics)
3. **TF-IDF Vectorization**: Convert text to numerical vectors
4. **Similarity Calculation**: Compute cosine similarity matrix
5. **Recommendation**: Find and return most similar songs

## 🔍 Limitations & Future Improvements

### Current Limitations
- Content-based only (no user preferences)
- Limited to songs in the dataset
- No genre filtering
- Performance may be slow with very large datasets

### Possible Improvements
- Add collaborative filtering
- Implement genre-based filtering
- Add user preferences and history
- Cache similarity matrix for faster responses
- Add more features (tempo, key, mood)
- Implement hybrid recommendation system

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Song Recommendation System - Content-Based Filtering Project

## 📚 References

- [TF-IDF Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [Cosine Similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Note**: Make sure the `spotify_millsongdata.csv` file is in the same directory as `app.py` before running the application.

