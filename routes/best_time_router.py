from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from agents.best_time_analyzer import BestTimeAnalyzer

router = APIRouter(prefix="/analytics", tags=["Best Time Analytics"])

class BestTimeRequest(BaseModel):
    product_name: str
    category: str
    keywords: List[str]
    hashtags: Optional[List[str]] = None

@router.post("/best-time-to-post")
async def best_time_to_post(request: BestTimeRequest):
    """
    Analyze the best time to post a product on Instagram
    
    Combines:
    - Instagram Graph API engagement data (50% weight)
    - Gemini AI cultural/seasonal insights (30% weight)
    - Firestore historical performance (20% weight)
    
    Example Request:
    {
        "product_name": "Hand-painted Terracotta Pots",
        "category": "Home Decor",
        "keywords": ["terracotta", "handmade", "clay", "pots"],
        "hashtags": ["#terracotta", "#handmade", "#homedecor"]
    }
    
    Example Response:
    {
        "product": "Hand-painted Terracotta Pots",
        "category": "Home Decor",
        "target_region": ["Maharashtra", "Gujarat"],
        "best_time_to_post": "Friday, Saturday | 7:00pm-9:00pm",
        "expected_engagement_improvement": "+67%",
        "season_spike": ["Diwali", "Gudi Padwa"],
        "reasoning": "...",
        ...
    }
    """
    try:
        analyzer = BestTimeAnalyzer()
        
        result = analyzer.analyze(
            product_name=request.product_name,
            category=request.category,
            keywords=request.keywords,
            hashtags=request.hashtags
        )
        
        if "error" in result and not result.get("product"):
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/test")
async def test_best_time():
    """
    Test endpoint with sample data
    """
    try:
        analyzer = BestTimeAnalyzer()
        
        result = analyzer.analyze(
            product_name="Brass Ganesh Idol",
            category="Spiritual Items",
            keywords=["brass", "ganesh", "idol", "statue", "handcrafted"],
            hashtags=["#brass", "#ganesh", "#spiritual", "#handmade"]
        )
        
        return {
            "status": "success",
            "message": "Test analysis completed",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")
