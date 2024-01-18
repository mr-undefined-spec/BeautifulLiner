
from xml.dom import minidom
from layer import Layer

class Svg:
    def __init__(self):
        self.__data = []
    #end

    def read(self, file_name):
        if not type(file_name) is str:
            raise ValueError("file_name must be str")
        self.__doc = minidom.parse(file_name)
    #end

    def get_group_paths_tuple(self):
        return_tuple = []
        for group in self.__doc.getElementsByTagName("g"):
            the_tuple = []
            the_tuple.append(group)

            the_paths = []
            for path in group.getElementsByTagName("path"):
                the_paths.append(path)
            #end for
            the_tuple.append(the_paths)

            return_tuple.append(the_tuple)
        #end for
        return tuple(return_tuple)
    #end

    def viewBoxString(self):
        root = self.__doc.getElementsByTagName("svg")
        return root[0].attributes["viewBox"].value
    #end 

    @property
    def doc(self):
        return self.__doc
    #end

    def append(self, layer):
        if not isinstance(layer, Layer):
            raise TypeError("The argument of the append method must be a Layer")
        #end if
        self.__data.append(layer)
    #end def

    def __getitem__(self, i):
        return self._data[i]
    #end def

    def __iter__(self):
        self._index = 0
        return self
    #end def
    def __next__(self):
        if self._index >= len(self._data): raise StopIteration
        self._index += 1
        return self._data[self._index-1]
    #end def
#end

