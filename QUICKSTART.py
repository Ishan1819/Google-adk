"""
🚀 QUICK START GUIDE - Best Time to Post Feature
================================================

This guide will help you get the Best Time to Post feature running quickly.

WHAT IT DOES:
-------------
Analyzes the best time to post products on Instagram by combining:
✅ Instagram Graph API - Real engagement data from your posts
✅ Gemini AI - Cultural, seasonal, and regional insights
✅ Firestore - Your historical performance data

SETUP STEPS:
============

STEP 1: Install Dependencies
-----------------------------
pip install -r requirements.txt

STEP 2: Configure Environment Variables
---------------------------------------
1. Copy .env.example to .env:
   copy .env.example .env

2. Edit .env and add your credentials:

   Required:
   - GOOGLE_API_KEY=your_gemini_api_key_here
   
   Optional (for Instagram data):
   - INSTAGRAM_ACCESS_TOKEN=your_token_here
   - INSTAGRAM_BUSINESS_ACCOUNT_ID=your_id_here

HOW TO GET CREDENTIALS:
-----------------------

📌 Google API Key (Required):
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key to your .env file

📌 Instagram Access Token (Optional but recommended):
1. Go to: https://developers.facebook.com/apps/
2. Create a new app or use existing
3. Add Instagram product
4. Get your Instagram Business Account ID
5. Generate access token with these permissions:
   - instagram_basic
   - instagram_manage_insights
   - pages_read_engagement
6. For long-lived token (60 days), exchange it:
   https://graph.facebook.com/v18.0/oauth/access_token?
   grant_type=fb_exchange_token&
   client_id={app-id}&
   client_secret={app-secret}&
   fb_exchange_token={short-lived-token}

STEP 3: Run the Server
----------------------
python main.py

The server will start at: http://127.0.0.1:8000

STEP 4: Test the API
-------------------

Option A: Browser Test
Visit: http://127.0.0.1:8000/analytics/test

Option B: Python Test Script
python test_api.py

Option C: curl Test
curl http://127.0.0.1:8000/analytics/test

USING THE API:
==============

Endpoint: POST /analytics/best-time-to-post

Example Request (PowerShell):
-----------------------------
$body = @{
    product_name = "Brass Ganesh Idol"
    category = "Spiritual Items"
    keywords = @("brass", "ganesh", "idol", "handcrafted")
    hashtags = @("#brass", "#ganesh", "#spiritual")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/analytics/best-time-to-post" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

Example Request (Python):
-------------------------
import requests

response = requests.post(
    "http://127.0.0.1:8000/analytics/best-time-to-post",
    json={
        "product_name": "Hand-painted Terracotta Pots",
        "category": "Home Decor",
        "keywords": ["terracotta", "handmade", "clay"],
        "hashtags": ["#terracotta", "#handmade"]
    }
)

result = response.json()
print(result)

RESPONSE FORMAT:
===============
{
  "status": "success",
  "data": {
    "product": "Brass Ganesh Idol",
    "category": "Spiritual Items",
    "target_region": ["Maharashtra", "Gujarat", "Karnataka"],
    "best_time_to_post": "Friday, Saturday | 7:00pm-9:00pm",
    "best_days": ["Friday", "Saturday", "Sunday"],
    "expected_engagement_improvement": "+65%",
    "season_spike": ["Ganesh Chaturthi", "Diwali"],
    "festivals": ["Ganesh Chaturthi", "Diwali"],
    "reasoning": "Spiritual items see peak demand during festival seasons...",
    "cultural_insights": "Ganesh idols are especially popular in Maharashtra..."
  }
}

TROUBLESHOOTING:
===============

❌ "GOOGLE_API_KEY not found"
→ Make sure you created .env file and added your API key

❌ Instagram API returns errors
→ It's OK! The system will use fallback estimates
→ Instagram data is optional - Gemini AI alone provides good insights

❌ "Module not found" errors
→ Run: pip install -r requirements.txt

❌ Port 8000 already in use
→ Change port in main.py: uvicorn.run(app, port=8001)

❌ Gemini API quota exceeded
→ Check your quota at: https://aistudio.google.com/
→ Free tier: 60 requests per minute

TESTING WITHOUT INSTAGRAM:
=========================
The feature works perfectly with just Gemini API!
- Instagram data weight: 50% → redistributed to Gemini
- You'll still get excellent recommendations based on:
  ✓ Cultural insights
  ✓ Seasonal trends
  ✓ Festival calendars
  ✓ Regional preferences

NEXT STEPS:
===========
1. ✅ Start server: python main.py
2. ✅ Test with sample: http://127.0.0.1:8000/analytics/test
3. ✅ Try your products: POST /analytics/best-time-to-post
4. ✅ Integrate with your frontend
5. ✅ Add Firestore for historical tracking (optional)

PRODUCTION TIPS:
===============
- Cache Gemini responses to save API costs
- Implement rate limiting on endpoints
- Set up Instagram token auto-refresh
- Add Firestore for better historical insights
- Use background tasks for bulk analysis

SUPPORT:
========
Check the full documentation: README_BEST_TIME.md

API Docs (when server is running):
http://127.0.0.1:8000/docs

Happy analyzing! 🎉
"""

print(__doc__)
