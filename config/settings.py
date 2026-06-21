import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_DRIVE_CREDENTIALS_PATH = os.getenv("GOOGLE_DRIVE_CREDENTIALS_PATH", "./credentials.json")

# 用途別モデル設定
MODELS = {
    "supervisor": "claude-sonnet-4-6",   # 統括・判断
    "observer":   "claude-sonnet-4-6",   # 監視・評価
    "department": "claude-haiku-4-5-20251001",  # 各部署（コスト重視）
}

GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/drive",
]
