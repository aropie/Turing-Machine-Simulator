# Turing Machine Simulator


Simulates a turing machine given a **.tm** file.

## Usage
`turing.py [-h] -f F [-i I] [-v] [-l L]`

optional arguments:  
  -h, --help  Show this help message and exit  
  -f F        Turing machine file in .tm format  
  -i I        String to be run with the Turing machine  
  -v          Prints step-by-step configurations  
  -l L        Prints first n elements of accepted language  

## .tm format
**.tm** format is a format for Turing machines analogue to **.cfg** format by University of
Waterloo for context free grammars.  
It's a text file with the following format:

* *n*, a positive integer indicating the number of states in the machine, 
followed by *n* lines conatining different strings for each state.

* *m*, a positive integer indicating the number of symbols in the input alphabet,
followed by *m* lines containing different characters.

* *l*, a positive integer indicating the number of symbols in the tape alphabet, 
followed by *l* lines containing different characters.

* A line containing the initial state.

* A line containing the blank character.

* *t*, a positive integer indicating the number of final states,
 followed by *t* lines containing different strings for each final state.
 
* A line containing the rejection state.
 
* *s*, a positive integer indicating the number of transitions,
followed by *s* lines containing the transitions in the following format:

    * *State symbol* **:** *state symbol direction*  
    So transition d(q1, *a*) -> (q2, *b*, L) would be:   
    `q1 a : q2 b L`
    
The rejection state is not necesary for some machines since the machine will assume rejection if a transition is not defined, although rejection state *needs* to be specified.

## Test files
Enclosed within are two sample *.tm* files:

* **even_number_of_zeros**: A machine that accepts strings in *{0, 1}\** that have an even number of zeroes

* **an_bn_cn**: A machine that accepts strings in *{a, b, c}\** that are of the form *a*^n, *b*^n and *c*^n
