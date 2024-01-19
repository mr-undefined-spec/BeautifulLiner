
from curve_set import CurveSet
from curve_set import SegmentSet
class LayerData:
    def __init__(self, name, path):
        self.name = name
        self.path = path
    #end
#end

class Layer:
    def __init__(self):
        self.__data = []
    #end

    def __getitem__(self, i):
        return self.__data[i]
    #end def

    def __iter__(self):
        self.__index = 0
        return self
    #end def
    def __next__(self):
        if self.__index >= len(self.__data): raise StopIteration
        self.__index += 1
        return self.__data[self.__index-1]
    #end def

    def append(self, layer_name, curve_set):
        if not type(layer_name) is str:
            raise TypeError("The 1st argument \"layer_name\" of the append method must be a str")
        if not isinstance(curve_set, CurveSet):
            raise TypeError("The 2nd argument \"curve_set\" of the append method must be a CurveSet")
        #end if
        self.__data.append( LayerData(layer_name, curve_set) )
    #end def
#end

