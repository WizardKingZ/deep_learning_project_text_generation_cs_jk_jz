#! /usr/bin/python

__author__="Johnew Zhang <jz2868@columbia.edu>"
__date__ ="$Nov 12, 2018"

from base import doc_reader
import numpy.random as npr

@doc_reader(1)
def simple_test_iterator(line):
    """
    Get an iterator object over the test corpus file
    """
    return line

def sample(input_dir, target, source, output_dir, prob=0.1):
    ## draw 10% sample from the dataset
    target_iterator = simple_test_iterator("/".join([input_dir, target]))
    source_iterator = simple_test_iterator("/".join([input_dir, source]))
    target_output_file = file("/".join([output_dir, target]), 'w')
    source_output_file = file("/".join([output_dir, source]), 'w')
    total_n = 1
    sampled_n = 1
    for t_it, s_it in zip(target_iterator, source_iterator):
        c = npr.choice([0, 1], size=1, p=[1.-prob, prob])
        total_n += 1
        if c == 1:
            target_output_file.write(t_it+"\n")
            source_output_file.write(s_it+"\n")
            sampled_n += 1
    target_output_file.close()
    source_output_file.close()
    print "Sampled: {} stories; Total: {} stories".format(sampled_n, total_n)