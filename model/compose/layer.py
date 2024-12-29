
import copy

from point import Point

from curve import Curve
import tkinter as tk

from enum import Enum

class EndpointStyle(Enum):
    BOTH_POINTED = "both_pointed"
    BOTH_WIDE = "both_wide"
#end

class Layer:
    def __init__(self, name):
        if not type(name) is str:
            raise TypeError("The 1st argument \"layer_name\" of the append method must be a str")
        #end
        self.__name = name

        self.__curve_set = []

        self.is_fill = False
        self.color   = "#000000"
        self.endpoint_style   = EndpointStyle.BOTH_POINTED

        self.continuous_curve_index_group = None
    #end

    @property
    def name(self):
        return self.__name
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

    def set_write_options(self, is_fill, color, endpoint_style):
        self.is_fill = is_fill
        self.color   = color

        if not isinstance(endpoint_style, EndpointStyle):
            raise TypeError("The argument \"endpoint_style\" of the set_write_options method must be an EndpointStyle")
        #end
        self.endpoint_style   = endpoint_style
    #end

    def __print_step(self, mode, global_calc_step, local_calc_step, step_name, progress_bar, log_text):
        curve_num = len(self.__curve_set)
        total_step_num = 7*curve_num
        __gl_step = global_calc_step - 1
        if mode == "CUI":
            print("{} {} / {}".format(step_name, local_calc_step + curve_num*__gl_step + 1, total_step_num))
        elif mode == "GUI":
            progress_bar.configure(  value=int( 100*(local_calc_step + curve_num*__gl_step)/total_step_num )  )
            progress_bar.update()
            log_text.insert( tk.END, "{} {} / {}\n".format(step_name, local_calc_step + curve_num*__gl_step + 1, total_step_num) )
            log_text.see(tk.END)
            log_text.update()
        #end
    #end

    def linearize(self, micro_segment_length, global_calc_step, mode, progress_bar=None, log_text=None):
        linear_approximate_layer = Layer(self.name + "L")

        step_name = ""
        if global_calc_step == 0:
            step_name = "linearize 1st"
        else:
            step_name = "linearize 2nd"
        #end
        for i, curve in enumerate(self.__curve_set):
            self.__print_step(mode, global_calc_step, i, step_name, progress_bar, log_text)
            linear_approximate_curve = curve.linearize(micro_segment_length)

            # If the target curve is too short and the linearize results are less than 4 points,
            # smoothen method will not work.
            # So ignore the target curve
            if len(linear_approximate_curve) > 4:
                linear_approximate_layer.append( linear_approximate_curve )
            #end
        #end
        return linear_approximate_layer
    #end

    def thin_smoothen(self, global_calc_step, mode, progress_bar=None, log_text=None):
        new_layer = Layer(self.name + "S")

        step_name = ""
        if global_calc_step == 1:
            step_name = "thin smoothen 1st"
        else:
            step_name = "thin smoothen 2nd"
        #end
        for i, curve in enumerate(self.__curve_set):
            self.__print_step(mode, global_calc_step, i, step_name, progress_bar, log_text)
            new_layer.append( curve.thin_smoothen() )
        #end
        return new_layer
    #end

    """
    def special_smoothen_for_hair(self, global_calc_step, mode, progress_bar=None, log_text=None):
        new_layer = Layer(self.name + "H")

        step_name = ""
        if global_calc_step == 1:
            step_name = "smoothen 1st"
        else:
            step_name = "smoothen 2nd"
        #end
        for i, curve in enumerate(self.__curve_set):
            self.__print_step(mode, global_calc_step, i, step_name, progress_bar, log_text)
            new_layer.append( curve.special_smoothen_for_hair() )
        #end
        return new_layer
    #end
    """

    def create_intersect_judge_rectangle(self, bbox):
        for i, curve in enumerate(self.__curve_set):
            curve.create_intersect_judge_rectangle()
            curve.create_qtree_ctrl_p_set(bbox)
        #end
    #end

    def create_sequential_points(self):
        for i, curve in enumerate(self.__curve_set):
            curve.create_sequential_points()
        #end
    #end

    def __get_curve_connection_info(self, target_curve_index, target_curve, distance_threshold):
        candidate_curve_index_set = []
        total_curve_num = len(self.__curve_set)
        for i in range(total_curve_num):
            if i == target_curve_index:
                continue
            #end
            curve = self.__curve_set[i]
            if target_curve.rect.test_collision(curve.rect):
                candidate_curve_index_set.append(i)
            #end
        #end

        #print(candidate_curve_index_set)

        ret_info = {"start": None, "end": None}

        #print("target", target_curve_index)

        for candidate_curve_index in candidate_curve_index_set:
            #print("candidate", candidate_curve_index)
            candidate_curve = self.__curve_set[candidate_curve_index]
            if target_curve.is_continuaous_at_start_side(candidate_curve, distance_threshold):
                ret_info["start"] = candidate_curve_index
            #end
            if target_curve.is_continuaous_at_end_side(candidate_curve, distance_threshold):
                ret_info["end"] = candidate_curve_index
            #end
        #end

        #print("\n")

        #print(self.curve_connection_info)
        return ret_info

    #end

    def create_continuous_curve_index_group(self, distance_threshold):
        
        curve_connection_info = []

        for i, curve in enumerate(self.__curve_set):
            curve_connection_info.append( self.__get_curve_connection_info(i, curve, distance_threshold) )
        #end

        # make a list of start:"None"
        start_none_list = []
        for i, info in enumerate(curve_connection_info):
            if info["start"] is None:
                start_none_list.append(i)
            #end
        #end
        #print(start_none_list)

        self.continuous_curve_index_group = []

        for i in start_none_list:
            tmp_index_group = []
            tmp_index_group.append(i)
            c_info = curve_connection_info[i]
            while c_info["end"] is not None:
                if c_info["end"] in start_none_list:
                    break
                #end
                if c_info["end"] in tmp_index_group:
                    break
                #end

                tmp_index_group.append(c_info["end"])
                c_info = curve_connection_info[c_info["end"]]

                
            #end

            self.continuous_curve_index_group.append(tmp_index_group)
        #end

        # not include in self.continuous_curve_index_group
        for i, curve in enumerate(self.__curve_set):
            not_include = True
            for curve_index in self.continuous_curve_index_group:
                if i in curve_index:
                    not_include = False
                #end
            #end

            if not_include:
                self.continuous_curve_index_group.append([i])
            #end
        #end

        #print( len(self.__curve_set))

        #print(curve_connection_info)

        #print(self.continuous_curve_index_group)
    #end

    def set_continuous_curve_index_group(self, continuous_curve_index_group):
        self.continuous_curve_index_group = continuous_curve_index_group
    #end

    def create_connection_point(self):
        for curve_index_group in self.continuous_curve_index_group:
            #print(curve_index_group)
            for i, curve_index in enumerate(curve_index_group):
                pre_index  = None if i == 0 else curve_index_group[i-1]
                next_index = None if i == len(curve_index_group) - 1 else curve_index_group[i+1]

                #print(i, curve_index, pre_index, next_index, len(curve_index_group))

                curve = self.__curve_set[curve_index]
                if pre_index is not None:
                    curve.create_connection_point_at_start_point(self.__curve_set[pre_index])
                #end

                if next_index is not None:
                    curve.create_connection_point_at_end_point(self.__curve_set[next_index])
                #end
            #end
        #end
    #end

    def __get_edge_deleted_curve(self, target_curve, ratio, position, pre_connection_point, next_connection_point):
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

        if position == "first" or position == "first_last" or position == "last":
            for i, intersected_curve in enumerate(intersected_curve_set):
                new_curve.update_start_end_index_with_intersection(intersected_curve, ratio)
            #end
        #end

        if pre_connection_point is not None:
            if next_connection_point is not None:
                # position = "middle"
                midpoint_start = pre_connection_point.get_midpoint(target_curve.start_connection_point)
                midpoint_end   = next_connection_point.get_midpoint(target_curve.end_connection_point)
                new_curve.overwrite_start_end_index_finding_nearest(midpoint_start, midpoint_end)
            #end
            else:
                # position = "last"
                midpoint_start = pre_connection_point.get_midpoint(target_curve.start_connection_point)
                midpoint_end   = None
                new_curve.overwrite_start_end_index_finding_nearest(midpoint_start, midpoint_end)
            #end
        else:
            if next_connection_point is not None:
                # position = "first"
                midpoint_start = None
                midpoint_end   = next_connection_point.get_midpoint(target_curve.end_connection_point)
                new_curve.overwrite_start_end_index_finding_nearest(midpoint_start, midpoint_end)
            else:
                # position = "first and last"
                pass # do nothing
            #end
        #end

        #print(new_curve.start_index)

        return new_curve
    #end

    def delete_edge(self, bbox, ratio, global_calc_step, mode, progress_bar=None, log_text=None):
        new_layer = Layer(self.name + "D")
        delete_edge2_step = 0

        new_continuous_curve_index_group = []
        new_curve_index = 0

        for curve_index_group in self.continuous_curve_index_group:
            tmp_new_continuous_curve_index_group = []

            for i, curve_index in enumerate(curve_index_group):
                self.__print_step(mode, global_calc_step+1, delete_edge2_step, "delete edge 2", progress_bar, log_text)

                pre_index  = None if i == 0 else curve_index_group[i-1]
                next_index = None if i == len(curve_index_group) - 1 else curve_index_group[i+1]

                position = self.get_position_of_continuous_curve(pre_index, next_index)

                curve = self.__curve_set[curve_index]
                pre_connection_point = None
                if pre_index is not None:
                    pre_connection_point = self.__curve_set[pre_index].end_connection_point
                #end

                next_connection_point = None
                if next_index is not None:
                    next_connection_point = self.__curve_set[next_index].start_connection_point
                #end

                new_layer.append( self.__get_edge_deleted_curve(curve, ratio, position, pre_connection_point, next_connection_point) )

                tmp_new_continuous_curve_index_group.append(new_curve_index)
                new_curve_index += 1

                delete_edge2_step += 1

            #end

            new_continuous_curve_index_group.append(tmp_new_continuous_curve_index_group)
        #end

        self.continuous_curve_index_group = new_continuous_curve_index_group
        return new_layer
    #end

    def broaden(self, broaden_width, global_calc_step, mode, progress_bar=None, log_text=None):
        new_layer = Layer(self.name + "B")
        curve_num = len(self.__curve_set)

        for curve_index_group in self.continuous_curve_index_group:
            for i, curve_index in enumerate(curve_index_group):
                pre_index  = None if i == 0 else curve_index_group[i-1]
                next_index = None if i == len(curve_index_group) - 1 else curve_index_group[i+1]
                position = self.get_position_of_continuous_curve(pre_index, next_index)

                curve = self.__curve_set[curve_index]
                new_layer.append( curve.broaden(broaden_width, position) )
            #end
        #end

        return new_layer
    #end

    def broad_smoothen(self, global_calc_step, mode, progress_bar=None, log_text=None):
        new_layer = Layer(self.name + "S")

        for i, curve in enumerate(self.__curve_set):
            self.__print_step(mode, global_calc_step, i, "broad_smoothen", progress_bar, log_text)
            new_layer.append( curve.broad_smoothen() )
        #end
        return new_layer
    #end

    def to_str(self):
        s = ''

        for curve in self.__curve_set:
            s += '<path d="'
            s += curve.to_str()
            if self.is_fill:
                s += '" fill="' + self.color + '" opacity="1" stroke="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" />\n'
            else:
                s += '" fill="none" opacity="1" stroke="' + self.color + '" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" />\n'
            #end
        #end
        return s
    #end


    def get_position_of_continuous_curve(self, pre_index, next_index):
        if pre_index is None and next_index is None:
            return "first_last"
        elif pre_index is None:
            return "first"
        elif next_index is None:
            return "last"
        else:
            return "middle"
        #end
    #end

    def printCurve(self):
        for i, curve in enumerate(self.__curve_set):
            print(i, str( curve.going_ctrl_p_set[0].s) )


    def to_str2(self):

        if self.continuous_curve_index_group is None:
            return self.to_str()
        #end

        s = ''

        for curve_index_group in self.continuous_curve_index_group:
            #print(curve_index_group)
            s += '<path d="'

            # going
            for i, curve_index in enumerate(curve_index_group):
                pre_index  = None if i == 0 else curve_index_group[i-1]
                next_index = None if i == len(curve_index_group) - 1 else curve_index_group[i+1]
                position = self.get_position_of_continuous_curve(pre_index, next_index)

                #print(curve_index, pre_index, next_index, position, str( self.__curve_set[curve_index].going_ctrl_p_set[0].p0 ))

                if position == "first" or position == "first_last":

                    the_first_point = self.__curve_set[curve_index].going_ctrl_p_set[0].p0
                    if self.endpoint_style == EndpointStyle.BOTH_POINTED:
                        the_first_point = self.__curve_set[curve_index].going_ctrl_p_set[0].p0.get_midpoint(self.__curve_set[curve_index].returning_ctrl_p_set[0].p3)
                    #end
                    s += "M "
                    s += str( the_first_point ) + " "
                    
                    s += "C "
                    s += str( self.__curve_set[curve_index].going_ctrl_p_set[0].p1 ) + " "
                    s += str( self.__curve_set[curve_index].going_ctrl_p_set[0].p2 ) + " "
                    s += str( self.__curve_set[curve_index].going_ctrl_p_set[0].p3 ) + " "
                else: #position == "middle" or position == "last":
                    s += "C "
                    s += str( self.__curve_set[curve_index].going_ctrl_p_set[0].p1 ) + " "
                    s += str( self.__curve_set[curve_index].going_ctrl_p_set[0].p2 ) + " "
                    s += str( self.__curve_set[curve_index].going_ctrl_p_set[0].p3 ) + " "
                #end
            #end

            # returning
            reversed_curve_index_group = list( reversed(curve_index_group) )
            #print(reversed_curve_index_group)
            for i, curve_index in enumerate( reversed_curve_index_group ):
                pre_index  = None if i == 0 else reversed_curve_index_group[i-1]
                next_index = None if i == len(reversed_curve_index_group) - 1 else reversed_curve_index_group[i+1]
                position = self.get_position_of_continuous_curve(pre_index, next_index)

                #print(curve_index, pre_index, next_index, position)

                if position == "first":
                    if self.endpoint_style == EndpointStyle.BOTH_WIDE:
                        s += "L "
                        s += str( self.__curve_set[curve_index].returning_ctrl_p_set[0].p0 ) + " "
                    #end
                    s += "C "
                    s += str( self.__curve_set[curve_index].returning_ctrl_p_set[0].p1 ) + " "
                    s += str( self.__curve_set[curve_index].returning_ctrl_p_set[0].p2 ) + " "
                    s += str( self.__curve_set[curve_index].returning_ctrl_p_set[0].p3 ) + " "
                elif position == "middle":
                    s += "C "
                    s += str( self.__curve_set[curve_index].returning_ctrl_p_set[0].p1 ) + " "
                    s += str( self.__curve_set[curve_index].returning_ctrl_p_set[0].p2 ) + " "
                    s += str( self.__curve_set[curve_index].returning_ctrl_p_set[0].p3 ) + " "
                elif position == "last":
                    s += "C "
                    s += str( self.__curve_set[curve_index].returning_ctrl_p_set[0].p1 ) + " "
                    s += str( self.__curve_set[curve_index].returning_ctrl_p_set[0].p2 ) + " "

                    the_last_point = self.__curve_set[curve_index].returning_ctrl_p_set[0].p3
                    if self.endpoint_style == EndpointStyle.BOTH_POINTED:
                        the_last_point = self.__curve_set[curve_index].returning_ctrl_p_set[0].p3.get_midpoint(self.__curve_set[curve_index].going_ctrl_p_set[0].p0)
                    #end
                    s += str( the_last_point ) + " "
                    s += "Z "
                elif position == "first_last":
                    if self.endpoint_style == EndpointStyle.BOTH_WIDE:
                        s += "L "
                        s += str( self.__curve_set[curve_index].returning_ctrl_p_set[0].p0 ) + " "
                    #end
                    s += "C "
                    s += str( self.__curve_set[curve_index].returning_ctrl_p_set[0].p1 ) + " "
                    s += str( self.__curve_set[curve_index].returning_ctrl_p_set[0].p2 ) + " "

                    the_last_point = self.__curve_set[curve_index].returning_ctrl_p_set[0].p3
                    if self.endpoint_style == EndpointStyle.BOTH_POINTED:
                        the_last_point = self.__curve_set[curve_index].returning_ctrl_p_set[0].p3.get_midpoint(self.__curve_set[curve_index].going_ctrl_p_set[0].p0)
                    #end
                    s += str( the_last_point ) + " "
                    s += "Z "
                #end
            #end

            s += '" fill="' + self.color + '" opacity="1" stroke="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" />\n'
        #end
        return s
    #end


#end

