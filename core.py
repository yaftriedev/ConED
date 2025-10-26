import subprocess

class ListActions:
    def __init__(self, ip, port, time_out_resp, path_file_killer, save_logs, local_debug):
        self.actions = []
        self.ip = ip
        self.port = port
        self.time_out_resp = time_out_resp
        self.path_file_killer = path_file_killer
        self.save_logs = save_logs
        self.local_debug = local_debug
    
    def info(self):
        print(f"IP: {self.ip} | PORT: {self.port} | TIME OUT RESPONSE: {self.time_out_resp} | PATH KILLER: {self.path_file_killer} | SAVE LOGS: {self.save_logs} | LOCAL DEBUG: {self.local_debug}")
        print("\nSelect a Option")
        print("    exit, info, clear")
        for i, command in enumerate(self.actions):
            print(f"    {i}. {command[0]}")
        print()
    
    def get_list_actions(self):
        return self.actions
    
    def exec_cmd(self, cmd, shell=True, capture_output=True, text=True):
        r = subprocess.run(cmd, shell=shell, capture_output=capture_output, text=text)
        print(f"Command: {r.args}\nReturn Code: {r.returncode}\n\n{r.stdout}")
        if r.stderr != "":
            print(f"Error: {r.stderr}")

    def precmd(self, predefined_commands, msg="Select Predefined Command: "):
        print(f"\n{msg}")
        for i, command in enumerate(predefined_commands):
            print(f"    {i}. {command[0]}")
        
        index = input("\nSelect a Predefined Command Index: ")
        
        if index.isdigit() and 0 <= int(index) < len(predefined_commands):
            self.exec_remote_cmd(predefined_commands[int(index)][1]())
        else:
            print(f"Error: {index} is not a valid option")