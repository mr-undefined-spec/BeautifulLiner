#import numpy as np

#import os
#import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '../../handler'))

from basic_handler import BasicHandler

class PickupIntersectionCandidatesHandler(BasicHandler):
    @staticmethod
    def process(target_curve, other_curves):
        candidates = []
        for other_curve in other_curves:
            if other_curve == target_curve:
                # do nothing
                pass
            elif target_curve.rect.test_collision(other_curve.rect):
                candidates.append(other_curve)
            #end
        #end
        return candidates
    #end
#end
