from agents.base_agent import BaseAgent
from tools.drive_tools import list_files


class RealEstateAgent(BaseAgent):
    def __init__(self, folder_id: str = ""):
        super().__init__("不動産エージェント", "不動産部門", folder_id)

    def execute(self, task: str) -> str:
        files = list_files(self.folder_id) if self.folder_id else []
        file_summary = "\n".join([f"- {f['name']}" for f in files]) or "（ファイルなし）"
        prompt = f"""
## 不動産部門フォルダのファイル一覧
{file_summary}

## タスク
{task}
"""
        return self.think(prompt, "あなたは不動産部門の専門AIエージェントです。物件管理・契約・入居者対応の専門家として回答してください。")
