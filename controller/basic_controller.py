from argparse import ArgumentParser

import os
import sys

class BasicController():
    def initialize(self):
        self.total_step_num = 0
        self.step_offset = 0
    #end

    def set_total_step_num(self, total_step_num):
        self.total_step_num = total_step_num
    #end

    def set_step_offset(self, step_offset):
        self.step_offset = step_offset
    #end

    def print_step(self, step_name, step_num):
        print("{} {} / {}".format(step_name, step_num + 1 + self.step_offset, self.total_step_num))
    #end
#end
