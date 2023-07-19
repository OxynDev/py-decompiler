import subprocess, re, os, time, glob , traceback, shutil, inspect, sys, threading, httpx
from win32com.client import GetObject
import pydumpck

pdata = r"""        if header_data[0:3] == b'MZ\x90':
            return FileType.FILE_EXE
        if header_data[0:4] == b'PYZ\x00':
            return FileType.FILE_PYZ
        if header_data[0:4] == b'\x7fELF':
            return FileType.FILE_ELF
        if header_data.find(bytes.fromhex('e3' + '0' * 14)) > -1:
            return FileType.FILE_PYC
        return FileType.FILE_UNKNOWN"""

ndata = """        return FileType.FILE_PYC"""

class Decompiler:
    def __init__(self):
        self.patch_pydumpck()
        self.start()

    def patch_pydumpck(self):
        lib_dir = pydumpck.__file__.split("\\__init__.py")[0] + "\\" + "py_common_dump\\__init__.py"
        lib_code = open(lib_dir,"r").read()
        if pdata in lib_code:
            open(lib_dir, "w").write(lib_code.replace(pdata, ndata))
            print("(LIB PATCHED) RESTART SCRIPT")
            os._exit()

    def get_process_list(self):

        res = subprocess.check_output(["injector/guidedhacking.exe", "scan"])
        pid_base_regex = re.compile(r'Base: (\S+) \| Version: \S+ \| PID: (\d+)')
        matches = pid_base_regex.findall(res.decode('utf-8'))
        result_list = [{'base': match[0], 'pid': match[1]} for match in matches]

        if len(result_list) > 0:
            return result_list
        else:
            return False

    def inject_code(self, pid: int):
        subprocess.call(f"injector/guidedhacking.exe {str(pid)} injector/dumper.py")

    def process_path(self, process_name):
        WMI = GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')      
        for p in processes :                             
            if p.Properties_("Name").Value == process_name :
                return p.Properties_[7].Value              
        return False        

    def decompile(self, dir: str):
        dirs = glob.glob(dir + "dump/*")
        for i in dirs:
            files = glob.glob(i + "\\*")
            for file in files:
                try:
                    if file.endswith(".pyc"):
                        def dec_thread(file,i):
                            o_dir = file.split(".pyc")[0] + "\\"
                            print(f" [.] Decompiling " + i.split("\\")[-1] + " " + file.split("\\")[-1])
                            subprocess.run(f"pydumpck {file} --output {o_dir} --decompile_file", capture_output = False,  text = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
                            os.remove(file)
                            decompiled_files = glob.glob(o_dir + "*")
                            for dec_file in decompiled_files:
                                if dec_file.endswith(".py"):
                                    os.replace(dec_file, file.split(".pyc")[0] + ".py")
                                    break
                            try:
                                shutil.rmtree(o_dir)
                            except:
                                pass
                            print(" [V] Done " + file.split("\\")[-1])
                        threading.Thread(target=dec_thread, args=(file,i,)).start()
                except:
                    traceback.print_exc()

            for class_object in glob.glob(i + "\\*"):
                if os.path.isdir(class_object):
                    class_tree = glob.glob(class_object + "\\*")
                    for file_method in class_tree:

                        def dec_thread(file_method,class_object):
                            try:
                                o_dir = file_method.split(".pyc")[0] + "\\"

                                if not os.path.exists(o_dir):
                                    os.makedirs(o_dir)

                                print(f" [.] Decompiling " + class_object.split("\\")[-1] + " " + file_method.split("\\")[-1])
                                subprocess.run(f"pydumpck {file_method} --output {o_dir}", 
                                            capture_output = False,  text = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL
                                            )
                                os.remove(file_method)
                                decompiled_files = glob.glob(o_dir + "*")
                                for dec_file in decompiled_files:
                                    if dec_file.endswith(".py"):
                                        os.replace(dec_file, file_method.split(".pyc")[0] + ".py")
                                        break
                                try:
                                    shutil.rmtree(o_dir)
                                except:
                                    pass
                                print(" [V] Done " + file_method.split("\\")[-1])
                            except:
                                traceback.print_exc()
                        threading.Thread(target=dec_thread, args=(file_method,class_object,)).start()
            

    def start(self):
        os.system("cls")
        discord = httpx.get("https://pastebin.com/raw/jSkxLZa3").text
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
            res = input(" [>] : ")

            try:
                int(res)
            except ValueError:
                os.system("cls")
                print("\n"," [X] Invalid selection")
                time.sleep(2)
                self.start()
            
            if (int(res) > len(process_list)) or (int(res) < 0):
                os.system("cls")
                print("\n"," [X] Invalid selection")
                time.sleep(2)
                self.start()

            self.inject_code(int(process_list[int(res)]['pid']))
            
            path = self.process_path(process_list[int(res)]['base']).split(process_list[int(res)]['base'])[0]
            os.system("cls")
            print("\n"," [.] Waiting")
            time.sleep(20)

            self.decompile(path)

Decompiler()