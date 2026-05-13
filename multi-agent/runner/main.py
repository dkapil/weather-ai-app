import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.planner_agent import create_plan

while True:

    query = input("Ask: ")

    if query.lower() == "exit":
        break

    result = create_plan(query)

    print(result)
