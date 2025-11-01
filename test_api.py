"""
Test the API endpoints using requests
Make sure the server is running first: python main.py
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_root():
    """Test root endpoint"""
    print("🔍 Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_best_time_endpoint():
    """Test the best time to post endpoint"""
    print("🔍 Testing /analytics/test endpoint...")
    response = requests.get(f"{BASE_URL}/analytics/test")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.text}\n")

def test_custom_product():
    """Test with custom product data"""
    print("\n🔍 Testing /analytics/best-time-to-post with custom product...")
    
    payload = {
        "product_name": "Hand-painted Terracotta Pots",
        "category": "Home Decor",
        "keywords": ["terracotta", "handmade", "clay", "pots", "decor"],
        "hashtags": ["#terracotta", "#handmade", "#homedecor", "#artisan"]
    }
    
    response = requests.post(
        f"{BASE_URL}/analytics/best-time-to-post",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        result = data.get("data", {})
        
        print(f"\n✨ Product: {result.get('product')}")
        print(f"📍 Target Regions: {', '.join(result.get('target_region', []))}")
        print(f"⏰ Best Time: {result.get('best_time_to_post')}")
        print(f"📈 Expected Boost: {result.get('expected_engagement_improvement')}")
        print(f"🎊 Festivals: {', '.join(result.get('festivals', []))}")
        print(f"\n💡 {result.get('reasoning', '')}\n")
    else:
        print(f"Error: {response.text}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 API ENDPOINT TESTING")
    print("=" * 60)
    print("⚠️  Make sure the server is running: python main.py")
    print("=" * 60 + "\n")
    
    try:
        test_root()
        test_best_time_endpoint()
        test_custom_product()
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server")
        print("Please start the server first: python main.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
