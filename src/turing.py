#!/usr/bin/python
import argparse
import sys
from enum import Enum


class TuringMachine:
    class DeltaFunction:
        """
        Class to describe delta function
        """

        def __init__(self, transitions):
            self.transitions = transitions

        def apply(self, state, symbol):
            return self.transitions[state][symbol]

    class Movement(Enum):
        """
        Enumeration for movement values
        """

        R = 1
        L = -1

    class Configuration:
        """
        Class to describe a TM configuration triplet
        (Current State, String, Position)
        """

        def __init__(self, state, string_list, position) -> None:
            self.state = state
            self.string_list = string_list
            self.position = position

        def __str__(self):
            return f"({self.state}, {''.join(self.string_list)}, {self.position})"

    def __init__(self, states, in_alph, tp_alph, start, blank, end, reject, delta_fun):
        self.states = states
        self.in_alph = in_alph
        self.tp_alph = tp_alph
        self.start = start
        self.blank = blank
        self.end = end
        self.reject = reject
        self.delta_fun = self.DeltaFunction(delta_fun)

        self._tm_is_valid()

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
                s += "({}, {}) -> {}\n".format(
                    q, symbol, self.delta_fun.transitions[q][symbol]
                )

        return s

    def _tm_is_valid(self):
        """
        Checks whether a given TM is valid
        """
        if not self.in_alph.issubset(self.tp_alph):
            print("Entry alphabet is not a subset of tape alphabet")
            sys.exit(0)
        elif self.blank not in self.tp_alph:
            print("Blank symbol is not in tape alphabet")
            sys.exit(0)
        elif self.start not in self.states:
            print("Start state is not in states set")
            sys.exit(0)
        elif not self.end.issubset(self.states):
            print("Start state is not in states set")
            sys.exit(0)

    def _string_is_valid(self, string):
        """
        Returns whether a given string is valid
        """
        for s in string:
            if s not in self.in_alph:
                print("Entry string is not a subset of alphabet")
                sys.exit(0)

    def _underline_string(self, string):
        return f"\033[4m{string}\033[0m"

    def _get_next_configuration(self, configuration):
        """
        Takes a configuration triplet and returns the new configuration
        """
        new_state, write_sym, direction = self.delta_fun.apply(
            configuration.state, configuration.string_list[configuration.position]
        )
        configuration.state = new_state
        configuration.string_list[configuration.position] = write_sym
        configuration.position += self.Movement[direction].value
        return configuration

    def accepts_string(self, string, verbose=False):
        """
        Tests if a given string is accepted by the TM
        """
        self._string_is_valid(string)
        string_list = list(self.blank + string + self.blank)
        current_configuration = self.Configuration(self.start, string_list, 1)
        if verbose:
            print(self)
            print()
            print("__EXECUTION__")
            print("{:10s} {} {:3s}".format("State", "Configuration", "Position"))
        while current_configuration.state not in self.end:
            if verbose:
                self.print_configuration(current_configuration)
            if current_configuration.state == self.reject:
                return False
            try:
                current_configuration = self._get_next_configuration(
                    current_configuration
                )
            except KeyError:
                return False
        return True

    def print_configuration(self, configuration):
        string_with_position = configuration.string_list[::]
        string_with_position[configuration.position] = self._underline_string(
            configuration.string_list[configuration.position]
        )
        print(
            "{:10s} {} {:3d}".format(
                configuration.state,
                "".join((string_with_position)),
                configuration.position,
            )
        )

    def _get_language_of_size(self, n):
        """
        Returns a generator with the strings of the alphabet of length n
        """
        if n <= 0:
            yield ""
        else:
            for s in self.in_alph:
                for w in self.get_language_of_size(n - 1):
                    yield s + w

    def _language(self):
        """
        Returns a generator for L*
        """
        n = 0
        while True:
            for w in self.get_language_of_size(n):
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


def file_to_TM(file):
    """
    Turns a given file in .tm format into a Turing Machine object
    """
    with open(file) as f:
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
        for state in states:
            delta[state] = {}
        for x in range(int(f.readline())):
            state_symbol, output = f.readline().split(":")
            state, symbol = state_symbol.strip().split(" ")
            next_state, write_sym, movement = output.strip().split(" ")
            delta[state][symbol] = (next_state, write_sym, movement)
    return TuringMachine(states, in_alph, tp_alph, start, blank, end, reject, delta)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="Turing machine file in .tm format", required=True)
    parser.add_argument("-i", help="String to be run with the Turing machine")
    parser.add_argument(
        "-v", help="Prints step-by-step configurations", action="store_true"
    )
    parser.add_argument("-l", help="Prints first n elements of accepted language")
    args = parser.parse_args()

    tm = file_to_TM(args.f)

    if args.i:
        result = "" if tm.accepts_string(args.i, args.v) else "NOT "
        print(
            "The string '{}' is {}accepted by the Turing machine".format(args.i, result)
        )

    if args.l:
        i = 1
        for w in tm.accepted_language():
            print(w)
            if i >= int(args.l):
                break
            i += 1


if __name__ == "__main__":
    main()
