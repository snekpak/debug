import sys

##----------------------------------------------##    

print('~~Spy Hook~~')

PREFIXES = ['driver', 'keeji', 'util']

#GREEN= '\033[2m'
PURPLE = '\033[95m'
GREY = '\033[90m'
ENDC = '\033[0m'  # End coloring

class SpyImporter:
  
    loaded_modules = set()
    last=''

    def find_spec(self, fullname, path, target=None):
      
      if fullname not in self.loaded_modules:
        seen="new"
        self.loaded_modules.add(fullname)
      else:
        seen="cached"
        
      if any(fullname.startswith(prefix) for prefix in PREFIXES):
        color = PURPLE
        message = f"{color}Import -> {fullname} {ENDC}"
      else:
        color = GREY
        message = f"{color}Import attempted from other package: {fullname} {seen} {ENDC}"
        
      if color == PURPLE:
        print(message)
        
      return None
        
            


sys.meta_path.insert(0, SpyImporter())



