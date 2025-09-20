from google.adk.agents import LlmAgent
import requests, time
from config import ACCESS_TOKEN, INSTAGRAM_BUSINESS_ACCOUNT_ID, LOCAL_IMAGE_PATH

def post_to_instagram(caption: str, image_url: str = LOCAL_IMAGE_PATH) -> str:
    """Post an image with a caption to Instagram via Graph API."""
    # Step 1: Create media container
    create_url = f"https://graph.facebook.com/v20.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(create_url, data=payload).json()

    if "id" not in response:
        return f"❌ Error creating media container: {response}"
    container_id = response["id"]

    # Step 2: Publish container
    time.sleep(5)
    publish_url = f"https://graph.facebook.com/v20.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"
    publish_payload = {
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN
    }
    publish_response = requests.post(publish_url, data=publish_payload).json()

    if "id" in publish_response:
        return f"✅ Successfully posted! Post ID: {publish_response['id']}"
    return f"❌ Error publishing post: {publish_response}"

instagram_poster_agent = LlmAgent(
    name="InstagramPosterAgent",
    description="Posts an image and caption to Instagram automatically",
    model="gemini-2.5-pro",  # Not used for reasoning, but keeps LLM Agent structure
    tools=[post_to_instagram]  # Register tool directly in the constructor
)