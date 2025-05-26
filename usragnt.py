import json
import logging
import requests
import sys

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename ='zeek_useragent.log')

def extract_user_agents(log_file_path):
    user_agents = []
    try:
        with open(log_file_path, "r") as file:
            for line in file:
                try: 
                    log_entry = json.loads(line)  
                    user_agent = log_entry.get("user_agent")
                    if user_agent:
                        user_agents.append(user_agent)
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON line: {e}")
        if not user_agents:
            print("No User-Agent fields found in the log file.")
            return []
        return user_agents
    except FileNotFoundError:
        print("Error: File not found.")
        return None

def analyze_user_agent(user_agent):
    api_url = f"https://useragentstring.com/?uas={user_agent}&getJSON=all"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"API request failed with status code: {response.status_code}")
            return None
        
    except requests.RequestException as e:
        print(f"Error connecting to API: {e}")
        return None

def display_results(user_agent, analysis):
    if not analysis:
        print(f"\nCould not analyze: {user_agent}\n")
        return
    browser = analysis.get("agent_name","Unknown")
    version = analysis.get("agent_version","Unknown")
    os_name = analysis.get("os_name","Unknown")
    os_version = analysis.get("os_versionNumber","Unknown")

    print(f"Browser: {browser} {version}")
    print(f"OS: {os_name} {os_version}")

def main():
    if len(sys.argv) != 2:
        print(f"ERROR: 1 argument expected, {len(sys.argv) - 1} given ")
        sys.exit()
    log_file_path = sys.argv[1]
    user_agents = extract_user_agents(log_file_path)

    if not user_agents:
        print("No user-agent found. Exiting.")
        return

    if len(user_agents) > 2:
        while True:
            answer = input(f"Found {len(user_agents)} user-agents. Analyze all? (y/n, default=n, default= 2 user_agents): ")
            if answer.lower() == "n" or answer == "":
                user_agents = user_agents[:2]
                break
            elif answer.lower() == "y":
                break
            else:
                print("Invalid input. Exiting.")
                sys.exit()

    for user_agent in user_agents:
        result = analyze_user_agent(user_agent)
        display_results(user_agent, result)

if __name__ == "__main__":
    main()

