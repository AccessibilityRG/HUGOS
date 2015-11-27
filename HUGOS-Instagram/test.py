__author__ = 'localadmin_hentenka'

import os

# Create variables
filename = "test.txt"
folder = r"C:\HY-Data\HENTENKA\KOODIT\Opetus\SWC_Helsinki\HUGOS1"

# Create a full path to file
fullpath = os.path.join(folder, filename)
print(fullpath)

# Open
f = open(fullpath, 'w')

# Write some stuff to the file
f.write("This my first line\nThis is my second line.\n")
f.write("This is the third line")

# Close the file
f.close()

