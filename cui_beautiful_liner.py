import os
import sys

global calc_step
calc_step = 0
global total_calc_step

sys.path.append(os.path.join(os.path.dirname(__file__), 'controller'))
from controller import Controller

from argparse import ArgumentParser

def main():
    usage = 'Usage: python {} FILE [-d|--delete_ratio <value>(default: 0.25)] [-l|--linear_approximate_length <value>(default: 1.0)] [-b|--broad_width <value>(default: 1.0)] [-n|--no_broad] [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('reading_file_path', type=str,
                            help='Reading svg file path.')
    argparser.add_argument('-d', '--delete_ratio',
                            type=float,
                            dest='delete_ratio',
                            default=0.25,
                            help='Ratio of both end areas to delete overhangs in the curve')
    argparser.add_argument('-l', '--linear_approximate_length',
                            type=float,
                            dest='linear_approximate_length',
                            default=1.0,
                            help='Length of the small segment when linearly approximating')
    argparser.add_argument('-b', '--broad_width',
                            type=float,
                            dest='broad_width',
                            default=1.0,
                            help='Width size when broadening the curve')
    argparser.add_argument('-n', '--no_broad',
                            action='store_false',
                            help='Donot broaden path')
    args = argparser.parse_args()

    controller = Controller()
    controller.run("CUI", args.reading_file_path, args.linear_approximate_length, args.delete_ratio, args.broad_width)
    print("Create " + args.reading_file_path.replace(".svg", "_BeauL.svg") )
    print("END OF JOB")
#end

if __name__ == '__main__':
    main()
#end
