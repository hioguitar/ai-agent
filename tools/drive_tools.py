import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

from config.settings import GOOGLE_DRIVE_CREDENTIALS_PATH, GOOGLE_SCOPES

TOKEN_PATH = "./token.json"


def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, GOOGLE_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_DRIVE_CREDENTIALS_PATH, GOOGLE_SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return build("drive", "v3", credentials=creds)


def list_files(folder_id: str, max_results: int = 20) -> list[dict]:
    service = get_drive_service()
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        pageSize=max_results,
        fields="files(id, name, mimeType, modifiedTime)",
    ).execute()
    return results.get("files", [])


def read_file_content(file_id: str) -> str:
    service = get_drive_service()
    file_meta = service.files().get(fileId=file_id, fields="mimeType,name").execute()
    mime = file_meta["mimeType"]

    # Google Docs → テキスト変換
    export_types = {
        "application/vnd.google-apps.document": "text/plain",
        "application/vnd.google-apps.spreadsheet": "text/csv",
    }
    if mime in export_types:
        content = service.files().export(
            fileId=file_id, mimeType=export_types[mime]
        ).execute()
        return content.decode("utf-8") if isinstance(content, bytes) else content

    # 通常ファイル
    request = service.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return buf.getvalue().decode("utf-8", errors="ignore")


def create_text_file(name: str, content: str, parent_folder_id: str) -> str:
    service = get_drive_service()
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp_path = f.name
    meta = {"name": name, "parents": [parent_folder_id]}
    media = MediaFileUpload(tmp_path, mimetype="text/plain")
    file = service.files().create(body=meta, media_body=media, fields="id").execute()
    os.unlink(tmp_path)
    return file["id"]


def find_folder_id(folder_name: str, parent_id: str = "root") -> str | None:
    service = get_drive_service()
    results = service.files().list(
        q=f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id, name)",
    ).execute()
    files = results.get("files", [])
    return files[0]["id"] if files else None


def create_folder(folder_name: str, parent_id: str = "root") -> str:
    service = get_drive_service()
    meta = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    folder = service.files().create(body=meta, fields="id").execute()
    return folder["id"]
