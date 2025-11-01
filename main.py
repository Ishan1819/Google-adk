from fastapi import FastAPI
from routes.caption_router import router as caption_router
from routes.insta_router import router as instagram_router
from routes.translator_router import router as translate_router
from routes.best_time_router import router as best_time_router
app = FastAPI(title="Instagram Pipeline API")

# Include Routers
app.include_router(caption_router)
app.include_router(instagram_router)
app.include_router(translate_router)
app.include_router(best_time_router)
@app.get("/")
async def root():
    return {"message": "🚀 Instagram Pipeline is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
