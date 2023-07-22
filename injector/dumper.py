import random 
import string
import os
import shutil
import inspect
import sys
import importlib.util
import pathlib
import traceback
import threading

class UwUdecompiler:

    functions = []
    classes = []
    unpyc3 = None

    def __init__(self) -> None:
        print(" [V] Decompiler Injected")
        self.all = globals().copy()
        self.load_unpyc()
        self.create_dirs()
        self.decompile()
    

    def load_unpyc(self):
        try:
            path = str(pathlib.Path().resolve())
            dis_path = f"{path}\\unpyc\\unpyc\\unpyc3.py"
            spec = importlib.util.spec_from_file_location("unpyc3", dis_path)
            self.unpyc3 = importlib.util.module_from_spec(spec)
            sys.modules["unpyc3"] = self.unpyc3
            spec.loader.exec_module(self.unpyc3)
        except:
            print("Cant load unpyc3 module")


    def create_dirs(self):
        try:
            shutil.rmtree("dump")
        except:
            pass

        dirs = ('functions','classes')

        if not os.path.exists("dump"):
            os.makedirs("dump")

        for i in dirs:
            if not os.path.exists("dump/" + i):
                os.makedirs("dump/" + i)

    def get_id(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(3))
        
    def get_functions(self):


        is_function_member = lambda member: inspect.isfunction(member) and member.__module__ == __name__
        functionmember = inspect.getmembers(sys.modules[__name__], is_function_member)

        for i in functionmember:
            self.functions.append(i[0])

    def get_classes(self):

        is_class_member = lambda member: inspect.isclass(member) and member.__module__ == __name__
        clsmembers = inspect.getmembers(sys.modules[__name__], is_class_member)

        for i in clsmembers:
            self.classes.append(i[0])



                        
    def get_code(self, data, dir):
        print("X")
        try:

            if dir == 'functions':
                code = self.unpyc3.decompile(self.all[data])
                print(code)
                with open("dump/" + dir + "/" + data + "_" + self.get_id() + ".py", 'w') as file:
                    file.write(str(code))
                    file.close()
                
            elif dir == 'classes':
                if data != "UwUdecompiler":
                    class_methods = inspect.getmembers(self.all[data], predicate=inspect.isfunction)
                    for method_name, method in class_methods:
                        code = self.unpyc3.decompile(method)
                        print(code)
                        if not os.path.exists("dump/classes/"+data):
                            os.makedirs("dump/classes/"+data)

                        with open("dump/classes/"+data + "/" + method_name + "_" + self.get_id() + ".py", 'w') as file:
                            file.write(str(code))
                            file.close()

        except:
            traceback.print_exc()
        
    def save_functions(self):
        self.get_functions()
        print(self.functions)
        for i in self.functions:
            threading.Thread(target=self.get_code, args=(i, 'functions',)).start()

    def save_classes(self):
        self.get_classes()
        print(self.classes)
        for i in self.classes:
            threading.Thread(target=self.get_code, args=(i, 'classes',)).start()

    def decompile(self):
        self.save_functions()
        self.save_classes()

        print("[!] DONE")

UwUdecompiler()
