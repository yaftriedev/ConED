# ConED
# Author: *****
# Version: 1.0
# OS: Linux/Bash

import subprocess, os, sys, core
from linux_nc import NCListActions

# Get Variables and Initialize List Actions
profile_list_actions = NCListActions(
    "172.24.206.62", # IP
    "4444", # Port
    "2", # Time Out Response
    "/tmp/er", # Path File Killer
    False, # Save Logs
    False # Local Debug
)

# Main Info
boolApp = True
subprocess.run("clear", shell=True)
print("Welcome to ConED")
profile_list_actions.info()

# Main Program Loop
while boolApp:
    option = input(">> ")

    if option == "":
        pass
    
    elif option.lower() == "exit":
        boolApp = False
    
    elif option.lower() == "info":
        profile_list_actions.info()
    
    elif option.lower() == "clear":
        subprocess.run("clear", shell=True)
    
    elif option.isdigit() and 0 <= int(option) < len(profile_list_actions.get_list_actions()):
        _action = profile_list_actions.get_list_actions()[int(option)]
        if callable(_action[1]):
            _action[1]()
        else:
            print(f"Error: Action for {_action[0]} is not callable")
    
    else:
        print(f"Error {option} isn't a correct option")