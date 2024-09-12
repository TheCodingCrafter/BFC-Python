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
import parser

class State:
    def __init__(self, m_size: int=30000) -> None:
        self.m_size = m_size
        self.memory = bytearray([0] * m_size)
        self.mpointer = 0
        self.ipointer = 0
    
    def ipointer_in_bounds(self) -> False:
        return ((self.ipointer >= 0) and (self.ipointer < self.m_size))

    def mpointer_in_bounds(self) -> False:
        return ((self.mpointer >= 0) and (self.mpointer < self.m_size))

class Debugger:
    def __init__(self, filename, m_size: int=30000) -> None:
        self.filename = filename
        self.bf_tokens = []
        self.state = State(m_size==m_size)

    def load_file(self) -> None:
        p = parser.Parser()
        with open(self.filename, 'r') as f:
            dat = f.read()

        raw_tokens = lexer.tokenize(dat)
        bf_tokens = p.optimize_bf_tokens(p.tokens_to_bf_tokens(raw_tokens, False))
        
        def _expand_bf_tks(bf_tks: list[parser.BFToken]) -> list[parser.BFToken]:
            n_tks = []
            try:
                for token in bf_tks:
                    for _ in range(int(token.value)):
                        n_tks.append(parser.BFToken(token.ID, 1))
            except IndexError:
                return []

            return n_tks
    
        self.bf_tokens = _expand_bf_tks(bf_tokens)


    def step(self) -> None:
        pass

    def step_n(self, n: int=1) -> None:
        pass

if __name__ == '__main__':
    d = Debugger('test.bf')
    d.load_file()
    print(d.bf_tokens)