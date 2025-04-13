#import numpy as np

#import os
#import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '../primitive'))

class Curve:
    def __init__(self):
        self._going_ctrl_p_list = []
        self.__intersect_judge_rectangular = None

        self._start_index = 0
        self._end_index   = -1
    #end

    @property
    def going_ctrl_p_list(self):
        return self._going_ctrl_p_list
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

    def update_start_index(self, start_index):
        if( self._start_index < start_index ):
            self._start_index = start_index
        #end
    #end

    def update_end_index(self, end_index):
        if( self._end_index == -1):
            self._end_index = end_index
        elif( end_index < self._end_index ):
            self._end_index = end_index
        #end
    #end

    def _get_the_end(self):
        # if self._end_index is initial state, then ...
        if (self._end_index == -1):
            return len(self._going_ctrl_p_list) 
        #end
        # if self._end_index is over the array size
        if ( self._end_index >= len(self._going_ctrl_p_list) ):
            return len(self._going_ctrl_p_list)
        #end
        # others, self._end_index is correct
        return self._end_index
    #end

    @property
    def start_index(self):
        return self._start_index
    #end
    @property
    def end_index(self):
        return self._end_index
    #end

    def get_points(self):
        points = []
        points.append(self._going_ctrl_p_list[self._start_index].start)

        the_end = self._get_the_end()
        for i in range( self._start_index, the_end ):
            points.append(self._going_ctrl_p_list[i].end)
        #end
        return points
    #end

    def to_str(self):
        s = ""
        for i, ctrl_p in enumerate(self._going_ctrl_p_list):
            s += ctrl_p.to_str(i==0)
        #end
        return s
    #end
#end
