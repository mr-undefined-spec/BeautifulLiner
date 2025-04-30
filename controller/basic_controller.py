import math

class BasicController():
    def __init__(self, mode="CUI", progress_bar=None, log_text=None):
        self.total_step_num = 0
        self.step_offset = 0

        if not mode in ["CUI", "GUI", "TEST"]:
            raise ValueError('The arg "mode" can be "CUI", "GUI" or "TEST"')
        #end
        self.mode = mode

        self.progress_bar = progress_bar
        self.log_text     = log_text
    #end

    def set_total_step_num(self, total_step_num):
        self.total_step_num = total_step_num
    #end

    def set_step_offset(self, step_offset):
        self.step_offset = step_offset
    #end

    def print_step(self, step_name, step_num):
        relative_step_num = round( 100*(step_num + 1 + self.step_offset) / self.total_step_num, 1 )
        if self.mode == "CUI" or self.mode == "TEST":
            print("{} % complete @ {}".format(relative_step_num, step_name))
        elif self.mode == "GUI":
            self.progress_bar.setValue(step_num + 1 + self.step_offset)
            self.log_text.append("{} {} / {}".format(step_name, step_num + 1 + self.step_offset, self.total_step_num))
        #end
    #end
#end
