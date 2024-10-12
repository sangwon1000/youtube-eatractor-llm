import os
import requests
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

class YouTubeMetadataFetcher:
    def __init__(self, api_key):
        """Initialize the fetcher with the YouTube API key."""
        self.api_key = api_key
    
    def _fetch_metadata(self, video_id, language_code=None):
        """Fetch video metadata in a specific language or local language if language_code is None."""
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={self.api_key}"
        if language_code:
            url += f"&hl={language_code}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                snippet = data['items'][0]['snippet']
                return snippet['title'], snippet['description']
        return None, None
    
    def get_video_metadata(self, video_id):
        """Get video metadata in both local language and English."""
        title_local, description_local = self._fetch_metadata(video_id)
        title_english, description_english = self._fetch_metadata(video_id, language_code='en')
        
        return {
            "local": {"title": title_local, "description": description_local},
            "english": {"title": title_english, "description": description_english}
        }
    
    def get_transcript_as_string(self, video_id):
        """Fetch the transcript of the video and return it as a concatenated string."""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            # Concatenate all text entries into a single string
            full_transcript = " ".join(entry['text'] for entry in transcript)
            return full_transcript
        except Exception as e:
            print(f"Error fetching transcript: {e}")
            return None
        
    def get_playlists(self, channel_id, max_results=50):
        """Fetch the list of playlists for a given YouTube channel."""
        url = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={channel_id}&maxResults={max_results}&key={self.api_key}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            playlists = []
            for item in data.get('items', []):
                playlist_info = {
                    "title": item['snippet']['title'],
                    "description": item['snippet']['description'],
                    "playlist_id": item['id']
                }
                playlists.append(playlist_info)
            return playlists
        else:
            print(f"Error fetching playlists: {response.status_code}, {response.text}")
            return None
        
# given playlist id, get all videos in the playlist
    def get_playlist_videos(self, playlist_id, max_results=50):
        """Fetch the list of videos in a given YouTube playlist."""
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults={max_results}&key={self.api_key}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            videos = []
            for item in data.get('items', []):
                video_info = {
                    "title": item['snippet']['title'],
                    "video_id": item['snippet']['resourceId']['videoId']
                }
                videos.append(video_info)
            return videos
        else:
            print(f"Error fetching videos: {response.status_code}, {response.text}")
            return None
