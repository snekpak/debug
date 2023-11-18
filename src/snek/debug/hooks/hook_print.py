# import sys
# import ast

# DEBUG = True  # Global debug flag

# class PrintTransformer(ast.NodeTransformer):
#     def visit_Call(self, node):
#         if (isinstance(node.func, ast.Name) and node.func.id == 'print' and DEBUG):
#             node.func = ast.Name(id='custom_print', ctx=ast.Load())
#         return node

# class DebugImportHook:
#     def find_module(self, name, path):
#         return self

#     def load_module(self, name):
#         # Load source code
#         with open(name + '.py', 'r') as f:
#             source = f.read()

#         # Transform AST
#         tree = ast.parse(source)
#         tree = PrintTransformer().visit(tree)
#         ast.fix_missing_locations(tree)

#         # Compile & execute
#         code = compile(tree, filename=name + '.py', mode='exec')
#         module = sys.modules.setdefault(name, imp.new_module(name))
#         exec(code, module.__dict__)
#         return module

# # Replacing print function for demonstration purposes
# def custom_print(*args, **kwargs):
#     print("Custom:", *args, **kwargs)

# sys.meta_path.insert(0, DebugImportHook())





#-----

from os.path import (dirname, abspath, join, splitext)
from os import (listdir)
import importlib.util
import imp
import sys

_scripts_path = dirname(abspath(__file__))
_script_list = [splitext(f)[0] for f in listdir(_scripts_path) if splitext(f)[1] == '.py']

class custom_import_hook(object):
    def find_module(self, name, path):
        if name not in _script_list: return None
        return self
    
    class _cmds(object):
        @staticmethod
        def my_print(string):
            print(string)
    
    def load_module(self, name):
        sys.modules.setdefault(name, imp.new_module(name))
        spec = importlib.util.spec_from_file_location('module.name', join(_scripts_path, f'{name}.py'))
        foo = importlib.util.module_from_spec(spec)
        for cmd in self._cmds.__dict__.keys():
            if cmd[0] == '_': continue
            setattr(foo, cmd, getattr(self._cmds, cmd))
        sys.meta_path.append(self)
        spec.loader.exec_module(foo)
        sys.meta_path.remove(self)
        return foo

meta_hook = custom_import_hook()
sys.meta_path.insert(0, meta_hook)
