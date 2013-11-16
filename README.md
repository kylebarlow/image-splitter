image-splitter
==============

Python application to split a large image onto multiple sheets of paper.
To view options, run with -h flag:
    ./image-splitter.py -h

The script takes as options what your desired image size and paper size are, in arbitrary units, and then creates corresponding PDFs.
When printing each PDF, print full-size on your paper to make the sizes make sense.

## Requirements ##
* Python3
* The Pillow implementation of PIL for Python3. This can be installed on Ubuntu/Debian with:
        sudo apt-get install python3-imaging

## License ##

Licensed under GPLv3