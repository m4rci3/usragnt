import json # JSON strings to dicts 
import logging 
import sys 
import requests

# file handler, (logs only ERROR and above) 
file_handler = logging.FileHandler("errorchecking.log")
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

#stream handler (console, logs, INFO and above)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_formatter = logging.Formatter('%(asctime)s - %(message)s')
stream_handler.setFormatter(stream_formatter)

#Config the root logger to use both handlers with a min log level of DEBUG  
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler])

def extract_user_agents(log_file_path): # Extracts and collects the "user_agent" field from each valid JSON line 
    user_agents = []
    try:
        with open(log_file_path, "r") as file:
            for line in file:
                try:
                    log_entry = json.loads(line) # Parse the line as JSON
                    user_agent = log_entry.get("user_agent") #get user_agent , return None if not found 
                    if user_agent:
                        user_agents.append(user_agent)
                except json.JSONDecodeError as e:
                    logging.warning(f"Skipping invalid JSON line {e}")
        if not user_agents:
            logging.info("No User-Agent fields found in the log file.")
            return []
        return user_agents
    except FileNotFoundError:
        logging.info(f"Log file {log_file_path} not found. Please check the path and try again")
        return None


def analyze_user_agent(user_agent): # sends the found user_agent string to an API , it analyzes then returns the info 
    api_url = f"https://useragentstring.com/?uas={user_agent}&getJSON=all"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            result = response.json() # parse JSON response to dict 
            return result
        else:
            logging.error(f"API request failed with status code: {response.status_code}")
            return None

    except requests.RequestException as e:
                logging.error(f"Error connecting to API: {e}")
                return None


def display_results(user_agent, analysis): # Takes dict values from the analyze function and sets them to a variable  
    if not analysis: # 
        logging.warning(f"Could not analyze user-agent: {user_agent}")
        return
    browser = analysis.get("agent_name", "Unknown") #get on the analysis dict to get specific info 
    version = analysis.get("agent_version", "Unknown")
    os_name = analysis.get("os_name", "Unknown")
    os_version = analysis.get("os_versionNumber", "Unknown")
    
    return browser, version, os_name, os_version

def main():
    if len(sys.argv) != 2:
        logging.error(f"Invalid number of arguments: Expected 1, got {len(sys.argv) - 1}")
        sys.exit()
    log_file_path = sys.argv[1]
    user_agents = extract_user_agents(log_file_path)

    if not user_agents:
        return

    if len(user_agents) > 2:
        while True:
            answer = input(
                f"Found {len(user_agents)} user-agents. Analyze all? (y/n, default=n, default= 2 user_agents): ")
            if answer.lower() == "n" or answer == "":
                user_agents = user_agents[:2]
                break
            elif answer.lower() == "y":
                break
            else:
                logging.info("Invalid input. Exiting.")
                sys.exit()

    for user_agent in user_agents:
        result = analyze_user_agent(user_agent)
        output = display_results(user_agent, result)
        if output: # if any output at all, check here to not result in a crash if result is returned as None 
            browser, version, os_name, os_version = output
            logging.info(f"Browser: {browser} {version}")
            logging.info(f"OS: {os_name} {os_version}")


if __name__ == "__main__":
    main()
