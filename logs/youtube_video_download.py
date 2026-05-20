import requests

def get_video_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        return f"Error downloading video: {e}"

def generate_compliance_log(message):
    with open('youtube_video_download.log', 'a') as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")

# Example usage
url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
video_file = get_video_file(url)
generate_compliance_log(f"API call returned a video file for a valid YouTube URL: {url}")