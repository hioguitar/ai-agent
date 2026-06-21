from agents.base_agent import BaseAgent
from tools.drive_tools import list_files


class StrategyAgent(BaseAgent):
    def __init__(self, folder_id: str = ""):
        super().__init__("戦略エージェント", "経営戦略部門", folder_id)

    def execute(self, task: str) -> str:
        files = list_files(self.folder_id) if self.folder_id else []
        file_summary = "\n".join([f"- {f['name']}" for f in files]) or "（ファイルなし）"
        prompt = f"""
## 経営戦略部門フォルダのファイル一覧
{file_summary}

## タスク
{task}
"""
        return self.think(prompt, "あなたは経営戦略部門の専門AIエージェントです。KPI管理・戦略立案・経営分析の専門家として回答してください。")
