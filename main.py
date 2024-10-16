import time
start_time = time.time()
import os
from dotenv import load_dotenv
from llama_cpp import Llama, LlamaGrammar
from youtube_metadata import YouTubeMetadataFetcher  # Assuming this class is in youtube_metadata_fetcher.py
from recipe_extractor import RecipeExtractor
from restaurant_extractor import RestaurantExtractor
# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("YOUTUBE_API_KEY")

# Initialize the YouTubeMetadataFetcher class
fetcher = YouTubeMetadataFetcher(api_key)

# Example usage
if __name__ == "__main__":
    recipe_video_id = "qWbHSOplcvY"
    
    # extractor = RecipeExtractor(recipe_video_id)
    # extractor.run()

    restaurant_video_id = "wu1fOmsPEr8"
    extractor = RestaurantExtractor(restaurant_video_id)
    extractor.run()