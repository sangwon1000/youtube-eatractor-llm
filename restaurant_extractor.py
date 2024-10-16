"""
https://www.youtube.com/watch?v=wu1fOmsPEr8&list=PLuMuHAJh9g_Py_PSm8gmHdlcil6CQ9QCM&index=154

this video is review of restaurant(s)

both in korean and englsih
what restaurant is covered?
what dishes are covered?
what is being said about each dish covered?
"""
import time
import os
from dotenv import load_dotenv
from llama_cpp import Llama, LlamaGrammar
from youtube_metadata import YouTubeMetadataFetcher  # Assuming this class is in youtube_metadata_fetcher.py

class RestaurantExtractor:
    def __init__(self, video_id: str, grammar_file_path: str = './recipe.gbnf'):
        # Load environment variables from .env file
        load_dotenv()

        # Get the API key from environment variables
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.video_id = video_id
        self.grammar_file_path = grammar_file_path  # Grammar file path now internal to the class

        # Initialize YouTubeMetadataFetcher
        self.fetcher = YouTubeMetadataFetcher(self.api_key)

        # Load the LLaMA model and the grammar
        self.llm = self.load_llama_model()
        self.grammar = self.load_grammar()

    def load_llama_model(self):
        # Load the LLaMA model
        return Llama.from_pretrained(
            repo_id="ggml-org/Meta-Llama-3.1-8B-Instruct-Q4_0-GGUF",
            filename="meta-llama-3.1-8b-instruct-q4_0.gguf",
            n_ctx=4096
        )

    def load_grammar(self):
        # Load GBNF grammar file
        with open(self.grammar_file_path, 'r') as f:
            grammar_text = f.read()

        # Create and return LlamaGrammar object from GBNF text
        return LlamaGrammar.from_string(grammar_text)

    def fetch_metadata(self):
        # Retrieve video metadata
        metadata = self.fetcher.get_video_metadata(self.video_id)

        # Extract relevant metadata fields
        video_metadata = {
            "title_local": metadata['local']['title'],
            "description_local": metadata['local']['description'],
            "title_english": metadata['english']['title'],
            "description_english": metadata['english']['description']
        }

        print("Video Metadata:")
        print(f"Local Title: {video_metadata['title_local']}")
        print(f"Local Description: {video_metadata['description_local']}")
        print(f"English Title: {video_metadata['title_english']}")
        print(f"English Description: {video_metadata['description_english']}")

        return video_metadata

    def fetch_transcript(self):
        # Fetch transcript using YouTubeMetadataFetcher
        transcript_string = self.fetcher.get_transcript_as_string(self.video_id)
        if transcript_string:
            print("\nTranscript:")
            print(transcript_string)
        return transcript_string

    def extract_restaurants(self, transcript_string, metadata):
        # Define the user query with metadata included in the context
        user_query = """
        This is a transcript from a video discussing restaurants. Based on the provided transcript and metadata about the video, identify all the restaurants mentioned, along with their locations.

        Provide the answer strictly in valid JSON format like this:
        {
            "restaurants": [
                {"name": "restaurant1", "location": "city or address"},
                {"name": "restaurant2", "location": "city or address"}
                // ... more restaurants
            ]
        }
        """

        # Combine metadata and transcript into the context
        prompt_with_context = f"""
        Video Metadata:
        Local Title: {metadata['title_local']}
        Local Description: {metadata['description_local']}
        English Title: {metadata['title_english']}
        English Description: {metadata['description_english']}

        Transcript: {transcript_string}

        User: {user_query}
        """

        # Generate a completion using LLaMA
        response = self.llm.create_chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt_with_context
                }
            ],
            # grammar=self.grammar
        )

        # Print the extracted restaurants
        print("\nExtracted Restaurants:")
        print(response)

        return response

    def run(self):
        # Start time tracking
        start_time = time.time()

        # Fetch metadata
        metadata = self.fetch_metadata()

        # Fetch transcript
        transcript_string = self.fetch_transcript()

        if transcript_string:
            # Extract restaurant information using transcript and metadata
            response = self.extract_restaurants(transcript_string, metadata)

            #pretty print the dictionary
            print(response)
            import json

            def pretty_print(data):
                """
                Pretty prints a dictionary or a JSON string in a formatted way.

                :param data: A dictionary or a JSON string
                """
                # Check if input is a JSON string
                if isinstance(data, str):
                    try:
                        # Parse the JSON string into a dictionary
                        data = json.loads(data)
                    except json.JSONDecodeError:
                        print("Invalid JSON string")
                        return

                # Check if input is a dictionary
                if isinstance(data, dict):
                    # Print the dictionary in a pretty JSON format
                    print(json.dumps(data, indent=4, sort_keys=True))
                else:
                    print("Input must be a dictionary or a JSON string")

            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")

            pretty_print(content)
            
            # next is to extract dishes and comments about each

            # search API


        # End time tracking
        end_time = time.time()
        print(f"Runtime of the program: {end_time - start_time} seconds")

