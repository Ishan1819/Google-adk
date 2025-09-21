import os
from google.adk.agents import LlmAgent
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# -----------------------
# Configure Google Gemini
# -----------------------
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)


def generate_caption_from_file(image_path: str) -> str:
    """
    Generate a short Instagram caption for a local image file.

    Args:
        image_path: Path to the image file on local device.

    Returns:
        Generated Instagram caption or error message.
    """
    try:
        if not os.path.exists(image_path):
            return f"❌ Error: File not found - {image_path}"

        # Open image directly
        img = Image.open(image_path)
        print(f"✅ Loaded image: {image_path}, size: {img.size}")

        # Prompt for Gemini
        prompt = """Create an engaging Instagram caption for this photo.
        Add a dummy artisan name compulsorily for now (Example -by Keshav Mahotsani)
        Keep it under 300 characters. Use 1-2 relevant emojis.
        Make it catchy and Instagram-style, not a description. Make it breath taking and very relevant.
        Focus on mood, feeling, or a brief inspirational message."""

        print("🌀 Calling Gemini API...")
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content([prompt, img])

        # Clean the output
        result = response.text.strip().strip('"\'')
        print(f"📝 Generated caption: {result}")
        return result

    except Exception as e:
        return f"❌ Error processing image: {str(e)}"


# -----------------------
# Define ADK LLM Agent
# -----------------------
caption_generator_agent = LlmAgent(
    name="CaptionGeneratorAgent",
    description=(
        "Generates short, catchy Instagram-style captions "
        "for local images on your device."
    ),
    model="gemini-2.5-pro",
    tools=[generate_caption_from_file]
)
