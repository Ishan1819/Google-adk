# import os
# from google.adk.agents import LlmAgent
# import google.generativeai as genai
# from PIL import Image
# from config import GOOGLE_API_KEY

# # Set environment variable for ADK
# os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# # Configure genai globally
# genai.configure(api_key=GOOGLE_API_KEY)

# def generate_caption(image_path: str) -> str:
#     """Generate a caption for the given image path.
    
#     Args:
#         image_path: Full path to the image file
        
#     Returns:
#         Generated Instagram caption or error message
#     """
#     if not image_path:
#         return "Error: Please provide an image path"
    
#     # Remove quotes if user included them
#     image_path = image_path.strip('"\'')
    
#     # Check if file exists
#     if not os.path.exists(image_path):
#         return f"Error: File not found at {image_path}"
    
#     try:
#         img = Image.open(image_path)
#         prompt = "Write a short, stylish Instagram caption for this photo."
        
#         model = genai.GenerativeModel("gemini-2.5-pro")
#         response = model.generate_content([prompt, img])
#         return response.text.strip()
    
#     except Exception as e:
#         return f"Error processing image: {str(e)}"

# caption_generator_agent = LlmAgent(
#     name="CaptionGeneratorAgent",
#     description="Generates Instagram-style captions for an image using Gemini",
#     model="gemini-2.5-pro",
#     tools=[generate_caption]
# )















import os
import requests
from google.adk.agents import LlmAgent
import google.generativeai as genai
from PIL import Image
from io import BytesIO
from config import GOOGLE_API_KEY

# Set environment variable for ADK
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# Configure genai globally
genai.configure(api_key=GOOGLE_API_KEY)

def generate_caption(image_url: str) -> str:
    """Generate a short Instagram caption for an online image.
    
    Args:
        image_url: URL of the image to caption
        
    Returns:
        Generated Instagram caption or error message
    """
    try:
        print(f"Starting caption generation for: {image_url}")
        
        if not image_url:
            return "Error: Please provide an image URL"
        
        # Remove quotes if user included them
        image_url = image_url.strip('"\'')
        print(f"Cleaned URL: {image_url}")
        
        # Download the image from URL
        print("Downloading image from URL...")
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Open image from bytes
        img = Image.open(BytesIO(response.content))
        print(f"Image downloaded successfully: {img.size}")
        
        # More specific prompt for Instagram captions
        prompt = """Create an engaging Instagram caption for this photo. 
        Keep it under 150 characters. Use 1-2 relevant emojis. 
        Make it catchy and Instagram-style, not a description. 
        Focus on mood, feeling, or a brief inspirational message."""
        
        print("Calling Gemini API...")
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content([prompt, img])
        
        result = response.text.strip()
        # Remove any extra quotes or formatting
        result = result.strip('"\'')
        print(f"Generated caption: {result}")
        return result
    
    except requests.RequestException as e:
        error_msg = f"Error downloading image: {str(e)}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error processing image: {str(e)}"
        print(error_msg)
        return error_msg

caption_generator_agent = LlmAgent(
    name="CaptionGeneratorAgent",
    description="Generates short, catchy Instagram-style captions for images from URLs. Ask the user for the image URL if not provided.",
    model="gemini-2.5-pro",
    tools=[generate_caption]
)