from google.adk.agents import LlmAgent
import requests, time
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
LOCAL_IMAGE_PATH = os.getenv("LOCAL_IMAGE_PATH")
CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY")
CLOUD_API_SECRET = os.getenv("CLOUD_API_SECRET")

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=CLOUD_API_KEY,
    api_secret=CLOUD_API_SECRET

)

def post_to_instagram(caption: str, image_path: str = LOCAL_IMAGE_PATH) -> str:
    """
    Uploads a local image to Cloudinary, then posts it to Instagram with caption.
    """
    try:
        # Step 1: Upload image to Cloudinary
        print(f"Uploading {image_path} to Cloudinary...")
        upload_result = cloudinary.uploader.upload(image_path)
        image_url = upload_result["secure_url"]
        print(f"✅ Uploaded to Cloudinary: {image_url}")

        # Step 2: Create media container with image_url
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

        # Step 3: Publish container
        time.sleep(5)  # wait for processing
        publish_url = f"https://graph.facebook.com/v20.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"
        publish_payload = {
            "creation_id": container_id,
            "access_token": ACCESS_TOKEN
        }
        publish_response = requests.post(publish_url, data=publish_payload).json()

        if "id" in publish_response:
            return f"✅ Successfully posted! Post ID: {publish_response['id']}"
        return f"❌ Error publishing post: {publish_response}"

    except FileNotFoundError:
        return f"❌ Error: File not found - {image_path}"
    except Exception as e:
        return f"❌ Error posting to Instagram: {str(e)}"


# -----------------------
# Define ADK LLM Agent
# -----------------------
instagram_poster_agent = LlmAgent(
    name="InstagramPosterAgent",
    description="Uploads a local image to Cloudinary, then posts it with a caption to Instagram.",
    model="gemini-2.5-pro",  # Not really used for reasoning
    tools=[post_to_instagram]
)
