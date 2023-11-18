import sys
print('~~Meta Path Hook~~')


class MetaPathList(list):
    def insert(self, index, object):
        print(f"New hook: {object}")
        super().insert(index, object)

    def append(self, object):
        print(f"New hook: {object}")
        super().append(object)

sys.meta_path = MetaPathList(sys.meta_path)


