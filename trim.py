import sys
def main(dir):
	data = ["train", "test", "valid"]
	for name in data:
		with open("/".join([dir, name + ".wp_target"])) as f:
			stories = f.readlines()
		stories = [" ".join(i.split()[0:1000]) for i in stories]
		with open("/".join([dir, name + ".wp_target"]), "w") as o:
			for line in stories:
				o.write(line.strip() + "\n")


if __name__ == '__main__':
	## python trim.py 'example/stories/writingPrompts'
	## main takes the path of the dataset and trim
	main(sys.argv[1])
