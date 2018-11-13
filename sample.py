__author__="Johnew Zhang <jz2868@columbia.edu>"
__date__ ="$Nov 12, 2018"

import sys
from util import sample

def main(args):
	"""
	args contrain either four or five arguments
	python sample.py input_dir target_file_name source_file_name output_dir 
	or 
	python sample.py input_dir target_file_name source_file_name output_dir 0.1
	The last argument represents the percentage to be sampled
	"""	
	if len(args) == 4+1:
		sample(args[1], args[2], args[3], args[4])
	else:
		sample(args[1], args[2], args[3], args[4], prob=float(args[5]))

if __name__ == '__main__':
	"""
	To sample the writingPrompt dataset, type
	python sample.py examples/stories/writingPrompts train.wp_target train.wp_source examples/stories/writingPrompts/sample
	python sample.py examples/stories/writingPrompts test.wp_target test.wp_source examples/stories/writingPrompts/sample
	python sample.py examples/stories/writingPrompts valid.wp_target valid.wp_source examples/stories/writingPrompts/sample
	"""
	main(sys.argv)
