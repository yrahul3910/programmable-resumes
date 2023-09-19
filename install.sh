#!/bin/bash
cd progres && 
    pysh main.pysh -o main.py -t &&
    cd .. && 
    pip3 install .