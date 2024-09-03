'''
BFC.
Copyright (C) 2024  TheCodingCrafter

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import argparse
import sys
import parser
from time import monotonic

# consts
VERSION = "1.0.1"

START_MESSAGE = '''BFC  Copyright (C) 2024  TheCodingCrafter
This program comes with ABSOLUTELY NO WARRANTY; for details use `--show-w'.
This is free software, and you are welcome to redistribute it
under certain conditions; use `--show-c' for details.
    
'''

WARRANTY_NOTICE = '''THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR
CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES
ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT
NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR
LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM
TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER
PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

'''

DISTRIBUTION_NOTICE = '''You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.



You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these
conditions:

-   a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.
-   b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under
    section 7. This requirement modifies the requirement in section 4
    to "keep intact all notices".
-   c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy. This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged. This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.
-   d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit. Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

'''

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
    aparser.add_argument('--allow-loop-extension', dest='loop_extension', action='store_true', help="Allow loop extension")
    aparser.add_argument('--do-not-optimize', dest='no_optimize', action='store_true', help="Don't optimize tokens")
    aparser.add_argument('--show-w', dest='show_warranty', action='store_true', help="Display warranty info")
    aparser.add_argument('--show-c', dest='show_dist_info', action='store_true', help="Display re-distribution info")


    args = aparser.parse_args(argv)
    return aparser, args
 
if __name__ == "__main__":
    print(START_MESSAGE)
    begin_time = monotonic()
    # get and verify args
    aparser, args = get_args(sys.argv[1:])
    
    # version
    if args.show_version:
        print(f'BFC (brainfuck compiler): {VERSION}')
        exit(0)

    if args.show_warranty:
        print(WARRANTY_NOTICE)
        if not args.show_dist_info: exit(0)
    
    if args.show_dist_info:
        print(DISTRIBUTION_NOTICE)
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