#!/usr/bin/env python3
"""
instagram_resumable_upload.py
Official-ish resumable upload flow for Instagram / Facebook (Graph API rupload).
Uses only Python stdlib. Works for local files (uploads binary to rupload host),
then finishes the container and publishes.

Caveats:
 - Exact endpoints/params can vary by Graph API version and whether you call a Page endpoint
   (video_reels) or Instagram user endpoint (/media). If you get a 400 / unexpected JSON,
   paste the response and I'll adapt.
 - Large files or interrupted connections may require chunked uploads. This simple impl
   attempts to upload the whole file in one request to the provided `upload_url`. If the
   server returns an expected-chunk-range, the code will currently raise and instruct how
   to perform chunked uploads (we can add that if you need it).
"""

import json
import os
import sys
import time
from urllib import request, parse, error
from urllib.parse import urlparse
import http.client

GRAPH_BASE = "https://graph.facebook.com"
DEFAULT_API_VERSION = "v17.0"  # change if you need another version

def _post_form(url: str, params: dict, timeout: int = 60):
    data = parse.urlencode(params).encode("utf-8")
    req = request.Request(url, data=data, method="POST")
    req.add_header("User-Agent", "python-instagram-resumable/1.0")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except error.HTTPError as he:
        body = he.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTPError {he.code}: {body}")
    except error.URLError as ue:
        raise RuntimeError(f"URLError: {ue}")

def _get_json(url: str, timeout: int = 30):
    req = request.Request(url, method="GET")
    req.add_header("User-Agent", "python-instagram-resumable/1.0")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as he:
        body = he.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTPError {he.code}: {body}")
    except error.URLError as ue:
        raise RuntimeError(f"URLError: {ue}")

def _upload_binary_to_rupload(upload_url: str, access_token: str, file_path: str, chunk_size: int = 64*1024):
    """
    Sends the file bytes to the rupload URL returned by the Graph API init call.
    This implementation attempts a single POST of the full file bytes (streamed).
    If the rupload endpoint requires chunked / ranged uploads, you'll get an error
    telling you the expected ranges — at that point we can implement byte-range uploads.
    """
    parsed = urlparse(upload_url)
    if parsed.scheme != "https":
        raise ValueError("upload_url must be HTTPS")

    host = parsed.hostname
    path = parsed.path
    if parsed.query:
        path += "?" + parsed.query

    conn = http.client.HTTPSConnection(host, timeout=300)
    headers = {
        "Authorization": f"OAuth {access_token}",
        "Content-Type": "application/octet-stream",
        "User-Agent": "python-instagram-resumable/1.0",
    }

    filesize = os.path.getsize(file_path)
    # Some rupload endpoints like a Content-Length header
    headers["Content-Length"] = str(filesize)
    # Some examples include an 'offset' header; we send offset: 0 for a single-shot upload
    headers["offset"] = "0"
    # send file in streaming fashion
    try:
        conn.putrequest("POST", path, skip_host=True, skip_accept_encoding=True)
        conn.putheader("Host", host)
        for k, v in headers.items():
            conn.putheader(k, v)
        conn.endheaders()

        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                conn.send(chunk)

        response = conn.getresponse()
        data = response.read().decode("utf-8", errors="ignore")
        status = response.status
        conn.close()
        # rupload often returns a short JSON or plain success, try parse
        try:
            return status, json.loads(data) if data else {"raw": ""}
        except Exception:
            return status, {"raw": data}
    except Exception as e:
        conn.close()
        raise

def upload_instagram_resumable(ig_user_id: str, access_token: str, file_path: str,
                               title: str = None, description: str = None,
                               api_version: str = DEFAULT_API_VERSION,
                               wait_for_finish: bool = True, poll_interval: int = 3):
    """
    High-level wrapper to upload a local video file to Instagram via the Graph API resumable flow.
    Returns final publish response (or the rupload responses) as dicts.

    - ig_user_id: Instagram Business/Creator numeric ID (string)
    - access_token: page/app access token with publishing scopes
    - file_path: path to local video file
    - title/description: optional text for publish step
    - wait_for_finish: if True, polls container status until it's ready before publishing
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    filesize = os.path.getsize(file_path)

    # Step 1: initialize a resumable upload session
    init_url = f"{GRAPH_BASE}/{api_version}/{ig_user_id}/media"
    # Many guides show using upload_phase=start and the endpoint may be /video_reels for pages.
    init_params = {"upload_phase": "start", "access_token": access_token, "file_size": str(filesize)}
    print("Initializing upload session...")
    init_resp = _post_form(init_url, init_params)
    # init_resp should contain an upload URL and an ID (names vary by endpoint/version)
    # common keys: 'video_id', 'upload_url', 'id' or 'upload_session_id'
    # We'll try to find the upload URL and video/container id
    upload_url = init_resp.get("upload_url") or init_resp.get("upload_url_https") or init_resp.get("upload_url_raw")
    video_id = init_resp.get("video_id") or init_resp.get("id") or init_resp.get("upload_session_id")
    if not upload_url or not video_id:
        # Some endpoints return slightly different JSON — show it and abort
        raise RuntimeError(f"Could not find upload_url/video_id in init response: {json.dumps(init_resp)}")

    print("Upload URL found; uploading binary to rupload...")
    status, upload_resp = _upload_binary_to_rupload(upload_url, access_token, file_path)
    print(f"rupload response status: {status}, body: {upload_resp}")

    # If rupload returns success JSON like {"success": true} or similar, proceed to finish.
    # Step 3: finish / publish
    finish_url = f"{GRAPH_BASE}/{api_version}/{ig_user_id}/media"
    finish_params = {
        "upload_phase": "finish",
        "access_token": access_token,
        "video_id": video_id
    }
    if title:
        finish_params["title"] = title
    if description:
        finish_params["description"] = description
    print("Sending finish/publish request...")
    finish_resp = _post_form(finish_url, finish_params)
    print("Finish response:", finish_resp)

    # The video/container will often need processing. Poll status if requested.
    container_id = finish_resp.get("id") or video_id
    if wait_for_finish and container_id:
        status_field = None
        print("Polling container status until processing is FINISHED (or error)...")
        for i in range(60):  # cap the number of polls (approx 3 minutes with default interval)
            try:
                # Query status; Graph API fields might be 'status' or 'status_code'
                status_json = _get_json(f"{GRAPH_BASE}/{api_version}/{container_id}?fields=status, status_code&access_token={access_token}")
            except Exception as e:
                print("Status check error:", e)
                time.sleep(poll_interval)
                continue

            # try both fields
            s = None
            if isinstance(status_json, dict):
                if "status" in status_json and isinstance(status_json["status"], dict):
                    s = status_json["status"].get("processing_status") or status_json["status"].get("status")
                if not s:
                    s = status_json.get("status_code") or status_json.get("status")
            print(f"poll {i}: {status_json}")
            if s and (str(s).upper() in ("FINISHED", "SUCCEEDED", "AVAILABLE", "ready")):
                print("Processing finished.")
                break
            # detect an error state
            if s and (str(s).upper() in ("ERROR", "FAILED")):
                raise RuntimeError(f"Container processing error: {status_json}")
            time.sleep(poll_interval)

    # Optionally, you might want to get the permalink / media id:
    try:
        published_info = _get_json(f"{GRAPH_BASE}/{api_version}/{container_id}?fields=id,permalink&access_token={access_token}")
    except Exception:
        published_info = {"note": "could not fetch permalink; check publish status with Graph API"}

    return {
        "init_response": init_resp,
        "rupload_response": upload_resp,
        "finish_response": finish_resp,
        "published_info": published_info
    }


