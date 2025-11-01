"""
Test Instagram API connection after fixing the metric error
"""
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def test_instagram_api():
    print("=" * 60)
    print("🧪 Testing Instagram Graph API Connection")
    print("=" * 60)
    
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    business_account_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    
    if not access_token or not business_account_id:
        print("❌ Missing Instagram credentials in .env file")
        return
    
    print(f"\n✅ Access Token: {access_token[:20]}...")
    print(f"✅ Business Account ID: {business_account_id}")
    
    # Test 1: Get account info
    print("\n" + "-" * 60)
    print("Test 1: Getting account information...")
    print("-" * 60)
    
    account_url = f"https://graph.facebook.com/v18.0/{business_account_id}"
    account_params = {
        "fields": "id,username,name,media_count,followers_count",
        "access_token": access_token
    }
    
    try:
        response = requests.get(account_url, params=account_params)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Username: {data.get('username', 'N/A')}")
            print(f"✅ Name: {data.get('name', 'N/A')}")
            print(f"✅ Media Count: {data.get('media_count', 'N/A')}")
            print(f"✅ Followers: {data.get('followers_count', 'N/A')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 2: Get recent media with FIXED metrics
    print("\n" + "-" * 60)
    print("Test 2: Getting recent media (FIXED metrics)...")
    print("-" * 60)
    
    media_url = f"https://graph.facebook.com/v18.0/{business_account_id}/media"
    media_params = {
        "fields": "id,caption,like_count,comments_count,timestamp,media_type,insights.metric(impressions,reach,saved)",
        "access_token": access_token,
        "limit": 5
    }
    
    try:
        response = requests.get(media_url, params=media_params)
        if response.status_code == 200:
            data = response.json()
            posts = data.get("data", [])
            print(f"✅ Found {len(posts)} recent posts")
            
            for i, post in enumerate(posts[:3], 1):
                print(f"\n  Post {i}:")
                print(f"    - Media Type: {post.get('media_type', 'N/A')}")
                print(f"    - Likes: {post.get('like_count', 0)}")
                print(f"    - Comments: {post.get('comments_count', 0)}")
                print(f"    - Timestamp: {post.get('timestamp', 'N/A')}")
                
                # Check insights
                insights = post.get("insights", {}).get("data", [])
                if insights:
                    print(f"    - Insights:")
                    for insight in insights:
                        metric = insight.get("name")
                        value = insight.get("values", [{}])[0].get("value", 0)
                        print(f"      • {metric}: {value}")
                else:
                    print(f"    - No insights available (post may be too recent)")
                
                caption = post.get("caption", "")
                if caption:
                    preview = caption[:60] + "..." if len(caption) > 60 else caption
                    print(f"    - Caption: {preview}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ Instagram API Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_instagram_api()
