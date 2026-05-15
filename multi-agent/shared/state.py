def create_state(query):

    return {
        "query": query,
        "tasks": [],
        "observations": [],
        "critic_feedback": None,
    }
