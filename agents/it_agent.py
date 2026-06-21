from agents.base_agent import BaseAgent
from tools.drive_tools import list_files


class ITAgent(BaseAgent):
    def __init__(self, folder_id: str = ""):
        super().__init__("ITエージェント", "ITインフラ部門", folder_id)

    def execute(self, task: str) -> str:
        files = list_files(self.folder_id) if self.folder_id else []
        file_summary = "\n".join([f"- {f['name']}" for f in files]) or "（ファイルなし）"
        prompt = f"""
## ITインフラ部門フォルダのファイル一覧
{file_summary}

## タスク
{task}
"""
        return self.think(prompt, "あなたはITインフラ部門の専門AIエージェントです。システム管理・ツール導入・AI運用保守の専門家として回答してください。")
