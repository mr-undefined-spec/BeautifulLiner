#import numpy as np

#import os
#import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '../primitive'))

class Curve:
    def __init__(self):
        self._going_ctrl_p_list = []
        self.__intersect_judge_rectangular = None
    #end

    def __getitem__(self, i):
        return self._going_ctrl_p_list[i]
    #end

    def __iter__(self):
        self._index = 0
        return self
    #end
    def __next__(self):
        if self._index >= len(self._going_ctrl_p_list): raise StopIteration
        self._index += 1
        return self._going_ctrl_p_list[self._index-1]
    #end

    def __len__(self):
        return len(self._going_ctrl_p_list)
    #end

    @property
    def going_ctlr_p_list(self):
        return self._going_ctrl_p_list
    #end

    def to_str(self):
        s = ""
        for i, ctrl_p in enumerate(self._going_ctrl_p_list):
            s += ctrl_p.to_str(i==0)
        #end
        return s
    #end
#end
