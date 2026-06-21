import json
import logging
from datetime import datetime
from pathlib import Path

import anthropic
from config.settings import ANTHROPIC_API_KEY, MODELS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)


class BaseAgent:
    def __init__(self, name: str, department: str, folder_id: str = ""):
        self.name = name
        self.department = department
        self.folder_id = folder_id
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = MODELS["department"]
        self.logger = logging.getLogger(name)
        self._log_path = Path("logs") / f"{department}.log"
        self._log_path.parent.mkdir(exist_ok=True)

    def think(self, prompt: str, system: str = "") -> str:
        if not system:
            system = f"あなたは{self.department}の専門AIエージェントです。簡潔・正確に回答してください。"
        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    def run(self, task: str) -> dict:
        self.logger.info(f"タスク開始: {task[:50]}")
        try:
            result = self.execute(task)
            self._write_log(task, result, "success")
            return {"status": "success", "agent": self.name, "result": result}
        except Exception as e:
            self.logger.error(f"エラー: {e}")
            self._write_log(task, str(e), "error")
            return {"status": "error", "agent": self.name, "error": str(e)}

    def execute(self, task: str) -> str:
        raise NotImplementedError("サブクラスで実装してください")

    def _write_log(self, task: str, result: str, status: str):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "task": task,
            "status": status,
            "result": result[:500],
        }
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
