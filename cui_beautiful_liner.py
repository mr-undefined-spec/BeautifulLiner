from argparse import ArgumentParser

#import os
#import sys
from execute_manager import ExecuteManager

def print_canvas(layer_set):
    template = r'<path stroke="#00ff00" stroke-width="1.5" fill="none" stroke-linecap="round" opacity="1" stroke-linejoin="round"'
    for layer in layer_set:
        for i, curve in enumerate(layer):
            s = ""
            s += template
            s += r' d="'
            s += curve.to_str()
            s += r'" />'
            print(s)
        #end

def main():
    usage = 'Usage: python {} FILE [-C|--continuous_ratio <value>(default: 0.25)] [-d|--delete_ratio <value>(default: 0.25)] [-l|--linear_approximate_length <value>(default: 1.0)] [-b|--broad_width <value>(default: 1.0)] [-n|--no_broad] [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('reading_file_path', type=str,
                            help='Reading svg file path.')
    argparser.add_argument('-C', '--continuous_ratio',
                            type=float,
                            dest='continuous_ratio',
                            default=2.0,
                            help='Ratio of both end areas to check continuous curve')
    argparser.add_argument('-e', '--eps_smooth_curve',
                            type=float,
                            dest='eps_smooth_curve',
                            default=1.0,
                            help='Convergence condition for smooth approximate curve')
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
    argparser.add_argument('-c', '--color',
                            type=str,
                            dest='output_color',
                            default="black",
                            help='Output line color')
    args = argparser.parse_args()

    ExecuteManager.execute(args.reading_file_path, args.linear_approximate_length, args.delete_ratio, args.broad_width, args.output_color)

#end

if __name__ == '__main__':
    main()
#end
