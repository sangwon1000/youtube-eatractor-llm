import time
start_time = time.time()
import os
from dotenv import load_dotenv
from llama_cpp import Llama, LlamaGrammar
from youtube_metadata import YouTubeMetadataFetcher  # Assuming this class is in youtube_metadata_fetcher.py
from recipe_extractor import RecipeExtractor
# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("YOUTUBE_API_KEY")

# Initialize the YouTubeMetadataFetcher class
fetcher = YouTubeMetadataFetcher(api_key)

# Define the video ID 백종원 레시피
video_id = "qWbHSOplcvY"

# Example usage
if __name__ == "__main__":
    video_id = "qWbHSOplcvY"
    
    extractor = RecipeExtractor(video_id)
    extractor.run()

