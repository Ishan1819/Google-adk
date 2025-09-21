# from agents import root_agent
# import asyncio

# def run_pipeline():
#     """Run the Instagram post pipeline"""
#     print("🚀 Starting Insta Auto Post Pipeline...")
#     try:
#         # First generate the caption
#         caption = root_agent.sub_agents[0].tools[0](root_agent.inputs["image_path"])
#         print(f"📝 Generated caption: {caption}")

#         # Then post to Instagram
#         result = root_agent.sub_agents[1].tools[0](caption=caption)
#         print("🎉 Pipeline Result:", result)
#         return result
#     except Exception as e:
#         error_msg = f"❌ Pipeline Error: {str(e)}"
#         print(error_msg)
#         return error_msg

# if __name__ == "__main__":
#     run_pipeline()














import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from caption_backend import router as caption_router

# Load environment variables
load_dotenv()

# FastAPI app setup
app = FastAPI(title="Instagram Auto Post API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(caption_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)