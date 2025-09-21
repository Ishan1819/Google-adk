from fastapi import APIRouter
from pydantic import BaseModel
from agents.subagents.caption_generate.caption_generator import caption_generator_agent
from agents.subagents.insta_generate.instagram_poster import instagram_poster_agent

router = APIRouter(prefix="/caption", tags=["caption"])

class ImageRequest(BaseModel):
    image_path: str

class CaptionResponse(BaseModel):
    success: bool
    caption: str | None = None
    post_result: str | None = None
    error: str | None = None

@router.post("/generate", response_model=CaptionResponse)
async def generate_caption(request: ImageRequest):
    try:
        # Generate caption using the caption generator agent
        caption = caption_generator_agent.tools[0](request.image_path)
        
        # Post to Instagram using the poster agent
        post_result = instagram_poster_agent.tools[0](caption, request.image_path)
        
        return CaptionResponse(
            success=True,
            caption=caption,
            post_result=post_result
        )
    except Exception as e:
        return CaptionResponse(
            success=False,
            error=str(e)
        )