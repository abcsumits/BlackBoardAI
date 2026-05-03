import os
import google_auth_httplib2
import google_auth_oauthlib
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
from thumbnail import generate_thumbnail
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
#while hosting remember to add web server url to https://console.cloud.google.com/auth/clients/create?project=uploader-453023
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def authenticate_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    # Load client secrets file, put the path of your file
    client_secrets_file = "token.json"

    
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    credentials = flow.run_local_server()

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

    return youtube

def upload_video(description,title,uid):
    youtube = authenticate_youtube()
    request_body = {
        "snippet": {
            "categoryId": "27",
            "title": title,
            "description": description,
            "tags": ["AI" ,"Deep Learning", "Technology", "Education"]
        },
        "status":{
            "privacyStatus": "private"
        }
    }

    # put the path of the video that you want to upload
    media_file = "combined_video"+uid+".mp4"

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(media_file, chunksize=-1, resumable=True)
    )

    response = None 

    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload {int(status.progress()*100)}%")
    thumbnail_path="thumbnail_"+uid
    generate_thumbnail(title, output_filename=thumbnail_path+".svg")
    thumbnail_path+=".png"
    if thumbnail_path:
        try:
            thumb_req = youtube.thumbnails().set(
                videoId=response['id'],
                media_body=MediaFileUpload(thumbnail_path)
            )
            thumb_resp = thumb_req.execute()
            print("Thumbnail uploaded:", thumb_resp)
        except HttpError as e:
            # thumbnail upload failed — video was uploaded but thumbnail not set
            print("Thumbnail upload failed:", e)
    return "https://www.youtube.com/watch?v="+response['id']


