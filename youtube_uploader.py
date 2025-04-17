import os
import google_auth_httplib2
import google_auth_oauthlib
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
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
            "tags": ["AI generated" ]
        },
        "status":{
            "privacyStatus": "public"
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

        return "https://www.youtube.com/watch?v="+response['id']


