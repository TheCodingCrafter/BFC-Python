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

import lexer
from ply import lex
import os

# cpp code
C_HEADER = '''#include <iostream>
#include <stdlib.h>
int main(int argc, char** argv) {
    char* arg;
    argv++;
    arg = *argv;
    char D[30000] = {0};
    int dpos = 0;
    int ac = 0;
'''
C_FOOTER = '''return 0;}'''

C_INC = 'D[dpos]++;\n'
C_DEC = 'D[dpos]--;\n'
C_ADD = 'D[dpos] += {v};\n'
C_SUB = 'D[dpos] -= {v};\n'

C_M_RIGHT_INC = 'dpos++;\n'
C_M_LEFT_DEC = 'dpos--;\n'
C_M_RIGHT = 'dpos += {v};\n'
C_M_LEFT = 'dpos -= {v};\n'

C_L_BGN = '''while (D[dpos] != 0) {\n'''
C_L_END = '''};\n'''

C_OUTPUT = 'std::cout << D[dpos];\n'

C_INPUT = 'D[dpos] = arg[ac]; ac++;\n'


# errors
class BFError(Exception):
    pass

class InvalidSyntax(BFError):
    pass

class BFToken:
    def __init__(self, ID: str, value: int) -> None:
        self.ID = str(ID)
        self.value = int(value)

    def __str__(self) -> str:
        return f'BFToken(ID={self.ID}, value={self.value})'
    
    def __repr__(self) -> str:
        return str(self)

