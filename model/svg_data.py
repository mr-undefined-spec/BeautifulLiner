
from xml.dom import minidom

class SvgData:
    def __init__(self, file_name):
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
#end

