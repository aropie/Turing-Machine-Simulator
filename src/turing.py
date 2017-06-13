#!/usr/bin/python
from enum import Enum
import argparse
import sys

class TuringMachine:

    class Delta:
        """
        Class to describe delta function
        """
        def __init__(self, transitions):
            self.transitions = transitions

        def value(self, state, symbol):
            return self.transitions[state][symbol]

    class Movement(Enum):
        """
        Enumeration for movement values
        """
        R = 1
        L = -1

    def __init__(self, states, in_alph, tp_alph, start, blank, end, reject, delta_fun):
        self.states = states
        self.in_alph = in_alph
        self.tp_alph = tp_alph
        self.start = start
        self.blank = blank
        self.end = end
        self.reject = reject
        self.delta_fun = self.Delta(delta_fun)

        self.check_if_valid()

    def __str__(self):
        s = "States".center(15, "-")
        s += "\n"
        for q in self.states:
            s += str(q) + "\n"
        s += "Inital state".center(20, "-")
        s += "\n"
        s += self.start + "\n"
        s += "End states".center(20, "-")
        s += "\n"
        for q in self.end:
            s += str(q) + "\n"
        s += "Reject state".center(20, "-")
        s += "\n"
        s += self.reject + "\n"
        s += "Input alphabet".center(20, "-")
        s += "\n"
        for a in self.in_alph:
            s += a + "\n"
        s += "Tape alphabet".center(20, "-")
        s += "\n"
        for a in self.tp_alph:
            s += a + "\n"
        s += "Delta function".center(20, "-")
        s += "\n"
        for q in self.delta_fun.transitions:
            for symbol in self.delta_fun.transitions[q]:
                s += "({}, {}) -> {}\n".format(q, symbol, self.delta_fun.transitions[q][symbol])

        return s
        

    def check_if_valid(self):
        """
        Checks whether a given TM is valid
        """
        if not self.in_alph.issubset(self.tp_alph):
            print("Entry alphabet is not a subset of tape alphabet")
            sys.exit(0)
        elif self.blank not in self.tp_alph:
            print( "Blank symbol is not in tape alphabet")
            sys.exit(0)
        elif self.start not in self.states:
            print( "Start state is not in states set")
            sys.exit(0)
        elif not self.end.issubset(self.states):
            print( "Start state is not in states set")
            sys.exit(0)

    def is_string_valid(self, string):
        """
        Checks whether a given string is valid
        """
        for s in string:
            if s not in self.in_alph:
                print( "Entry string is not a subset of alphabet")
                sys.exit(0)

    def delta(self, configuration):
        """
        Takes a configuration triplet and returns the new configuration
        """
        actual_state, string, position = configuration
        new_state, substitution, direction = self.delta_fun.value(actual_state, string[position])
        string[position] = substitution
        position += self.Movement[direction].value
        
        return (new_state, string, position)

    def accepts(self, string, verbose=False):
        """
        Tests if a given string is accepted by the TM
        """
        string = list(self.blank + string + self.blank)
        configuration = (self.start, string, 1)
        if verbose:
            print(self)
            print()
            print("__EXECUTION__")
            print("{:10s} {} {:3s}".format("State", "Configuration", "Position"))
            self.print_cfg(configuration)
        while configuration[0] not in self.end:
            if configuration[0] == self.reject:
                return False
            try:
                configuration = self.delta(configuration)
            except KeyError:
                return False
            if verbose:
                self.print_cfg(configuration)
        return True

    def print_cfg(self, configuration):
        state, string, position = configuration
        print("{:10s} {} {:3d}".format(state, "|".join(string), position))

    def n_language(self, n):
        """
        Returns a generator with the strings of the alphabet of length n
        """
        if n <= 0:
            yield ""
        else:
            for s in self.in_alph:
                for w in self.n_language(n-1):
                    yield s + w 

    def language(self):
        """
        Returns a generator for L*
        """
        n = 0
        while(True):
            for w in self.n_language(n):
                yield w
            n += 1

    def accepted_language(self):
        """
        Returns a generator with the accepted language
        """
        language = self.language()
        for w in language:
            if self.accepts(w):
                yield w


def file_to_TM(f):
    """
    Turns a given file in .tm format into a Turing Machine object
    """
    f = open(f)
    states = set()
    in_alph = set()
    tp_alph = set()
    end = set()
    delta = {}
    for x in range(int(f.readline())):
        states.add(f.readline().rstrip("\n"))
    for x in range(int(f.readline())):
        in_alph.add(f.readline().rstrip("\n"))
    for x in range(int(f.readline())):
        tp_alph.add(f.readline().rstrip("\n"))
    start = f.readline().rstrip("\n")
    blank = f.readline().rstrip("\n")
    for x in range(int(f.readline())):
        end.add(f.readline().rstrip("\n"))
    reject = f.readline().rstrip("\n")
    for q in states:
        delta[q] = {}
    for x in range(int(f.readline())):
        st_sym, triplet = f.readline().split(":")
        state, symbol = st_sym.strip().split(" ")
        result = tuple(triplet.strip().split(" "))
        delta[state][symbol] = result
    f.close()
    return TuringMachine(states, in_alph, tp_alph, start, blank, end, reject, delta)


def main():

    parser = argparse.ArgumentParser() 
    parser.add_argument("-f", help="Turing machine file in .tm format", required=True)
    parser.add_argument("-i", help="String to be run with the Turing machine")
    parser.add_argument("-v", help="Prints step-by-step configurations", action="store_true")
    parser.add_argument("-l", help="Prints first n elements of accepted language")
    args = parser.parse_args()

    tm = file_to_TM(args.f)

    if args.i:
        tm.is_string_valid(args.i)
        result = "" if tm.accepts(args.i, args.v) else "NOT "
        print("The string '{}' is {}accepted by the Turing machine".format(args.i, result))

    if args.l:
        i = 1
        for w in tm.accepted_language():
            print(w)
            if i >= int(args.l):
                break
            i += 1
            
if __name__ == "__main__":
    main()
