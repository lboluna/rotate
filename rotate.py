# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 22:11:36 2022

Title: rotate.py
Purpose: Convert port numbering of S4P touchstone file.
Author: luis.boluna@keysight.com
Known issues/limitations:
    Expand use of ports 
     - Check port numbering for errors
     - Not hard code ports, for other applications
    
    Examples:
    
python rotate.py filename.s4p
python rotate.py filename.s4p --newfile foo.s4p
"""

import skrf as rf
import os
import ast

def rotate_ports(FILENAME, NEWFILENAME):
    try:
        s4p_in = rf.Network(FILENAME)
    except:
        raise ValueError('File: '+FILENAME+' does not exist')
    nports = s4p_in.nports
    if nports != 4:
        raise ValueError('Number of ports is not 4 but '+nports)
    s4p_in.renumber([0,1,2,3],[0,2,1,3])
    print("\n>>> Port 1 unchanged to Port 1")
    print(">>> Port 2 swapped to Port 3")
    print(">>> Port 3 swapped to Port 2")
    print(">>> Port 4 unchanged to Port 4")
    file, file_extension = os.path.splitext(NEWFILENAME)
    print(file_extension)
    if file_extension !=  '.s4p':
        s4p_in.write_touchstone(NEWFILENAME+'.s4p')
        print("\n File saved: {}\n".format(NEWFILENAME+'.s4p'))
    else:
        s4p_in.write_touchstone(NEWFILENAME)
        print("\n File saved: {}\n".format(NEWFILENAME))

def parse_ports(p):
    import numpy as np

    p0 = np.array(p[0])
    p1 = np.array(p[1])
    # check if 4 ports
    if p0.size == 4 and p1.size == 4:   
        #print("four ports, ok")
        #check if any zeros in port numbering
        if not np.where(p0) or not np.where(p1):
            #print("zero found")
            #substract one to make port pythonic (zero index referenced)
            p0 = p0 - 1
            p1 = p1 - 1
            val0, cnt0 = np.unique(p0, return_counts = True)
            val1, cnt1 = np.unique(p1, return_counts = True)
            #if any duplicate values found then flag as error
            if np.any(cnt0 > 1) or np.any(cnt1 > 1):
                raise ValueError("Error: Port numbering duplicate values found")
            #if any ports outside of 0 to 3 flag it as error       
            elif np.logical_and(p0 > -1, p0 < 4).all() and np.logical_and(p1 > -1, p1 < 3).all():
                return True,p0.tolist(),p1.tolist()
            else:
                raise ValueError("Error: Port numbering out of range")
    else:
        raise ValueError("Error: Port numbering: Number of ports is not four")



def main():
    import argparse
    
    help_header = "\n\n" \
                  "================================================\n" \
                  "Converts port numbering of S4P touchstone file.\n"\
                  "\n" \
                  "Example:\n\n" \
                  "python rotate.py filename.s4p\n"\
                  "\n" \
                  "or,\n" \
                  "\n" \
                  "python rotate.py filename.s4p --newfile foo.s4p\n" \
                  "\n\n" \
                  "Version 1.0    ---    luis.boluna@keysight.com\n"\
                  "================================================\n\n"

    parser = argparse.ArgumentParser(help_header)
    parser.add_argument('file', metavar = 'file', type=str, help = "The filename of the touchstone S4P file")
    parser.add_argument('--newfile', type=str, required=False, help = "New filename if it is not same as original")
    #parser.add_argument('--ports', type=str, required=False, help = "example: [1,2,3,4],[1,3,2,4]")
    args = parser.parse_args()
    
    #p = ast.literal_eval(args.ports)
    
    # if args.ports:
    #     port = parse_ports(p)
    # else:
    #     port = "[0,1,2,3],[0,2,1,3]"
    
    if args.newfile:
        rotate_ports(args.file, args.newfile)
    else:
        rotate_ports(args.file. args.file) 
    
if __name__ == "__main__":
        main()
