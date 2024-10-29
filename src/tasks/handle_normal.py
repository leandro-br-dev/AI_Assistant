# Path: src/tasks/handle_normal.py

description = "Responds normally to user queries."
trigger = "If it was a regular question, use this task."
example = "{'type': 'handle_normal', 'content': 'Provide a standard response to the user.'}"

def execute(content):
    """Execute the normal response task."""
    print(f"Handling normal task: {content}")
    return content