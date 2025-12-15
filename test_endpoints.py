"""
Quick test script to verify all API endpoints are working
Run this to test your hosted API before taking screenshots
"""
import requests
import json
from datetime import datetime

# UPDATE THIS WITH YOUR RENDER URL
API_BASE_URL = "https://your-render-url.onrender.com/api"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health_check():
    """Test the health check endpoint"""
    print_section("1. Health Check Endpoint")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(f"\nResponse:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_search():
    """Test the search endpoint"""
    print_section("2. Search Endpoint")
    try:
        query = "love"
        response = requests.get(
            f"{API_BASE_URL}/search?query={query}&limit=5",
            timeout=10
        )
        print(f"Query: '{query}'")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Search test passed!")
            print(f"\nFound {data.get('count', 0)} results")
            if data.get('results'):
                print("\nFirst 3 results:")
                for i, song in enumerate(data['results'][:3], 1):
                    print(f"  {i}. {song['song']} by {song['artist']}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_recommendations():
    """Test the recommendations endpoint"""
    print_section("3. Recommendations Endpoint")
    try:
        # First, search for a song to get a valid one
        search_response = requests.get(
            f"{API_BASE_URL}/search?query=love&limit=1",
            timeout=10
        )
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            if search_data.get('results'):
                test_song = search_data['results'][0]['song']
                test_artist = search_data['results'][0]['artist']
                print(f"Testing with: '{test_song}' by {test_artist}")
                
                response = requests.post(
                    f"{API_BASE_URL}/recommend",
                    params={
                        "song_name": test_song,
                        "artist_name": test_artist,
                        "num_recommendations": 5
                    },
                    timeout=30
                )
                
                print(f"Status Code: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Recommendations test passed!")
                    print(f"\nSelected Song: {data['selected_song']['song']} by {data['selected_song']['artist']}")
                    print(f"Recommendations: {data['total_recommendations']}")
                    if data.get('recommendations'):
                        print("\nTop 3 recommendations:")
                        for i, rec in enumerate(data['recommendations'][:3], 1):
                            print(f"  {i}. {rec['song']} by {rec['artist']} (Similarity: {rec['similarity_score']:.2%})")
                    return True
                else:
                    error_data = response.json() if response.content else {}
                    print(f"❌ Failed: {response.status_code}")
                    print(f"Error: {error_data.get('detail', 'Unknown error')}")
                    return False
            else:
                print("❌ No songs found in search")
                return False
        else:
            print("❌ Search failed, cannot test recommendations")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_frontend():
    """Test if frontend is accessible"""
    print_section("4. Frontend Accessibility")
    try:
        frontend_url = API_BASE_URL.replace('/api', '')
        response = requests.get(frontend_url, timeout=10)
        print(f"Frontend URL: {frontend_url}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Frontend is accessible!")
            if 'Song Recommendation System' in response.text:
                print("✅ Frontend content loaded correctly")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("  API Endpoint Testing Script")
    print("  Song Recommendation System")
    print("="*60)
    print(f"\nTesting API at: {API_BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if "your-render-url" in API_BASE_URL:
        print("\n⚠️  WARNING: Please update API_BASE_URL with your actual Render URL!")
        print("   Edit this file and change:")
        print("   API_BASE_URL = 'https://your-render-url.onrender.com/api'")
        return
    
    results = []
    results.append(("Health Check", test_health_check()))
    results.append(("Search", test_search()))
    results.append(("Recommendations", test_recommendations()))
    results.append(("Frontend", test_frontend()))
    
    print_section("Test Summary")
    print(f"{'Test':<20} {'Status':<10}")
    print("-" * 30)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<20} {status:<10}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed! Your API is ready for submission!")
    else:
        print("\n⚠️  Some tests failed. Please check your deployment.")

if __name__ == "__main__":
    main()

