import subprocess, re, os, time, shutil, httpx
from win32com.client import GetObject

class Decompiler:
    def __init__(self):
        self.start()

    def get_process_list(self):

        res = subprocess.check_output(["injector/pyinject.exe", "scan"])
        pid_base_regex = re.compile(r'Base: (\S+) \| Version: \S+ \| PID: (\d+)')
        matches = pid_base_regex.findall(res.decode('utf-8'))
        result_list = [{'base': match[0], 'pid': match[1]} for match in matches]

        if len(result_list) > 0:
            return result_list
        else:
            return False

    def inject_disassembler_code(self, pid: int):
        subprocess.call(f"injector/pyinject.exe {str(pid)} injector/dumper.py")

    def inject_code(self, pid: int):
        subprocess.call(f"injector/pyinject.exe {str(pid)} InjCode.py")

    def process_path(self, process_name):
        WMI = GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')      
        for p in processes :                             
            if p.Properties_("Name").Value == process_name :
                return p.Properties_[7].Value              
        return False        

    def start(self):
        os.system("cls")
        try:
            discord = httpx.get("https://pastebin.com/raw/jSkxLZa3").text
        except:
            discord == "https://discord.gg/8W6BweksGY"
        os.system("cls")

        print("\n",discord, """\n\n    ____      _   _             _    
   / ___|_  _| | | | ___   ___ | | __
  | |  _\ \/ / |_| |/ _ \ / _ \| |/ /
  | |_| |>  <|  _  | (_) | (_) |   < 
   \____/_/\_\_| |_|\___/ \___/|_|\_\\
                                    """ ,"\n")

        process_list = self.get_process_list()

        if process_list == False:
            print("Python process not found")

        else:
            print(" Select target process:","\n")

            for i in range(len(process_list)):
                print(f" [{i}] " + process_list[i]['base'])

            print("\n")
            process_res = input(" [>] : ")

            try:
                int(process_res)
            except ValueError:
                os.system("cls")
                print("\n"," [X] Invalid selection")
                time.sleep(2)
                self.start()
            
            if (int(process_res) > len(process_list)) or (int(process_res) < 0):
                os.system("cls")
                print("\n"," [X] Invalid selection")
                time.sleep(2)
                self.start()

            os.system("cls")
            print("\n")
            print(" [1] decompiler \n [2] executor","\n\n")
            res = input(" [>] : ")

            try:
                int(res)
            except ValueError:
                os.system("cls")
                print("\n"," [X] Invalid selection")
                time.sleep(2)
                self.start()

            if int(res) == 1:
                path = self.process_path(process_list[int(process_res)]['base']).split(process_list[int(res)]['base'])[0]
                try:
                    shutil.copytree("unpyc", path + "\\unpyc")
                except:
                    pass
                
                self.inject_disassembler_code(int(process_list[int(res)]['pid']))
                
                os.system("cls")
                print()
                input(" [V] Decompiler injected")
                time.sleep(3)

            elif int(res) == 2:
                os.system("cls")
                while True:
                    self.inject_code(int(process_list[int(process_res)]['pid']))
                    print(" Injected")
                    input(" Press eneter to inject code.py again")
                    os.system("cls")
            else:
                os.system("cls")
                print("\n"," [X] Invalid selection")
                time.sleep(2)
                self.start()

Decompiler()