#! /usr/bin/python

__author__="Johnew Zhang <jz2868@columbia.edu>"
__date__ ="$Nov 12, 2018"

## wrapper.py implement a simple decorator for reading file.

def doc_reader(num_fields):
    def doc_iter_decorator(func):
        def func_wrapper(file_name):
            """
            Get an iterator object over the count file. The elements of the
            iterator contain (count, tagtype, tag/tags, word/None) tuples. Blank lines, indicating
            count file boundaries return (None, None, None, None).
            """
            with open(file_name, 'r') as f:
                l = f.readline()
                while l:
                    line = l.strip()
                    if line: # Nonempty line
                        yield func(line)
                    else: # Empty line
                        yield (None, )*num_fields                        
                    l = f.readline()
                f.close()
        return func_wrapper
    return doc_iter_decorator
