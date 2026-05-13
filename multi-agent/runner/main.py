import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.planner_agent import create_plan
from core.executor import execute_plan

while True:

    query = input("Ask: ")

    if query.lower() == "exit":
        break

    planner_output = create_plan(query)

    print("\nPLANNER:")
    print(planner_output)

    if planner_output["type"] == "clarification":

        print("\nCLARIFICATION:")
        print(planner_output["message"])

        continue

    if planner_output["type"] == "refusal":

        print("\nREFUSAL")
        print(planner_output["message"])

        continue

    observations = execute_plan(planner_output["tasks"])

    print("\nOBSERVATIONS:")
    print(observations)
