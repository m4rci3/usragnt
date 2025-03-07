import json
import logging

def extract_user_agents(log_file):
    user_agents = []  # empty list for storage
    try:  # just in case something fails
        with open("log_file", 'r') as file:  # opens with read permissions
            logs = json.load(file)  # allows this function to parse through if proper JSON
            for log_entry in logs:  # loop through each Zeek entry
                if 'user_agent' in log_entry:  # checks for this key
                    user_agents.append(log_entry['user_agent'])  # appends key to the empty list at the start
            logging.info("HOORAY!")  # if this dookie code works
    except Exception as e:  # error handling to show that it did not work
        logging.error(f"Error reading the log file: {e}")  # what will happen if an error occurs
    return user_agents  # if successful, returns the user_agents list
