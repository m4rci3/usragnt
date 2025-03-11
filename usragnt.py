import json

def extract_user_agents(log_file_path):
    user_agents = []

    try:
        with open(log_file_path, "r") as file:
            for line in file:
                try:
                    log_entry = json.loads(line)  # Parse each line as a JSON object
                    user_agent = log_entry.get("user_agent")
                    if user_agent:
                        print(f"Extracted User-Agent: {user_agent}")
                        user_agents.append(user_agent)
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON line: {e}")

        if not user_agents:
            print("No User-Agent fields found in the log file.")
            return None

        return user_agents

    except FileNotFoundError:
        print("Error: File not found.")
        return None

# Provide the correct file path
log_file_path = input('What is the path to your log file? ')

# Call the function
user_agents = extract_user_agents(log_file_path)
print(user_agents)

