__author__="Johnew Zhang <jz2868@columbia.edu>"
__date__ ="$Nov 12, 2018"

import sys
from util import summary_stat

def main(args):
	"""
	python summary.py input_dir 
	"""	
	summary_stat(args[1])

if __name__ == '__main__':
	"""
	python summary.py examples/stories/writingPrompts
	"""
	main(sys.argv)
