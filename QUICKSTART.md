# 🚀 Quick Start Guide

## Installation (One-Time Setup)

1. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Using run.py (Recommended)
```bash
python run.py
```

### Option 2: Using app.py directly
```bash
python app.py
```

### Option 3: Using uvicorn
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Access the Application

- **Frontend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## Testing

After starting the server, run the test script in another terminal:
```bash
python test_api.py
```

## First Use

1. Open http://localhost:8000 in your browser
2. Type a song name (e.g., "Shape of You")
3. Click "Get Recommendations" or press Enter
4. View similar songs with similarity scores!

## Troubleshooting

- **Port already in use**: Change the port in `app.py` or `run.py`
- **Module not found**: Run `pip install -r requirements.txt`
- **CSV file not found**: Make sure `spotify_millsongdata.csv` is in the same directory as `app.py`
- **Slow loading**: The first request may take time as the dataset loads and processes

## Notes

- Initial data loading may take 1-2 minutes (one-time on server start)
- The system processes the entire dataset on startup
- Recommendations are based on song content (artist, title, lyrics)

