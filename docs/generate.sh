#!/bin/bash

make clean ; make html

python3 $(which sphinx-apidoc) -o ./source/ ../Tree
