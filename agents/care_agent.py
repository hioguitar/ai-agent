from agents.base_agent import BaseAgent
from tools.drive_tools import list_files


class CareAgent(BaseAgent):
    def __init__(self, folder_id: str = ""):
        super().__init__("介護エージェント", "介護部門", folder_id)

    def execute(self, task: str) -> str:
        files = list_files(self.folder_id) if self.folder_id else []
        file_summary = "\n".join([f"- {f['name']}" for f in files]) or "（ファイルなし）"
        prompt = f"""
## 介護部門フォルダのファイル一覧
{file_summary}

## タスク
{task}
"""
        return self.think(prompt, "あなたは介護部門の専門AIエージェントです。利用者管理・シフト・介護記録の専門家として回答してください。")
