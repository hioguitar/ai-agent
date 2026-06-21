"""
使い方:
  python main.py supervisor "今月の工事案件の進捗をまとめて"
  python main.py observer
  python main.py dept 建設 "協力会社リストを整理して"
"""
import sys
from agents.supervisor_agent import SupervisorAgent
from agents.observer_agent import ObserverAgent
from agents.construction_agent import ConstructionAgent
from agents.accounting_agent import AccountingAgent
from agents.general_affairs_agent import GeneralAffairsAgent
from agents.strategy_agent import StrategyAgent
from agents.it_agent import ITAgent
from agents.care_agent import CareAgent
from agents.realestate_agent import RealEstateAgent

DEPT_AGENTS = {
    "建設": ConstructionAgent,
    "経理": AccountingAgent,
    "総務": GeneralAffairsAgent,
    "経営戦略": StrategyAgent,
    "IT": ITAgent,
    "介護": CareAgent,
    "不動産": RealEstateAgent,
}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    mode = sys.argv[1]

    if mode == "supervisor":
        task = " ".join(sys.argv[2:]) or "全部署の状況を報告してください"
        agent = SupervisorAgent()
        result = agent.run(task)
        print(result["result"] if result["status"] == "success" else result["error"])

    elif mode == "observer":
        agent = ObserverAgent()
        result = agent.run()
        print(result["result"] if result["status"] == "success" else result["error"])

    elif mode == "dept":
        dept = sys.argv[2] if len(sys.argv) > 2 else ""
        task = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else "状況を報告してください"
        if dept not in DEPT_AGENTS:
            print(f"部署名が不正です。選択肢: {list(DEPT_AGENTS.keys())}")
            return
        agent = DEPT_AGENTS[dept]()
        result = agent.run(task)
        print(result["result"] if result["status"] == "success" else result["error"])

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
