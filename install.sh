#!/bin/bash
cd progres && 
    pysh main.pysh -o main.py -t &&
    cd .. && 
    pip3.9 install . &&
    rm progres/main.py