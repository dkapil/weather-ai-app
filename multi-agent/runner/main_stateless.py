import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.planner_agent import create_plan
from agents.critic_agent import review
from core.executor import execute_plan


def printj(data):
    print(json.dumps(data, indent=2))


while True:

    query = input("Ask: ")

    if query.lower() == "exit":
        break

    planner_output = create_plan(query)

    print("\nPLANNER:")
    printj(planner_output)

    if planner_output["type"] == "clarification":

        print("\nCLARIFICATION:")
        printj(planner_output["message"])

        continue

    if planner_output["type"] == "refusal":

        print("\nREFUSAL")
        printj(planner_output["message"])

        continue

    observations = execute_plan(planner_output["tasks"])

    print("\nOBSERVATIONS:")
    printj(observations)

    critic_output = review(query, observations)

    print("\nCRITIC:")
    printj(critic_output)

    if critic_output["status"] == "complete":

        print("\nFINAL ANSWER:")
        print(critic_output["answer"])

    else:

        print("\nINCOMPLETE:")
        print(critic_output["reason"])
