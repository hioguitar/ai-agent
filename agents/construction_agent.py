from agents.base_agent import BaseAgent
from tools.drive_tools import list_files, read_file_content


class ConstructionAgent(BaseAgent):
    def __init__(self, folder_id: str = ""):
        super().__init__("建設エージェント", "建設部門", folder_id)

    def execute(self, task: str) -> str:
        files = list_files(self.folder_id) if self.folder_id else []
        file_summary = "\n".join([f"- {f['name']}" for f in files]) or "（ファイルなし）"
        prompt = f"""
## 建設部門フォルダのファイル一覧
{file_summary}

## タスク
{task}
"""
        return self.think(prompt, "あなたは建設部門の専門AIエージェントです。工事管理・施工スケジュール・協力会社管理の専門家として回答してください。")
