from fastapi import APIRouter, UploadFile, File
import os
import tempfile
from pydantic import BaseModel
from agents.subagents.caption_generate.caption_generator import caption_generator_agent
from agents.subagents.insta_generate.instagram_poster import instagram_poster_agent

router = APIRouter(prefix="/caption", tags=["caption"])

class CaptionResponse(BaseModel):
    success: bool
    caption: str | None = None
    post_result: str | None = None
    error: str | None = None

@router.post("/generate", response_model=CaptionResponse)
async def generate_caption(image: UploadFile = File(...)):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image.filename)[1]) as temp_file:
            # Write uploaded file content to temporary file
            content = await image.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Generate caption using the caption generator agent
            caption = caption_generator_agent.tools[0](temp_file_path)
            
            # Post to Instagram using the poster agent
            post_result = instagram_poster_agent.tools[0](caption, temp_file_path)
            
            return CaptionResponse(
                success=True,
                caption=caption,
                post_result=post_result
            )
        finally:
            # Clean up - delete the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                
    except Exception as e:
        return CaptionResponse(
            success=False,
            error=str(e)
        )