"""
Simple script to run the Song Recommendation System
"""
import uvicorn

if __name__ == "__main__":
    print("=" * 50)
    print("🎵 Song Recommendation System")
    print("=" * 50)
    print("\nStarting server...")
    print("Frontend: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

