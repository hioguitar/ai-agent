from agents.base_agent import BaseAgent
from tools.drive_tools import list_files


class AccountingAgent(BaseAgent):
    def __init__(self, folder_id: str = ""):
        super().__init__("経理エージェント", "経理部", folder_id)

    def execute(self, task: str) -> str:
        files = list_files(self.folder_id) if self.folder_id else []
        file_summary = "\n".join([f"- {f['name']}" for f in files]) or "（ファイルなし）"
        prompt = f"""
## 経理部フォルダのファイル一覧
{file_summary}

## タスク
{task}
"""
        return self.think(prompt, "あなたは経理部の専門AIエージェントです。請求・支払・帳票・資金繰り管理の専門家として回答してください。")
