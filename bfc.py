import argparse
import sys
import parser
from time import monotonic

# consts
VERSION = "1.0.1"

def gen_output_file(input_f: str) -> str:
    def _strip_extension(fname: str) -> str:
        return '.'.join(fname.split('.')[:-1])
    
    return _strip_extension(input_f) + '.exe'


def get_args(argv) -> tuple[argparse.ArgumentParser, argparse.Namespace]:
    # create parser
    aparser = argparse.ArgumentParser(description="BFC, brainfuck compiler")

    # add arguments
    aparser.add_argument('input_file', metavar='INPUT_FILE', type=str, help="Input File", nargs='?', default=None)
    aparser.add_argument('-o', '--output_file', metavar='OUTPUT_FILE', type=str, required=False, help='Output file')
    aparser.add_argument('-p', '--preprocess', dest='preprocess', action='store_true', help='Preprocess but do not compile')
    aparser.add_argument('-v', '--version', dest='show_version', action='store_true', help='Show Compiler version')
    aparser.add_argument('--allow-loop-extension', dest='loop_extension', action='store_true', help="allow loop extension")
    aparser.add_argument('--do-not-optimize', dest='no_optimize', action='store_true', help="don't optimize tokens")

    args = aparser.parse_args(argv)
    return aparser, args

if __name__ == "__main__":
    begin_time = monotonic()
    # get and verify args
    aparser, args = get_args(sys.argv[1:])
    
    # version
    if args.show_version:
        print(f'BFC (brainfuck compiler): {VERSION}')
        exit(0)

    # input file
    if args.input_file is None:
        aparser.print_usage()
        exit(-1)
    args_input_file = args.input_file

    # output file
    if args.output_file is None:
        args_output_file = gen_output_file(args_input_file)
    else:
        args_output_file = args.output_file

    # non-critical args
    args_preprocess = args.preprocess
    args_loop_extension = args.loop_extension
    args_no_optimize = args.no_optimize

    '''
    print(f'input file: {args_input_file}')
    print(f'output file: {args_output_file}')
    print(f'args_preprocess: {args_preprocess}')
    print(f'args_loop_extension: {args_loop_extension}')
    print(f'args_no_optimize: {args_no_optimize}')
    '''

    # compile!
    par = parser.Parser()
    code, status = par.compile(args_input_file, args_output_file, preprocess_only=args_preprocess, allow_non_numeric_ext=args_loop_extension)

    end_time = monotonic()
    total_time = end_time - begin_time

    # display
    if code:
        print(f'Operation FINISHED in {total_time:.03f} seconds.')
    else:
        print(f'Operation FAILED in {total_time:.03f} seconds. (Error: {status})')