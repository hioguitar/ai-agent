import json
from pathlib import Path
from datetime import datetime
from config.settings import MODELS
from agents.base_agent import BaseAgent


class ObserverAgent(BaseAgent):
    def __init__(self):
        super().__init__("オブザーバー", "監視", "")
        self.model = MODELS["observer"]
        self.logs_dir = Path("logs")
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)

    def execute(self, task: str = "全エージェントを評価してください") -> str:
        # 全ログを読み込む
        all_logs = []
        for log_file in self.logs_dir.glob("*.log"):
            with open(log_file, encoding="utf-8") as f:
                for line in f:
                    try:
                        all_logs.append(json.loads(line))
                    except Exception:
                        pass

        if not all_logs:
            return "評価対象のログがまだありません。"

        # 統計集計
        total = len(all_logs)
        success = sum(1 for l in all_logs if l.get("status") == "success")
        errors = total - success
        agents = list({l["agent"] for l in all_logs})

        eval_prompt = f"""
あなたは第三者目線のオブザーバーエージェントです。
以下のデータを基に、全エージェントの動作を客観的に評価してください。

## 実行統計
- 総タスク数: {total}
- 成功: {success}
- エラー: {errors}
- 稼働エージェント: {', '.join(agents)}

## 直近ログ（最新10件）
{json.dumps(all_logs[-10:], ensure_ascii=False, indent=2)}

## 評価観点
1. 品質（完了率・エラー率）
2. 効果（業務改善への貢献）
3. リスク（異常・懸念事項）
4. 改善提案

簡潔にレポートしてください。
"""
        report = self.think(eval_prompt)
        self._save_report(report)
        return report

    def _save_report(self, report: str):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.reports_dir / f"observer_report_{ts}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(report)
        self.logger.info(f"レポート保存: {path}")
