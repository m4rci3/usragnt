import json
import logging

def extract_user_agent(log_file_path):
    try:
        # Open and read the file
        with open(log_file_path, "r") as file:
            log_data = json.load(file)  # Read and parse JSON

        # Extract the user-agent
        user_agent = log_data.get("user_agent", None)

        if user_agent:
            print(f"Extracted User-Agent: {user_agent}")
            return user_agent
        else:
            print("User-Agent not found in log entry.")
            return None

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    except FileNotFoundError:
        print("Error: File not found.")
        return None

# Provide the correct file path
log_file_path = input('What is the path to your log file? ')

# Call the function
user_agent = extract_user_agent(log_file_path)
print(user_agent)
