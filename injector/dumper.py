import dis
import marshal
import random 
import string
import os
import shutil
import inspect
import sys
import traceback

class UwUdecompiler:

    functions = []
    classes = []

    def __init__(self) -> None:
        self.all = globals().copy()
        self.create_dirs()
        self.decompile()
        
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



                        
    def get_bytecode(self, data, dir):
        try:
            bytecode = None
            name = None

            if dir == 'functions':
                bytecode = dis.Bytecode(self.all[data]) 
                with open("dump/" + dir + "/" + data + "_" + self.get_id() + ".pyc", 'wb') as file:
                    file.write(marshal.dumps(bytecode.codeobj))
                    file.close()

            elif dir == 'classes':
                if data != "UwUdecompiler":
                    class_methods = inspect.getmembers(self.all[data], predicate=inspect.isfunction)
                    for method_name, method in class_methods:
                        bytecode = dis.Bytecode(method) 

                        if not os.path.exists("dump/classes/"+data):
                            os.makedirs("dump/classes/"+data)

                        with open("dump/classes/"+data + "/" + method_name + "_" + self.get_id() + ".pyc", 'wb') as file:
                            file.write(marshal.dumps(bytecode.codeobj))
                            file.close()




        except:
            traceback.print_exc()
        
    def save_functions(self):
        self.get_functions()
        for i in self.functions:
            self.get_bytecode(i, 'functions')

    def save_classes(self):
        self.get_classes()
        for i in self.classes:
            self.get_bytecode(i, 'classes')

    def decompile(self):
        self.save_functions()
        self.save_classes()

        print("[!] DONE")

UwUdecompiler()
