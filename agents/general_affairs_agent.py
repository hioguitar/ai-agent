from agents.base_agent import BaseAgent
from tools.drive_tools import list_files


class GeneralAffairsAgent(BaseAgent):
    def __init__(self, folder_id: str = ""):
        super().__init__("総務エージェント", "総務部", folder_id)

    def execute(self, task: str) -> str:
        files = list_files(self.folder_id) if self.folder_id else []
        file_summary = "\n".join([f"- {f['name']}" for f in files]) or "（ファイルなし）"
        prompt = f"""
## 総務部フォルダのファイル一覧
{file_summary}

## タスク
{task}
"""
        return self.think(prompt, "あなたは総務部の専門AIエージェントです。人事・勤怠・文書管理・庶務の専門家として回答してください。")
