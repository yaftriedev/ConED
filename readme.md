# ConED

## Config Vars
Go to coned.py file ans change vars.
(ip, port, time_out_resp, path_file_killer, save_logs, local_debug)

## Create a new profile
```
import core, subprocess, os

class NameProfile(core.ListActions):
    def __init__(self, ip, port, time_out_resp, path_file_killer, save_logs, local_debug):
        super().__init__(ip, port, time_out_resp, path_file_killer, save_logs, local_debug)

        self.actions = []

```
You can use functions: 
+ info(), 
+ get_list_actions(), 
+ exec_cmd(cmd, shell=True, capture_output=True, text=True)
+ precmd(predefined_commands, msg="Select Predefined Command: ")

Include in the ConED File: profile_list_actions = YourProfileClass(vars)