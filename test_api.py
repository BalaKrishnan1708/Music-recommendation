"""
Simple test script to verify the API is working correctly
Run this after starting the server to test the endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed!")
            print(f"   Status: {data['status']}")
            print(f"   Dataset loaded: {data['dataset_loaded']}")
            print(f"   Total songs: {data['total_songs']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        print("   Make sure the server is running on http://localhost:8000")
        return False

def test_search():
    """Test the search endpoint"""
    print("\nTesting search endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/search?query=shape&limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search test passed!")
            print(f"   Found {data['count']} results")
            if data['results']:
                print(f"   Example: {data['results'][0]['song']} by {data['results'][0]['artist']}")
            return True
        else:
            print(f"❌ Search test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Search test error: {e}")
        return False

def test_recommendations():
    """Test the recommendations endpoint"""
    print("\nTesting recommendations endpoint...")
    try:
        # First, search for a song that exists in the dataset
        search_response = requests.get(f"{BASE_URL}/search?query=love&limit=1")
        if search_response.status_code == 200:
            search_data = search_response.json()
            if search_data['results']:
                # Use the first found song for recommendations
                test_song = search_data['results'][0]['song']
                test_artist = search_data['results'][0]['artist']
                print(f"   Using song from dataset: '{test_song}' by {test_artist}")
            else:
                # Fallback to a common search term
                test_song = "Heart-shaped Bruise"
                test_artist = None
        else:
            test_song = "Heart-shaped Bruise"
            test_artist = None
        
        # Get recommendations for the found song
        params = {"song_name": test_song, "num_recommendations": 5}
        if test_artist:
            params["artist_name"] = test_artist
            
        response = requests.post(f"{BASE_URL}/recommend", params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recommendations test passed!")
            print(f"   Selected: {data['selected_song']['song']} by {data['selected_song']['artist']}")
            print(f"   Recommendations: {data['total_recommendations']}")
            if data['recommendations']:
                print(f"   Top recommendation: {data['recommendations'][0]['song']} "
                      f"(similarity: {data['recommendations'][0]['similarity_score']:.2%})")
            return True
        elif response.status_code == 404:
            print(f"⚠️  Song not found in dataset")
            return False
        else:
            print(f"❌ Recommendations test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Recommendations test error: {e}")
        return False

def main():
    print("=" * 50)
    print("🧪 API Test Suite")
    print("=" * 50)
    print("\nMake sure the server is running: python app.py\n")
    
    results = []
    results.append(test_health_check())
    results.append(test_search())
    results.append(test_recommendations())
    
    print("\n" + "=" * 50)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 50)

if __name__ == "__main__":
    main()

