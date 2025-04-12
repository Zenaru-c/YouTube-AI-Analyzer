# ##[*.imported modules]
import os
import re
import googleapiclient.discovery
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential

# ##[*.azure and youtube api setup]
endpoint = "https://models.inference.ai.azure.com"
model_name = "Phi-3-medium-4k-instruct"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyCmu8Yr1m1_qUi886PN26w-Dk9WOaLdIFw"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

# ##[*.regex for youtube id]
def extract_video_id(url):
    pattern = r"(?:youtu\.be/|youtube\.com/(?:.*[?&]v=|embed/|v/))([^?&]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

# ##[*.ai analysis]
def analyze_youtube_comments(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return "Invalid YouTube URL. Please make sure it is correct."

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=8
    )
    response = request.execute()

    comments = []
    for item in response["items"]:
        comments.append(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])

    comments_text = "\n".join(comments)
    user_message = (
        f"Here are some comments from a YouTube video:\n{comments_text}\n"
        "Based on the provided comments, do you believe the video is good, bad or questionable? Answer by saying one of these words(good, bad, questionable), and explain in 2 sentences why you think so. If there are no comments present then answer by saying (no comments present)."
    )

    ai_response = client.complete(
        messages=[UserMessage(user_message)],
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
        model=model_name
    )

    return ai_response.choices[0].message.content
