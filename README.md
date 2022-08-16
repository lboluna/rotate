# rotate.py
Simplistic script to rotate ports in touchstone file

Title: rotate.py

Purpose: Convert port numbering of S4P touchstone file.
Author: luis.boluna@keysight.com




Known issues/limitations:
    Expand use of ports 
     - Check port numbering for errors
     - Plan not to hard code ports, for other applications
    

Examples:
    
python rotate.py filename.s4p
python rotate.py filename.s4p --newfile foo.s4p
