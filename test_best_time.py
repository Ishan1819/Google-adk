"""
Quick test script for Best Time to Post feature
Run this after setting up your .env file
"""
import asyncio
from agents.best_time_analyzer import BestTimeAnalyzer

async def test_analyzer():
    print("=" * 60)
    print("🧪 Testing Best Time to Post Analyzer")
    print("=" * 60)
    
    analyzer = BestTimeAnalyzer()
    
    # Test with sample product
    print("\n📦 Analyzing: Brass Ganesh Idol")
    print("-" * 60)
    
    result = analyzer.analyze(
        product_name="Brass Ganesh Idol",
        category="Spiritual Items",
        keywords=["brass", "ganesh", "idol", "statue", "handcrafted"],
        hashtags=["#brass", "#ganesh", "#spiritual", "#handmade"]
    )
    
    print("\n✨ RESULTS:")
    print("-" * 60)
    print(f"🎯 Product: {result['product']}")
    print(f"📂 Category: {result['category']}")
    print(f"📍 Target Regions: {', '.join(result['target_region'])}")
    print(f"⏰ Best Time: {result['best_time_to_post']}")
    print(f"📈 Expected Boost: {result['expected_engagement_improvement']}")
    print(f"🎊 Festivals: {', '.join(result['festivals'])}")
    print(f"📅 Season Spike: {', '.join(result['season_spike'])}")
    print(f"\n💡 Reasoning:\n{result['reasoning']}")
    print(f"\n🌏 Cultural Insights:\n{result['cultural_insights']}")
    
    print("\n" + "=" * 60)
    print("✅ Test completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_analyzer())
