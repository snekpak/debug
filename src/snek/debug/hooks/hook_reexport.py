import sys
import types
import importlib.abc
import importlib.machinery

##----------------------------------------------##    

print('~~Function Spy Hook~~')
#GREEN= '\033[2m'
PURPLE = '\033[95m'
GREY = '\033[90m'
ENDC = '\033[0m'  # End coloring

PREFIXES = ['driver', 'keeji', 'util']

class FunctionSpyHook(importlib.abc.MetaPathFinder):
  def __init__(self, prefixes):
    self.prefixes = prefixes
    self.function_sources = {}
    self.collisions = {}  # To store collisions

  def find_spec(self, fullname, path, target=None):
    if any(fullname.startswith(prefix) for prefix in self.prefixes):
        spec = importlib.machinery.PathFinder.find_spec(fullname, path, target)
        if spec and spec.loader:
            spec.loader.exec_module = self.exec_module_wrapper(spec.loader.exec_module)
        return spec
    return None

  def exec_module_wrapper(self, original_exec_module):
    def exec_module(module):
      original_exec_module(module)
      for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, types.FunctionType):
            if attr_name not in self.function_sources:
                self.function_sources[attr_name] = {module.__name__}
            else:
                self.function_sources[attr_name].add(module.__name__)
                _len = len(self.function_sources[attr_name])
                if _len > 1:
                  # Add to collisions instead of printing immediately
                  self.collisions[attr_name] = self.function_sources[attr_name]
    return exec_module

  def print_collisions(self):
    for func, modules in self.collisions.items():
      print(f"Collision --> {PURPLE}{func}{ENDC}:")
      for module_name in modules:
        print(f"{GREY}-- {module_name}{ENDC}")
        
  def find_collisions(self, lookup):
    if lookup in self.collisions:
      #print('looking up', lookup, self.collisions)
      val = self.collisions.get(lookup)
      #print('??',list(val))
      return val
    else:
      return None





# After all imports
hook = FunctionSpyHook(PREFIXES)
sys.meta_path.insert(0, hook)

def debug_collisions():
  hook.print_collisions()
  
def find_collisions(key):
  return hook.find_collisions(key)
#sys.meta_path.insert(0, FunctionSpyHook(PREFIXES))



