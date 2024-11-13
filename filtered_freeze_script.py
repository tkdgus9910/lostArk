# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 14:48:37 2024

@author: tmlab
"""

import os

input_file = "requirements.txt"
output_file = "requirements.txt"

exclude_keywords = ["win32", "mkl"]

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        if not any(keyword in line for keyword in exclude_keywords):
            outfile.write(line)
print(f"Filtered requirements saved to {output_file}")