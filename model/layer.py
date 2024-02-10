
import copy

from point import Point
from control_point import LinearApproximateCurveControlPoint

from curve import Curve
import tkinter as tk

class Layer:
    def __init__(self):
        self.__curve_set = []
        self.is_fill = False
        self.color   = "#000000"
    #end

    def __getitem__(self, i):
        return self.__curve_set[i]
    #end

    def __iter__(self):
        self.__index = 0
        return self
    #end
    def __next__(self):
        if self.__index >= len(self.__curve_set): raise StopIteration
        self.__index += 1
        return self.__curve_set[self.__index-1]
    #end

    def append(self, curve):
        if not isinstance(curve, Curve):
            raise TypeError("The argument of the append method must be a Curve(CubicBezierCurve or LinearApproximateCurve)")
        #end if
        self.__curve_set.append(curve)
    #end

    def set_write_options(self, is_fill, color):
        self.is_fill = is_fill
        self.color   = color
    #end

    def to_svg(self):
        s = ''
        for curve in self.__curve_set:
            s += '<path d="'
            s += curve.to_svg()
            if self.is_fill:
                s += '" fill="' + self.color + '" opacity="1" stroke="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" />\n'
            else:
                s += '" fill="none" opacity="1" stroke="' + self.color + '" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" />\n'
        #end
        return s
    #end

    def linearize(self, micro_segment_length, global_calc_step, mode, progress_bar=None, log_text=None):
        linear_approximate_layer = Layer()

        curve_num = len(self.__curve_set)
        for i, curve in enumerate(self.__curve_set):
            if mode == "CUI":
                print("linearize {} / {}".format(i + curve_num*global_calc_step, curve_num*6))
            elif mode == "GUI":
                progress_bar.configure(  value=int( 100*(i + curve_num*global_calc_step)/curve_num/6.0 )  )
                progress_bar.update()
                log_text.insert( tk.END, "linearize {} / {}\n".format(i + curve_num*global_calc_step, curve_num*6) )
                log_text.see(tk.END)
                log_text.update()
            #end
            linear_approximate_curve = curve.linearize(micro_segment_length)

            # If the target curve is too whort and the linearize results are less than 4 points,
            # smoothen method will not work.
            # So ignore the target curve
            if len(linear_approximate_curve) > 4:
                linear_approximate_layer.append( linear_approximate_curve )
            #end
        #end
        return linear_approximate_layer
    #end

    def smoothen(self, global_calc_step, mode, progress_bar=None, log_text=None):
        new_layer = Layer()
        curve_num = len(self.__curve_set)
        for i, curve in enumerate(self.__curve_set):
            if mode == "CUI":
                print("smoothen {} / {}".format(i + curve_num*global_calc_step, curve_num*6))
            elif mode == "GUI":
                progress_bar.configure(  value=int( 100*(i + curve_num*global_calc_step)/curve_num/6.0 )  )
                progress_bar.update()
                log_text.insert( tk.END, "smoothen {} / {}\n".format(i + curve_num*global_calc_step, curve_num*6) )
                log_text.see(tk.END)
                log_text.update()
            #end
            new_layer.append( curve.smoothen() )
        #end
        return new_layer
    #end

    def __get_edge_deleted_curve(self, target_curve, ratio):
        new_curve = copy.deepcopy(target_curve)

        intersected_curve_set = []
        for curve in self.__curve_set:
            if curve == target_curve:
                continue
            #end
            if target_curve.rect.test_collision(curve.rect):
                intersected_curve_set.append(curve)
            #end
        #end

        inter_num = len(intersected_curve_set)

        for i, intersected_curve in enumerate(intersected_curve_set):
            new_curve.update_start_end_index_with_intersection(intersected_curve, ratio)
        #end

        return new_curve
    #end

    def delete_edge(self, bbox, ratio, global_calc_step, mode, progress_bar=None, log_text=None):
        new_layer = Layer()
        for i, curve in enumerate(self.__curve_set):
            if mode == "CUI":
                print("prepare delete edge {}".format(i))
            elif mode == "GUI":
                log_text.insert( tk.END, "prepare delete edge {}\n".format(i) )
                log_text.see(tk.END)
                log_text.update()
            #end
            curve.create_intersect_judge_rectangle()
            curve.create_qtree_ctrl_p_set(bbox)
        #end
        curve_num = len(self.__curve_set)
        for i, curve in enumerate(self.__curve_set):
            if mode == "CUI":
                print("delete edge {} / {}".format(i + curve_num*global_calc_step, curve_num*6))
            elif mode == "GUI":
                progress_bar.configure(  value=int( 100*(i + curve_num*global_calc_step)/curve_num/6.0 )  )
                progress_bar.update()
                log_text.insert( tk.END, "delete edge {} / {}\n".format(i + curve_num*global_calc_step, curve_num*6) )
                log_text.see(tk.END)
                log_text.update()
            #end
            new_layer.append( self.__get_edge_deleted_curve(curve, ratio) )
        #end
        return new_layer
    #end

    def broaden(self, broaden_width, global_calc_step, mode, progress_bar=None, log_text=None):
        new_layer = Layer()
        curve_num = len(self.__curve_set)
        for i, curve in enumerate(self.__curve_set):
            if mode == "CUI":
                print("broaden {} / {}".format(i + curve_num*global_calc_step, curve_num*6))
            elif mode == "GUI":
                progress_bar.configure(  value=int( 100*(i + curve_num*global_calc_step)/curve_num/6.0 )  )
                progress_bar.update()
                log_text.insert( tk.END, "broaden {} / {}\n".format(i + curve_num*global_calc_step, curve_num*6) )
                log_text.see(tk.END)
                log_text.update()
            #end
            new_layer.append( curve.broaden(broaden_width) )
        #end
        return new_layer
    #end
#end

