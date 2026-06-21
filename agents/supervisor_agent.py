import json
from config.settings import MODELS
from agents.base_agent import BaseAgent
from agents.construction_agent import ConstructionAgent
from agents.accounting_agent import AccountingAgent
from agents.general_affairs_agent import GeneralAffairsAgent
from agents.strategy_agent import StrategyAgent
from agents.it_agent import ITAgent
from agents.care_agent import CareAgent
from agents.realestate_agent import RealEstateAgent


DEPARTMENT_MAP = {
    "建設": ConstructionAgent,
    "経理": AccountingAgent,
    "総務": GeneralAffairsAgent,
    "経営戦略": StrategyAgent,
    "IT": ITAgent,
    "介護": CareAgent,
    "不動産": RealEstateAgent,
}


class SupervisorAgent(BaseAgent):
    def __init__(self, folder_ids: dict[str, str] = {}):
        super().__init__("スーパーバイザー", "統括", "")
        self.model = MODELS["supervisor"]
        self.folder_ids = folder_ids  # {"建設": "folder_id", ...}

    def execute(self, task: str) -> str:
        # タスクをどの部署へ振り分けるか判断
        routing_prompt = f"""
以下のタスクを、該当する部署に振り分けてください。
複数の部署が必要な場合はすべてリストアップしてください。

選択肢: 建設, 経理, 総務, 経営戦略, IT, 介護, 不動産

タスク: {task}

JSON形式で回答:
{{"departments": ["部署名1", "部署名2"], "reason": "理由"}}
"""
        routing_raw = self.think(routing_prompt)
        try:
            routing = json.loads(routing_raw.strip().strip("```json").strip("```"))
        except Exception:
            routing = {"departments": list(DEPARTMENT_MAP.keys()), "reason": "解析失敗のため全部署へ"}

        self.logger.info(f"振り分け先: {routing['departments']}")

        results = []
        for dept in routing["departments"]:
            if dept not in DEPARTMENT_MAP:
                continue
            folder_id = self.folder_ids.get(dept, "")
            agent = DEPARTMENT_MAP[dept](folder_id=folder_id)
            result = agent.run(task)
            results.append(result)

        # 結果を集約
        summary_prompt = f"""
タスク: {task}

各部署エージェントの実行結果:
{json.dumps(results, ensure_ascii=False, indent=2)}

上記を統合して、簡潔な最終レポートを作成してください。
"""
        return self.think(summary_prompt)
