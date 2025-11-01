# Best Time to Post Feature 🚀

## Overview

AI-powered recommendation engine that combines:

- **Instagram Graph API** (50% weight) - Real engagement data
- **Gemini AI** (30% weight) - Cultural & seasonal insights
- **Firestore** (20% weight) - Your historical performance

## Setup Instructions

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
GOOGLE_API_KEY=your_gemini_api_key
INSTAGRAM_ACCESS_TOKEN=your_instagram_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_business_account_id
```

#### Getting Instagram Access Token:

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create an App → Products → Instagram → Instagram Graph API
3. Get your Business Account ID from Instagram Settings
4. Generate a User Access Token with permissions: `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`
5. Convert to long-lived token (60 days):
   ```
   https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-lived-token}
   ```

#### Getting Google API Key:

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create API key
3. Enable Generative Language API

### 3. Run the Server

```powershell
python main.py
```

Or with uvicorn:

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## API Endpoints

### 1. POST `/analytics/best-time-to-post`

Analyze best time to post for a product.

**Request Body:**

```json
{
  "product_name": "Hand-painted Terracotta Pots",
  "category": "Home Decor",
  "keywords": ["terracotta", "handmade", "clay", "pots"],
  "hashtags": ["#terracotta", "#handmade", "#homedecor"]
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "product": "Hand-painted Terracotta Pots",
    "category": "Home Decor",
    "target_region": ["Maharashtra", "Gujarat", "Rajasthan"],
    "best_time_to_post": "Friday, Saturday | 7:00pm-9:00pm",
    "best_days": ["Friday", "Saturday", "Sunday"],
    "best_time_slots": ["7:00pm-9:00pm", "11:00am-1:00pm"],
    "expected_engagement_improvement": "+67%",
    "season_spike": ["Diwali", "Gudi Padwa"],
    "festivals": ["Diwali", "Ganesh Chaturthi"],
    "reasoning": "Traditional home decor items see increased demand during festival preparation periods...",
    "cultural_insights": "Terracotta products align with eco-friendly trends and traditional aesthetics...",
    "data_sources": {
      "instagram": "instagram_graph_api",
      "gemini": "ai_analysis",
      "firestore": "mock_data"
    },
    "detailed_analysis": {
      "instagram_insights": {...},
      "gemini_insights": {...},
      "historical_performance": {...}
    }
  }
}
```

### 2. GET `/analytics/test`

Test endpoint with sample data (Brass Ganesh Idol).

**Example:**

```bash
curl http://127.0.0.1:8000/analytics/test
```

## How It Works

### Algorithm Flow:

```
1. Instagram Graph API
   └─> Fetch last 50 posts
   └─> Filter by category/hashtags
   └─> Analyze engagement patterns
   └─> Extract peak times & days

2. Gemini AI Analysis
   └─> Analyze seasonal demand
   └─> Identify cultural relevance
   └─> Determine regional preferences
   └─> Predict festival spikes

3. Firestore Historical Data
   └─> Query past performance
   └─> Extract best performing times
   └─> Calculate average engagement

4. Weighted Combination
   └─> Instagram: 50% weight
   └─> Gemini: 30% weight
   └─> Firestore: 20% weight
   └─> Return final recommendation
```

## Testing

### Quick Test:

```powershell
# Start server
python main.py

# In another terminal or browser:
# Visit: http://127.0.0.1:8000/analytics/test
```

### Custom Test:

```powershell
curl -X POST "http://127.0.0.1:8000/analytics/best-time-to-post" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Brass Ganesh Idol",
    "category": "Spiritual Items",
    "keywords": ["brass", "ganesh", "idol", "handcrafted"],
    "hashtags": ["#brass", "#ganesh", "#spiritual"]
  }'
```

## Firestore Integration (Optional)

To enable historical data tracking:

1. Create a Firebase project
2. Download service account credentials JSON
3. Set environment variable:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
   ```
4. Update `fetch_firestore_history()` in `agents/best_time_analyzer.py`

Example Firestore structure:

```
posts/
  {post_id}/
    - product_name
    - category
    - posted_at
    - views
    - likes
    - comments
    - engagement_rate
```

## Troubleshooting

### Instagram API Returns 400/401

- Check access token is valid (not expired)
- Verify Business Account ID is correct
- Ensure you have correct permissions

### Gemini API Errors

- Verify GOOGLE_API_KEY is set correctly
- Check API quota limits
- Ensure Generative Language API is enabled

### No Instagram Data

- The system will use fallback estimates
- Check if access token has insights permission
- Verify Business Account has recent posts

## Production Recommendations

1. **Cache Results**: Cache Gemini responses for similar products (save API costs)
2. **Rate Limiting**: Add rate limiting to prevent abuse
3. **Async Processing**: For multiple products, use background tasks
4. **Firestore**: Implement full Firestore integration for better historical insights
5. **Monitoring**: Log all API calls and errors
6. **Token Refresh**: Implement Instagram token auto-refresh

## Example Use Cases

### Use Case 1: Festival Product Launch

```json
{
  "product_name": "Handmade Diya Set",
  "category": "Festival Decor",
  "keywords": ["diya", "diwali", "handmade", "clay"]
}
```

### Use Case 2: Regional Craft

```json
{
  "product_name": "Madhubani Painting",
  "category": "Art",
  "keywords": ["madhubani", "folk art", "bihar", "painting"]
}
```

### Use Case 3: Seasonal Product

```json
{
  "product_name": "Woolen Shawl",
  "category": "Fashion",
  "keywords": ["woolen", "shawl", "winter", "handwoven"]
}
```

## Support

For issues or questions, check:

- Instagram Graph API Docs: https://developers.facebook.com/docs/instagram-api
- Gemini API Docs: https://ai.google.dev/docs
- FastAPI Docs: https://fastapi.tiangolo.com/
