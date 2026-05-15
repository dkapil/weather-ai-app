from tools.weather import get_weather
from tools.air_quality import get_air_quality
from tools.time import get_time

TOOLS = {
    "get_weather": get_weather,
    "get_air_quality": get_air_quality,
    "get_time": get_time,
}


def execute_plan(tasks):

    observations = []

    for task in tasks:

        tool_name = task["tool"]
        tool_input = task["input"]

        if tool_name not in TOOLS:

            observations.append(
                {"tool": tool_name, "input": tool_input, "error": "Unknown tool"}
            )

            continue

        result = TOOLS[tool_name](tool_input)

        observations.append({"tool": tool_name, "input": tool_input, "result": result})

    return observations
