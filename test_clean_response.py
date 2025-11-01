"""
Quick test to verify the cleaned response format
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_clean_response():
    print("=" * 70)
    print("🧪 TESTING CLEAN RESPONSE FORMAT")
    print("=" * 70)
    
    payload = {
        "product_name": "Silver Oxidized Earrings",
        "category": "Jewelry",
        "keywords": ["silver", "earrings", "oxidized", "handmade"],
        "hashtags": ["#silverjewelry", "#handmade", "#jewelry"]
    }
    
    print("\n📤 Sending request...")
    response = requests.post(
        f"{BASE_URL}/analytics/best-time-to-post",
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        result = data.get("data", {})
        
        print("\n✅ SUCCESS! Clean Response:")
        print("=" * 70)
        print(f"📦 Product: {result.get('product')}")
        print(f"📂 Category: {result.get('category')}")
        print(f"\n📍 Target Regions: {', '.join(result.get('target_region', []))}")
        print(f"\n⏰ Best Time to Post: {result.get('best_time_to_post')}")
        print(f"\n🎊 Season Spike: {', '.join(result.get('season_spike', []))}")
        print(f"\n🎉 Festivals: {', '.join(result.get('festivals', []))}")
        print(f"\n📈 Expected Improvement: {result.get('expected_engagement_improvement')}")
        print(f"\n💡 Reasoning:\n{result.get('reasoning', '')}")
        
        print("\n" + "=" * 70)
        print("📋 RESPONSE STRUCTURE:")
        print("=" * 70)
        print(json.dumps(result, indent=2))
        
        print("\n" + "=" * 70)
        print("✅ VERIFICATION:")
        print("=" * 70)
        print(f"✓ Product: {'✅' if 'product' in result else '❌'}")
        print(f"✓ Category: {'✅' if 'category' in result else '❌'}")
        print(f"✓ Target Region: {'✅' if 'target_region' in result else '❌'}")
        print(f"✓ Best Time: {'✅' if 'best_time_to_post' in result else '❌'}")
        print(f"✓ Season Spike: {'✅' if 'season_spike' in result else '❌'}")
        print(f"✓ Festivals: {'✅' if 'festivals' in result else '❌'}")
        print(f"✓ Reasoning: {'✅' if 'reasoning' in result else '❌'}")
        print(f"✓ Expected Improvement: {'✅' if 'expected_engagement_improvement' in result else '❌'}")
        
        # Check for unwanted fields
        unwanted = ['detailed_analysis', 'data_sources', 'best_days', 'best_time_slots', 'cultural_insights']
        print(f"\n✓ No extra fields: {'✅' if not any(field in result for field in unwanted) else '❌ Found: ' + str([f for f in unwanted if f in result])}")
        
        print("\n" + "=" * 70)
        
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    try:
        test_clean_response()
    except requests.exceptions.ConnectionError:
        print("\n❌ Server not running!")
        print("Please start: python main.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