class Parser:
    def __init__(self):
        pass

    def read_file(self, filename: str) -> str:
        '''
        read data from a file
        '''
        with open(filename, 'r') as f:
            return f.read()

    def write_file(self, filename: str, data: bytearray) -> None:
        '''
        write binary data to a file
        '''
        with open(filename, 'wb') as f:
            f.write(data)
        return

    def tokens_to_bf_tokens(self, tokens: list[lex.LexToken], allow_non_numeric_ext: bool) -> list[BFToken]:
        '''
        converts LexTokens to BFTokens
        '''
        n_tokens = []
        tok_names = {
            'PLUS': 'INCREMENT',
            'MINUS': 'DECREMENT',
            'LEFT_BRACKET': 'LOOP_BEGIN',
            'RIGHT_BRACKET': 'LOOP_END',
            'LESS_THAN': 'MOVE_LEFT',
            'GREATER_THAN': 'MOVE_RIGHT',
            'COMMA': 'INPUT',
            'DOT': 'OUTPUT'
        }
        skip_next = False
        non_numeric_tokens = [ # disallowed for extension via ints unless --allow-loop-extension is enabled TODO: pass args to compile() & make this work
            'LEFT_BRACKET',
            'RIGHT_BRACKET'
        ]
        loop_depth = 0 # keep track of loops

        for i, tok in enumerate(tokens):
            if skip_next:
                skip_next = False
                continue
            else:
                if tok.type == "NUMBER":
                    raise InvalidSyntax(f"Unexpected Number Token (ln. {tok.lineno}, char. {tok.lexpos})")

            name = tok_names[tok.type]
            # number handling
            try:
                if tokens[i + 1].type == "NUMBER":
                        if tok.type in non_numeric_tokens:
                            # check if --allow-loop-extension is enabled
                            if not allow_non_numeric_ext:
                                raise InvalidSyntax(f"{tok.type} tokens cannot be extended. (ln. {tok.lineno}, char. {tok.lexpos})")
                            
                        value = tokens[i + 1].value
                        skip_next = True
                else:
                    value = 1
            except IndexError:
                value = 1
            
            n_tokens.append(BFToken(name, value))
            ctok = n_tokens[-1]
            if ctok.ID == "LOOP_BEGIN":
                loop_depth += ctok.value
                print(f'+{ctok.value}: {loop_depth}')
            
            elif ctok.ID == "LOOP_END":
                loop_depth -= ctok.value
                print(f'-{ctok.value}: {loop_depth}')

            if loop_depth < 0:
                raise InvalidSyntax(f"Unmatched Loop End (ln. {tok.lineno}, char. {tok.lexpos})")

            if (i >= (len(tokens) - 1)) and (loop_depth > 0): # if last token
                raise InvalidSyntax(f"Unclosed Loop token.")

            


        return n_tokens
    
    def optimize_bf_tokens(self, tokens: list[BFToken]) -> list[BFToken]:
        '''
        optimizes bf tokens by combining the values of same type tokens to reduce list size
        '''
        n_tokens = []
        current_type = None
        current_length = 0

        for tok in tokens:
            # starting new chain of same type tokens
            if tok.ID != current_type:
                if current_length > 0:
                    # add to array and reset
                    n_tokens.append(BFToken(current_type, current_length))
                    current_length = tok.value
                    current_type = tok.ID

                else:
                    # assume start of chain, reset
                    current_length = tok.value
                    current_type = tok.ID

            else:
                current_length += tok.value

        
        # add last chain to array
        n_tokens.append(BFToken(current_type, current_length))

        # return
        return n_tokens

    def bf_tokens_to_c_code(self, tokens: list[BFToken]) -> str:
        c_code = C_HEADER
        for token in tokens:
            match token.ID:
                case 'INCREMENT':
                    if token.value == 1:
                        c_code += C_INC
                    else:
                        c_code += C_ADD.format(v=token.value)

                case 'DECREMENT':
                    if token.value == 1:
                        c_code += C_DEC
                    else:
                        c_code += C_SUB.format(v=token.value)

                case 'MOVE_LEFT':
                    if token.value == 1:
                        c_code += C_M_LEFT_DEC
                    else:
                        c_code += C_M_LEFT.format(v=token.value)
                
                case 'MOVE_RIGHT':
                    if token.value == 1:
                        c_code += C_M_RIGHT_INC
                    else:
                        c_code += C_M_RIGHT.format(v=token.value)

                case 'OUTPUT':
                    for _ in range(token.value):
                        c_code += C_OUTPUT

                case 'INPUT':
                    for _ in range(token.value):
                        c_code += C_INPUT

                case 'LOOP_BEGIN':
                    for _ in range(token.value):
                        c_code += C_L_BGN
                
                case 'LOOP_END':
                    for _ in range(token.value):
                        c_code += C_L_END
 


        c_code += C_FOOTER

        return c_code
    
    def compile(self, input_file: str, outputfile: str, preprocess_only: bool, allow_non_numeric_ext: bool) -> list[bool, any]:
        try:
            file_data = self.read_file(input_file)
            file_raw_tokens = lexer.tokenize(file_data)
            file_bf_tokens = self.optimize_bf_tokens(self.tokens_to_bf_tokens(file_raw_tokens, allow_non_numeric_ext))

            if preprocess_only:
                def _bftk_to_str(tks: list[BFToken]) -> str:
                    bf_chars = {
                        'INCREMENT': '+',
                        'DECREMENT': '-',
                        'MOVE_LEFT': '<',
                        'MOVE_RIGHT': '>',
                        'OUTPUT': '.',
                        'INPUT': ',',
                        'LOOP_BEGIN': '[',
                        'LOOP_END': ']'
                    }

                    s = ''
                    for tk in tks:
                        s += str(bf_chars[tk.ID]) * tk.value

                    return s

                self.write_file(outputfile, _bftk_to_str(file_bf_tokens).encode())
                return [True, None]

            c_code = self.bf_tokens_to_c_code(file_bf_tokens)

            self.write_file(outputfile + '.tmp', c_code.encode())

            v = os.system(f'g++ -x c++ {outputfile + '.tmp'} -s -o {outputfile}')
            if v != 0: return [False, v]
            v = os.system(f'del {outputfile + '.tmp'} -f')
            if v != 0: return [False, v]

            return [True, None]
        
        except Exception as e:
            return [False, e]


if __name__ == '__main__':
    p = Parser()
    print(p.compile('test.bf', 'test.cpp', False))
