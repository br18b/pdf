def load_params(input_filename):
	input = open("input.txt", "r")
	lines = input.readlines()
	path = "~/"
	filenames = ["DD","DD"]
	frames = range(0,100)
	tasks = ["vx","vy","vz"]
	for line in lines:
		tokens = line.split()
		if tokens[0] == "path" or tokens[0] == "-p":
			path = tokens[1]
			if path[-1] == "/":
				path = path[:-1]
		elif tokens[0] == "filenames" or tokens[0] == "-f":
			filenames[0] = tokens[1]
			filenames[1] = tokens[2]
		elif tokens[0] == "range" or tokens[0] == "-r":
			start = int(tokens[1])
			end = int(tokens[2])+1
			skip = 1
			if len(tokens) > 3:
				skip = int(tokens[3])
			frames = range(start, end, skip)
		elif tokens[0] == "tasks" or tokens[0] == "-t":
			tasks = tokens[1:]
	input.close()
	print("path: %s"%(path))
	print("data file names: %sXXXX/%sXXXX"%(filenames[0],filenames[1]))
	if len(frames) > 1 and frames[2]-frames[1] > 1:
	        print("frames: %s%04d/%s%04d to %s%04d/%s%04d, skip %d"%(
	filenames[0], frames[0], filenames[1], frames[0],
	filenames[0], frames[-1], filenames[1], frames[-1], frames[2]-frames[1]-1))
	else:
	        print("frames: %s%04d/%s%04d to %s%04d/%s%04d, no skipping"%(
	filenames[0], frames[0], filenames[1], frames[0],
	filenames[0], frames[-1], filenames[1], frames[-1]))
	print("tasks:\n")
	for task in tasks:
		print(task)
	return path, filenames, frames, tasks
